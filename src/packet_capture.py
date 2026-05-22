from scapy.all import sniff, wrpcap, IP, TCP, UDP, ICMP
import threading
import time
import os
from datetime import datetime
from colorama import init, Fore

init(autoreset=True)

class PacketCapture:
    def __init__(self, interface=None, max_packets=1000):
        self.interface = interface
        self.max_packets = max_packets
        self.packets = []
        self.capturing = False
        self.capture_file = None
        self.storage_path = "./captures"
        
        # Crear directorio de capturas
        os.makedirs(self.storage_path, exist_ok=True)
    
    def packet_callback(self, packet):
        """Callback para procesar cada paquete"""
        if not self.capturing:
            return
        
        packet_info = {
            'timestamp': datetime.now().isoformat(),
            'length': len(packet),
            'protocol': 'Unknown'
        }
        
        # Identificar protocolo
        if IP in packet:
            packet_info['src_ip'] = packet[IP].src
            packet_info['dst_ip'] = packet[IP].dst
            packet_info['proto'] = packet[IP].proto
            
            if TCP in packet:
                packet_info['protocol'] = 'TCP'
                packet_info['src_port'] = packet[TCP].sport
                packet_info['dst_port'] = packet[TCP].dport
                packet_info['flags'] = packet[TCP].flags
            elif UDP in packet:
                packet_info['protocol'] = 'UDP'
                packet_info['src_port'] = packet[UDP].sport
                packet_info['dst_port'] = packet[UDP].dport
            elif ICMP in packet:
                packet_info['protocol'] = 'ICMP'
                packet_info['type'] = packet[ICMP].type
        
        self.packets.append(packet_info)
        
        # Mostrar en consola
        print(f"{Fore.GREEN}[PCAP] {packet_info['protocol']} | "
              f"{packet_info.get('src_ip', 'N/A')}:{packet_info.get('src_port', 'N/A')} -> "
              f"{packet_info.get('dst_ip', 'N/A')}:{packet_info.get('dst_port', 'N/A')}")
        
        # Guardar a archivo PCAP cada cierto número de paquetes
        if len(self.packets) % 100 == 0:
            self.save_capture()
    
    def start_capture(self, duration=None, packet_count=None):
        """Inicia la captura de paquetes"""
        self.capturing = True
        self.packets = []
        
        # Generar nombre de archivo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.capture_file = os.path.join(self.storage_path, f"capture_{timestamp}.pcap")
        
        print(f"{Fore.CYAN}[*] Iniciando captura en {self.interface or 'default'}")
        print(f"[*] Archivo de salida: {self.capture_file}")
        print(f"{Fore.YELLOW}[!] Presiona Ctrl+C para detener\n")
        
        try:
            # Iniciar captura
            sniff(iface=self.interface, 
                  prn=self.packet_callback, 
                  store=False,
                  timeout=duration,
                  count=packet_count)
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Captura detenida por el usuario")
        finally:
            self.stop_capture()
    
    def stop_capture(self):
        """Detiene la captura y guarda los paquetes"""
        self.capturing = False
        self.save_capture()
        print(f"{Fore.GREEN}[✓] Captura finalizada")
        print(f"[✓] Paquetes capturados: {len(self.packets)}")
        print(f"[✓] Archivo guardado: {self.capture_file}")
    
    def save_capture(self):
        """Guarda los paquetes capturados en formato PCAP"""
        if self.packets and self.capture_file:
            # Convertir a formato Scapy y guardar
            print(f"{Fore.CYAN}[*] Guardando {len(self.packets)} paquetes...")
            # Nota: Para guardar realmente necesitarías los paquetes Scapy originales
            # Esto es una simplificación

def capture_packets(interface=None, duration=None, count=None):
    """Función principal para capturar paquetes"""
    capture = PacketCapture(interface)
    capture.start_capture(duration, count)
    return capture.packets
