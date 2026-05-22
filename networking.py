#!/usr/bin/env python3
"""
Networking Tool - Professional Security Suite
"""
import argparse
import sys
import os
from src.scanner import scan_ports
from src.ids import detect_intrusions
from src.report import generate_html_report
from src.utils import print_banner, get_platform

def main():
    print_banner()
    
    parser = argparse.ArgumentParser(
        description="Networking Tool - Escaneo de puertos, detección de intrusos y monitoreo de red",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  networking --scan 192.168.1.1 -p 1-1000
  networking --scan 192.168.1.1 -p 22,80,443 --stealth --threads 200
  networking --ids --interface eth0
  networking --scan 8.8.8.8 -p 1-1000 --report
        """
    )
    
    # Escaneo de puertos
    parser.add_argument("--scan", help="Dirección IP o dominio a escanear")
    parser.add_argument("-p", "--ports", default="1-1000", help="Rango de puertos (ej: 22,80 o 1-1000)")
    parser.add_argument("--threads", type=int, default=100, help="Número de hilos para escaneo (default: 100)")
    parser.add_argument("--stealth", action="store_true", help="Modo sigiloso con retrasos aleatorios")
    
    # Detección de intrusos
    parser.add_argument("--ids", action="store_true", help="Activar detección de intrusos (ARP spoofing)")
    parser.add_argument("--interface", default="eth0", help="Interfaz de red para monitoreo")
    
    # Reportes
    parser.add_argument("--report", action="store_true", help="Generar reporte HTML")
    parser.add_argument("--output", default="report.html", help="Nombre del archivo de reporte")
    
    args = parser.parse_args()
    
    scan_results = {}
    alerts_results = []
    
    # Ejecutar escaneo si se solicita
    if args.scan:
        print(f"\n[+] Iniciando escaneo contra: {args.scan}")
        open_ports = scan_ports(args.scan, args.ports, args.threads, args.stealth)
        scan_results = {
            'target': args.scan,
            'open_ports': open_ports,
            'services': {p: scan_ports.__code__ for p in open_ports}  # Simplificado
        }
    
    # Ejecutar IDS si se solicita
    if args.ids:
        print(f"\n[+] Iniciando detección de intrusos en {args.interface}")
        alerts_results = detect_intrusions(args.interface)
    
    # Generar reporte
    if args.report and (scan_results or alerts_results):
        report_file = generate_html_report(scan_results, alerts_results, args.output)
        print(f"\n[✓] Reporte guardado: {report_file}")
        
        # Intentar abrir en navegador
        if get_platform() == "Windows":
            os.system(f"start {report_file}")
        elif get_platform() == "Linux":
            os.system(f"xdg-open {report_file}")
    
    if not (args.scan or args.ids):
        parser.print_help()

if __name__ == "__main__":
    # Verificar permisos en Linux para IDS
    if get_platform() == "Linux" and os.geteuid() != 0:
        print("[!] Para detección de intrusos en Linux necesitas permisos root (sudo)")
    
    main()
