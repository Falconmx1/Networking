from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
import threading
import json
import time
import os
from datetime import datetime
import psutil

app = Flask(__name__, static_folder='web', template_folder='web')
app.config['SECRET_KEY'] = 'networking-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

# Datos en tiempo real
network_stats = {
    'bytes_sent': 0,
    'bytes_recv': 0,
    'packets_sent': 0,
    'packets_recv': 0,
    'connections': [],
    'alerts': []
}

def get_network_io():
    """Obtiene estadísticas de red"""
    net_io = psutil.net_io_counters()
    return {
        'bytes_sent': net_io.bytes_sent,
        'bytes_recv': net_io.bytes_recv,
        'packets_sent': net_io.packets_sent,
        'packets_recv': net_io.packets_recv,
        'errin': net_io.errin,
        'errout': net_io.errout,
        'dropin': net_io.dropin,
        'dropout': net_io.dropout
    }

def get_connections():
    """Obtiene conexiones activas"""
    connections = []
    for conn in psutil.net_connections(kind='inet'):
        if conn.status == 'ESTABLISHED':
            connections.append({
                'local_ip': f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else 'N/A',
                'remote_ip': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else 'N/A',
                'status': conn.status,
                'pid': conn.pid
            })
    return connections

def background_monitor():
    """Hilo de monitoreo en segundo plano"""
    while True:
        try:
            # Enviar estadísticas de red
            io_stats = get_network_io()
            socketio.emit('network_stats', io_stats)
            
            # Enviar conexiones activas
            connections = get_connections()
            socketio.emit('connections', connections[:50])  # Top 50
            
            # Enviar uso de CPU/RAM
            socketio.emit('system_stats', {
                'cpu': psutil.cpu_percent(),
                'ram': psutil.virtual_memory().percent,
                'timestamp': datetime.now().isoformat()
            })
            
            time.sleep(2)  # Actualizar cada 2 segundos
        except Exception as e:
            print(f"Error en monitor: {e}")
            time.sleep(5)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stats')
def api_stats():
    return {
        'network': get_network_io(),
        'connections': get_connections()[:20],
        'system': {
            'cpu': psutil.cpu_percent(),
            'ram': psutil.virtual_memory().percent
        }
    }

@socketio.on('connect')
def handle_connect():
    print('Cliente conectado al dashboard')
    emit('connected', {'message': 'Conectado a Networking Dashboard'})

def start_dashboard(host='0.0.0.0', port=5000):
    """Inicia el dashboard web"""
    print(f"\n🌐 Dashboard web iniciado en http://{host}:{port}")
    print(f"📊 Monitoreo en tiempo real activo\n")
    
    # Iniciar hilo de monitoreo
    monitor_thread = threading.Thread(target=background_monitor, daemon=True)
    monitor_thread.start()
    
    # Ejecutar servidor
    socketio.run(app, host=host, port=port, debug=False, allow_unsafe_werkzeug=True)
