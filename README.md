# 🌐 Networking Tool

**Networking** es una herramienta de seguridad y monitoreo de red diseñada para **detectar intrusos**, **escaneo de puertos**, **análisis de tráfico** y más. Funciona tanto en **Windows** como en **Linux**.

---

## 🚀 Características

- 🕵️‍♂️ **Detección de intrusos** (análisis de conexiones sospechosas)
- 🔌 **Escaneo de puertos** (TCP/UDP)
- 📡 **Monitor de tráfico en tiempo real**
- 🧠 **Detección de ARP spoofing** (en Linux)
- 🧾 **Generación de reportes** (HTML/JSON/TXT)
- 🛡️ **Modo sigiloso** (detección pasiva)

---

## 🖥️ Compatibilidad

| Sistema | Soporte |
|---------|---------|
| Linux   | ✅ Completo |
| Windows | ✅ Completo (requiere Npcap o WinPcap) |

---

## 📦 Instalación

### Linux
```bash
git clone https://github.com/Falconmx1/Networking.git
cd Networking
sudo python3 setup.py install

🚀 Comandos finales para usar TODO

# Instalar todo
pip install -r requirements.txt

# Iniciar dashboard web (http://localhost:5000)
python networking.py --dashboard --port 5000

# Iniciar API para app móvil (http://localhost:5001)
python networking.py --api --port 5001

# Escaneo completo con todo
sudo python networking.py --scan 192.168.1.1 -p 1-1000 --stealth --vuln 192.168.1.1 --ids --capture

# Generar reporte HTML
python networking.py --scan 8.8.8.8 -p 80,443 --report

# Captura de paquetes por 60 segundos
sudo python networking.py --capture --interface eth0 --duration 60
