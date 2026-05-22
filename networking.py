#!/usr/bin/env python3
"""
Networking Tool - Professional Security Suite v3.0
"""
import argparse
import sys
import threading
from src.utils import print_banner, get_platform
from src.scanner import scan_ports
from src.ids import detect_intrusions
from src.vuln_scanner import scan_vulnerabilities
from src.packet_capture import capture_packets
from src.dashboard import start_dashboard
from src.api import start_api_server

def main():
    print_banner()
    
    parser = argparse.ArgumentParser(
        description="Networking Tool v3.0 - Suite profesional de seguridad",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Escaneo
    parser.add_argument("--scan", help="Escaneo de puertos a IP/dominio")
    parser.add_argument("-p", "--ports", default="1-1000", help="Rango de puertos")
    parser.add_argument("--threads", type=int, default=200, help="Hilos para escaneo")
    parser.add_argument("--stealth", action="store_true", help="Modo sigiloso")
    
    # IDS
    parser.add_argument("--ids", action="store_true", help="Detección de intrusos")
    parser.add_argument("--interface", default="eth0", help="Interfaz de red")
    
    # Vulnerabilidades
    parser.add_argument("--vuln", help="Escaneo de vulnerabilidades a IP/dominio")
    
    # Captura de paquetes
    parser.add_argument("--capture", action="store_true", help="Capturar paquetes")
    parser.add_argument("--duration", type=int, help="Duración en segundos")
    parser.add_argument("--packets", type=int, help="Número de paquetes a capturar")
    
    # Dashboard y API
    parser.add_argument("--dashboard", action="store_true", help="Iniciar dashboard web")
    parser.add_argument("--api", action="store_true", help="Iniciar API para app móvil")
    parser.add_argument("--port", type=int, default=5000, help="Puerto del servidor")
    
    args = parser.parse_args()
    
    # Dashboard web
    if args.dashboard:
        start_dashboard(host='0.0.0.0', port=args.port)
        return
    
    # API server
    if args.api:
        start_api_server(host='0.0.0.0', port=args.port + 1)
        return
    
    # Escaneo de puertos
    if args.scan:
        open_ports = scan_ports(args.scan, args.ports, args.threads, args.stealth)
        print(f"\n✅ Puertos abiertos: {open_ports}")
    
    # Detección de intrusos
    if args.ids:
        alerts = detect_intrusions(args.interface)
    
    # Escaneo de vulnerabilidades
    if args.vuln:
        vulns = scan_vulnerabilities(args.vuln)
    
    # Captura de paquetes
    if args.capture:
        capture_packets(args.interface, args.duration, args.packets)
    
    if not (args.scan or args.ids or args.vuln or args.capture or args.dashboard or args.api):
        parser.print_help()

if __name__ == "__main__":
    main()
