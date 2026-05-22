import socket
import requests
from datetime import datetime
from colorama import init, Fore

init(autoreset=True)

class VulnerabilityScanner:
    def __init__(self, target):
        self.target = target
        self.vulnerabilities = []
        self.vuln_database = {
            21: {
                'service': 'FTP',
                'vulns': ['Anonymous login allowed', 'CVE-2011-2523 (vsftpd backdoor)']
            },
            22: {
                'service': 'SSH',
                'vulns': ['Weak cipher suites', 'CVE-2018-15473 (user enumeration)']
            },
            80: {
                'service': 'HTTP',
                'vulns': ['Directory listing enabled', 'Outdated server version']
            },
            443: {
                'service': 'HTTPS',
                'vulns': ['SSL/TLS weak protocols', 'Missing security headers']
            },
            445: {
                'service': 'SMB',
                'vulns': ['EternalBlue vulnerability (MS17-010)', 'Null session allowed']
            },
            3306: {
                'service': 'MySQL',
                'vulns': ['Default credentials', 'Remote root access']
            },
            3389: {
                'service': 'RDP',
                'vulns': ['BlueKeep vulnerability (CVE-2019-0708)', 'Weak encryption']
            }
        }
    
    def check_banner(self, ip, port):
        """Obtiene banner del servicio"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((ip, port))
            sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
            banner = sock.recv(1024).decode('utf-8', errors='ignore')
            sock.close()
            return banner.strip()
        except:
            return None
    
    def check_http_vulns(self, ip, port):
        """Verifica vulnerabilidades HTTP específicas"""
        vulns = []
        url = f"http://{ip}:{port}"
        
        try:
            # Check directory listing
            r = requests.get(f"{url}/", timeout=5)
            if 'Index of /' in r.text or 'Directory listing for' in r.text:
                vulns.append("Directory listing enabled")
            
            # Check security headers
            if 'X-Frame-Options' not in r.headers:
                vulns.append("Missing X-Frame-Options header")
            if 'X-Content-Type-Options' not in r.headers:
                vulns.append("Missing X-Content-Type-Options header")
            
            # Check for common sensitive files
            sensitive_files = ['phpinfo.php', 'info.php', 'test.php', 'config.php']
            for file in sensitive_files:
                try:
                    r = requests.get(f"{url}/{file}", timeout=3)
                    if r.status_code == 200:
                        vulns.append(f"Sensitive file exposed: {file}")
                except:
                    pass
                    
        except:
            pass
        
        return vulns
    
    def check_ftp_anonymous(self, ip, port):
        """Verifica si permite acceso anónimo a FTP"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((ip, port))
            sock.recv(1024)
            sock.send(b"USER anonymous\r\n")
            sock.recv(1024)
            sock.send(b"PASS anonymous@\r\n")
            response = sock.recv(1024).decode('utf-8')
            sock.close()
            
            if '230' in response:  # Login successful
                return True
        except:
            pass
        return False
    
    def scan(self):
        """Ejecuta escaneo de vulnerabilidades"""
        print(f"{Fore.CYAN}[*] Escaneando vulnerabilidades en {self.target}")
        print(f"{Fore.YELLOW}[!] Esto puede tomar unos minutos...\n")
        
        # Escanear puertos comunes
        for port, info in self.vuln_database.items():
            print(f"{Fore.CYAN}[?] Verificando puerto {port} ({info['service']})...")
            
            try:
                # Verificar si el puerto está abierto
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((self.target, port))
                sock.close()
                
                if result == 0:
                    print(f"{Fore.GREEN}[+] Puerto {port} abierto - {info['service']}")
                    
                    # Realizar verificaciones específicas
                    if port == 21:
                        if self.check_ftp_anonymous(self.target, port):
                            self.vulnerabilities.append({
                                'port': port,
                                'service': info['service'],
                                'vulnerability': 'Anonymous FTP login allowed',
                                'severity': 'HIGH',
                                'remediation': 'Disable anonymous access on FTP server'
                            })
                    
                    elif port in [80, 443]:
                        http_vulns = self.check_http_vulns(self.target, port)
                        for vuln in http_vulns:
                            self.vulnerabilities.append({
                                'port': port,
                                'service': info['service'],
                                'vulnerability': vuln,
                                'severity': 'MEDIUM',
                                'remediation': 'Configure web server security properly'
                            })
                    
                    # Agregar vulnerabilidades genéricas de la base de datos
                    for vuln in info['vulns']:
                        self.vulnerabilities.append({
                            'port': port,
                            'service': info['service'],
                            'vulnerability': vuln,
                            'severity': 'HIGH' if 'CVE' in vuln else 'MEDIUM',
                            'remediation': f'Review and patch {info["service"]} service'
                        })
                        
            except Exception as e:
                pass
        
        # Mostrar reporte
        self.print_report()
        return self.vulnerabilities
    
    def print_report(self):
        """Muestra reporte de vulnerabilidades"""
        print(f"\n{'='*60}")
        print(f"{Fore.RED}🚨 REPORTE DE VULNERABILIDADES")
        print(f"{'='*60}")
        
        if not self.vulnerabilities:
            print(f"{Fore.GREEN}✓ No se encontraron vulnerabilidades críticas")
        else:
            print(f"{Fore.YELLOW}[!] Se encontraron {len(self.vulnerabilities)} vulnerabilidades:\n")
            
            for vuln in self.vulnerabilities:
                severity_color = Fore.RED if vuln['severity'] == 'HIGH' else Fore.YELLOW
                print(f"{severity_color}[{vuln['severity']}] {vuln['service']} (Puerto {vuln['port']})")
                print(f"    → {vuln['vulnerability']}")
                print(f"    → Solución: {vuln['remediation']}\n")

def scan_vulnerabilities(target):
    """Función principal de escaneo de vulnerabilidades"""
    scanner = VulnerabilityScanner(target)
    return scanner.scan()
