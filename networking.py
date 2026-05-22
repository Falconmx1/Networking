#!/usr/bin/env python3
"""
Networking Tool - Main CLI
"""
import argparse
import sys
from src.scanner import scan_ports
from src.ids import detect_intrusions

def main():
    parser = argparse.ArgumentParser(description="Networking - Security & Monitoring Tool")
    parser.add_argument("--scan", help="Escanear puertos a una IP (ej: 192.168.1.1)")
    parser.add_argument("-p", "--ports", default="1-1000", help="Rango de puertos (ej: 22,80 o 1-1000)")
    parser.add_argument("--ids", action="store_true", help="Activar detección de intrusos")
    parser.add_argument("--interface", default="eth0", help="Interfaz de red (Linux: eth0, Windows: 'Wi-Fi' o 'Ethernet')")
    
    args = parser.parse_args()
    
    if args.scan:
        print(f"[*] Escaneando {args.scan} en puertos {args.ports}")
        scan_ports(args.scan, args.ports)
    elif args.ids:
        print(f"[*] Iniciando IDS en {args.interface}")
        detect_intrusions(args.interface)
    else:
        print("Uso: networking --scan 192.168.1.1 -p 1-1000")
        print("      networking --ids --interface eth0")

if __name__ == "__main__":
    main()
