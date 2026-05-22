import json
import time
from datetime import datetime
import os

def generate_html_report(scan_data, alerts_data, filename="report.html"):
    """Genera reporte HTML profesional"""
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    html_template = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Networking Tool - Reporte de Seguridad</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
                color: #333;
            }}
            
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 15px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                overflow: hidden;
            }}
            
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }}
            
            .header h1 {{
                font-size: 2.5em;
                margin-bottom: 10px;
            }}
            
            .header p {{
                font-size: 1.1em;
                opacity: 0.9;
            }}
            
            .content {{
                padding: 30px;
            }}
            
            .section {{
                margin-bottom: 40px;
            }}
            
            .section h2 {{
                color: #667eea;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 3px solid #667eea;
            }}
            
            .stats {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }}
            
            .stat-card {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
            }}
            
            .stat-card h3 {{
                font-size: 2em;
                margin-bottom: 10px;
            }}
            
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            
            th, td {{
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }}
            
            th {{
                background: #667eea;
                color: white;
            }}
            
            tr:hover {{
                background: #f5f5f5;
            }}
            
            .alert-critical {{
                background: #fee;
                color: #c00;
                font-weight: bold;
            }}
            
            .alert-warning {{
                background: #ffeaa7;
                color: #d63031;
            }}
            
            .footer {{
                background: #f8f9fa;
                padding: 20px;
                text-align: center;
                color: #666;
            }}
            
            .badge {{
                display: inline-block;
                padding: 3px 8px;
                border-radius: 5px;
                font-size: 0.9em;
            }}
            
            .badge-open {{
                background: #00b894;
                color: white;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌐 Networking Tool</h1>
                <p>Reporte de Seguridad de Red</p>
                <p><small>Generado: {timestamp}</small></p>
            </div>
            
            <div class="content">
                <div class="stats">
                    <div class="stat-card">
                        <h3>{len(scan_data.get('open_ports', []))}</h3>
                        <p>Puertos Abiertos</p>
                    </div>
                    <div class="stat-card">
                        <h3>{len(alerts_data)}</h3>
                        <p>Alertas de Seguridad</p>
                    </div>
                    <div class="stat-card">
                        <h3>{scan_data.get('target', 'N/A')}</h3>
                        <p>Target Escaneado</p>
                    </div>
                </div>
                
                <div class="section">
                    <h2>🔌 Puertos Abiertos Detectados</h2>
                    {'<table>' + ''.join([f'''
                        <tr>
                            <td><strong>Puerto {p}</strong></td>
                            <td>{scan_data.get('services', {{}}).get(p, 'Unknown')}</td>
                            <td><span class="badge badge-open">ABIERTO</span></td>
                        </tr>
                    ''' for p in scan_data.get('open_ports', [])]) + '</table>' if scan_data.get('open_ports') else '<p>No se encontraron puertos abiertos</p>'}
                </div>
                
                <div class="section">
                    <h2>🚨 Alertas de Intrusos</h2>
                    {'<table>' + ''.join([f'''
                        <tr class="{'alert-critical' if alert.get('type') == 'ARP Spoofing' else 'alert-warning'}">
                            <td><strong>{alert.get('type', 'Unknown')}</strong></td>
                            <td>IP: {alert.get('ip', 'N/A')}</td>
                            <td>{alert.get('details', '')}</td>
                        </tr>
                    ''' for alert in alerts_data]) + '</table>' if alerts_data else '<p>✓ No se detectaron intrusiones</p>'}
                </div>
            </div>
            
            <div class="footer">
                <p>Networking Tool - Herramienta Profesional de Seguridad</p>
                <p>© 2025 - Reporte generado automáticamente</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print(f"[✓] Reporte HTML generado: {filename}")
    return filename
