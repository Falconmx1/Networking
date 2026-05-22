import socket
import threading
from queue import Queue
from colorama import init, Fore, Style
from .utils import random_delay, stealth_mode_enabled

init(autoreset=True)

class PortScanner:
    def __init__(self, target, ports, threads=100, stealth=False):
        self.target = target
        self.ports = ports
        self.threads = threads
        self.stealth = stealth
        self.open_ports = []
        self.queue = Queue()
        self.lock = threading.Lock()
        
    def scan_port(self, port):
        """Escanea un puerto individual con opción sigilosa"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            
            if self.stealth:
                random_delay(0.05, 0.2)  # Retraso aleatorio
                
            result = sock.connect_ex((self.target, port))
            sock.close()
            
            if result == 0:
                service = self.get_service_name(port)
                with self.lock:
                    self.open_ports.append(port)
                    print(f" {Fore.GREEN}[+] Puerto {port} ({service}) - ABIERTO")
                    
        except Exception as e:
            pass
    
    def get_service_name(self, port):
        """Obtiene nombre del servicio común"""
        services = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
            53: "DNS", 80: "HTTP", 110: "POP3", 111: "RPC",
            135: "RPC", 139: "NetBIOS", 143: "IMAP", 443: "HTTPS",
            445: "SMB", 993: "IMAPS", 995: "POP3S", 3306: "MySQL",
            3389: "RDP", 5432: "PostgreSQL", 5900: "VNC", 8080: "HTTP-Alt"
        }
        return services.get(port, "Unknown")
    
    def worker(self):
        """Hilo trabajador para escaneo"""
        while not self.queue.empty():
            port = self.queue.get()
            self.scan_port(port)
            self.queue.task_done()
    
    def scan(self):
        """Ejecuta escaneo multithreading"""
        print(f"\n{Fore.CYAN}[*] Escaneando {self.target}")
        print(f"[*] Puertos: {self.ports[0]}-{self.ports[-1]}")
        print(f"[*] Hilos: {self.threads}")
        if self.stealth:
            print(f"{Fore.YELLOW}[!] MODO SIGILOSO ACTIVADO (retrasos aleatorios)")
        print("-" * 50)
        
        # Llenar queue
        for port in self.ports:
            self.queue.put(port)
        
        # Crear y iniciar hilos
        threads = []
        for _ in range(self.threads):
            t = threading.Thread(target=self.worker)
            t.start()
            threads.append(t)
        
        # Esperar a que terminen
        for t in threads:
            t.join()
        
        return self.open_ports

def scan_ports(target, port_range, threads=100, stealth=False):
    """Función principal de escaneo"""
    # Parsear rango de puertos
    ports = []
    if '-' in port_range:
        start, end = map(int, port_range.split('-'))
        ports = list(range(start, end+1))
    else:
        ports = [int(p) for p in port_range.split(',')]
    
    scanner = PortScanner(target, ports, threads, stealth)
    open_ports = scanner.scan()
    
    print("-" * 50)
    print(f"\n{Fore.GREEN}[✓] Escaneo completado")
    print(f"[✓] Puertos abiertos encontrados: {len(open_ports)}")
    
    return open_ports
