import socket
import sys

def scan_port(ip, port):
    """Intenta conectar a un puerto específico"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except:
        return False

def parse_ports(port_range):
    """Convierte '22,80,1-100' en lista de puertos"""
    ports = set()
    for part in port_range.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            ports.update(range(start, end+1))
        else:
            ports.add(int(part))
    return sorted(ports)

def scan_ports(target, port_range):
    print(f"\n[+] Escaneando {target}...\n")
    open_ports = []
    ports = parse_ports(port_range)
    
    for port in ports:
        if scan_port(target, port):
            print(f"  Puerto {port}: ABIERTO")
            open_ports.append(port)
    
    print(f"\n[+] Escaneo completado. Puertos abiertos: {len(open_ports)}")
    return open_ports
