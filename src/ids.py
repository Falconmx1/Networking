import socket
import struct
import time
import sys

# Solo funciona en Linux (por raw socket) - en Windows requeriría Npcap
def detect_intrusions(interface):
    """Detecta conexiones sospechosas (escucha raw)"""
    print(f"[!] Modo IDS activado en {interface}")
    print("[!] Detectando conexiones nuevas...")
    
    try:
        # RAW socket (requiere root)
        sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
        sock.bind((interface, 0))
    except:
        print("[!] Modo IDS solo funciona en Linux con permisos root (sudo)")
        print("[!] En Windows, usa Wireshark + Npcap o implementa con scapy")
        return
    
    connections = {}
    print("[*] Monitoreando (Ctrl+C para detener)...")
    
    try:
        while True:
            packet, addr = sock.recvfrom(65535)
            # Extraer IPs (formato Ethernet + IP)
            if len(packet) > 34:
                # IP src offset 26, dst offset 30
                src_ip = socket.inet_ntoa(packet[26:30])
                dst_ip = socket.inet_ntoa(packet[30:34])
                conn_key = f"{src_ip} -> {dst_ip}"
                
                if conn_key not in connections:
                    connections[conn_key] = time.time()
                    print(f"[ALERTA] Nueva conexión: {conn_key}")
                elif time.time() - connections[conn_key] > 60:
                    del connections[conn_key]
    except KeyboardInterrupt:
        print("\n[+] IDS detenido")
