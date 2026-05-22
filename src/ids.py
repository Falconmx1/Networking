from scapy.all import ARP, Ether, srp, sniff, send
import time
import sys
from colorama import init, Fore, Style

init(autoreset=True)

class ARPSpoofDetector:
    def __init__(self, interface=None):
        self.interface = interface
        self.mac_ip_map = {}
        self.suspicious_activity = []
        
    def get_mac(self, ip):
        """Obtiene MAC de una IP usando ARP request"""
        arp_request = ARP(pdst=ip)
        broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = broadcast / arp_request
        answered = srp(packet, timeout=2, verbose=False)[0]
        
        if answered:
            return answered[0][1].hwsrc
        return None
    
    def scan_network(self, ip_range="192.168.1.0/24"):
        """Escanea la red para mapear IP -> MAC"""
        print(f"{Fore.CYAN}[*] Escaneando red {ip_range}...")
        arp_request = ARP(pdst=ip_range)
        broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = broadcast / arp_request
        answered = srp(packet, timeout=2, verbose=False)[0]
        
        for sent, received in answered:
            self.mac_ip_map[received.psrc] = received.hwsrc
            
        print(f"{Fore.GREEN}[✓] Encontrados {len(self.mac_ip_map)} dispositivos")
        return self.mac_ip_map
    
    def detect_arp_spoof(self, packet):
        """Detecta posibles ataques ARP spoofing"""
        if packet.haslayer(ARP) and packet[ARP].op == 2:  # ARP response
            ip = packet[ARP].psrc
            mac = packet[ARP].hwsrc
            
            if ip in self.mac_ip_map:
                if self.mac_ip_map[ip] != mac:
                    alert = f"🚨 ALERTA ARP SPOOFING: IP {ip} está cambiando MAC! Antes: {self.mac_ip_map[ip]}, Ahora: {mac}"
                    print(f"{Fore.RED}{alert}")
                    self.suspicious_activity.append({
                        'type': 'ARP Spoofing',
                        'ip': ip,
                        'old_mac': self.mac_ip_map[ip],
                        'new_mac': mac,
                        'timestamp': time.time()
                    })
                    self.mac_ip_map[ip] = mac  # Actualizar para futuras detecciones
            else:
                # Nueva IP detectada
                print(f"{Fore.YELLOW}[!] Nueva IP detectada: {ip} -> {mac}")
                self.mac_ip_map[ip] = mac
    
    def start_monitoring(self, interface=None):
        """Inicia monitoreo ARP en tiempo real"""
        iface = interface or self.interface
        print(f"{Fore.CYAN}[*] Monitoreando ARP en {iface}")
        print(f"{Fore.YELLOW}[!] Presiona Ctrl+C para detener")
        
        try:
            sniff(iface=iface, prn=self.detect_arp_spoof, store=0, filter="arp")
        except KeyboardInterrupt:
            print(f"\n{Fore.GREEN}[✓] Monitoreo detenido")
            return self.suspicious_activity

def detect_intrusions(interface):
    """Función principal de detección de intrusos"""
    detector = ARPSpoofDetector(interface)
    
    # Primero escanear la red
    detector.scan_network()
    
    # Luego monitorear
    alerts = detector.start_monitoring(interface)
    return alerts
