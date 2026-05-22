from flask import Flask, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from datetime import timedelta
import psutil
import json
import os
from src.scanner import scan_ports
from src.ids import detect_intrusions
from src.vuln_scanner import scan_vulnerabilities

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'networking-jwt-secret-change-this'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

jwt = JWTManager(app)

# Datos de usuarios (en producción usar base de datos)
users = {
    'admin': 'networking2025',
    'falconmx1': 'securepass123'
}

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Autenticación para app móvil"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username in users and users[username] == password:
        access_token = create_access_token(identity=username)
        return jsonify({
            'success': True,
            'access_token': access_token,
            'username': username
        })
    else:
        return jsonify({'success': False, 'message': 'Credenciales inválidas'}), 401

@app.route('/api/scan', methods=['POST'])
@jwt_required()
def api_scan():
    """Endpoint para escaneo de puertos"""
    data = request.get_json()
    target = data.get('target')
    ports = data.get('ports', '1-1000')
    stealth = data.get('stealth', False)
    
    if not target:
        return jsonify({'error': 'Target requerido'}), 400
    
    open_ports = scan_ports(target, ports, threads=100, stealth=stealth)
    
    return jsonify({
        'target': target,
        'open_ports': open_ports,
        'count': len(open_ports),
        'stealth_mode': stealth
    })

@app.route('/api/vulnerabilities', methods=['POST'])
@jwt_required()
def api_vulnerabilities():
    """Endpoint para escaneo de vulnerabilidades"""
    data = request.get_json()
    target = data.get('target')
    
    if not target:
        return jsonify({'error': 'Target requerido'}), 400
    
    vulns = scan_vulnerabilities(target)
    
    return jsonify({
        'target': target,
        'vulnerabilities': vulns,
        'total': len(vulns)
    })

@app.route('/api/network/stats', methods=['GET'])
@jwt_required()
def api_network_stats():
    """Obtener estadísticas de red"""
    net_io = psutil.net_io_counters()
    connections = []
    
    for conn in psutil.net_connections(kind='inet'):
        if conn.status == 'ESTABLISHED':
            connections.append({
                'local': f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else None,
                'remote': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
                'status': conn.status
            })
    
    return jsonify({
        'bytes_sent': net_io.bytes_sent,
        'bytes_recv': net_io.bytes_recv,
        'active_connections': len(connections),
        'connections': connections[:20],
        'system': {
            'cpu': psutil.cpu_percent(),
            'ram': psutil.virtual_memory().percent
        }
    })

@app.route('/api/system/info', methods=['GET'])
@jwt_required()
def api_system_info():
    """Información del sistema"""
    return jsonify({
        'hostname': os.uname().nodename if hasattr(os, 'uname') else 'Unknown',
        'platform': psutil.PLATFORM,
        'cpu_cores': psutil.cpu_count(),
        'total_ram': psutil.virtual_memory().total,
        'disk_usage': psutil.disk_usage('/').percent
    })

def start_api_server(host='0.0.0.0', port=5001):
    """Inicia el servidor API para la app móvil"""
    print(f"\n📱 API Server iniciado en http://{host}:{port}")
    print(f"🔑 Endpoints disponibles:")
    print(f"   POST /api/auth/login")
    print(f"   POST /api/scan")
    print(f"   POST /api/vulnerabilities")
    print(f"   GET  /api/network/stats")
    print(f"   GET  /api/system/info\n")
    
    app.run(host=host, port=port, debug=False, threaded=True)
