#!/usr/bin/env python3
"""
QUANTUM-HIJACK PROJECT
Herramienta de Hacking Ético 2026 - Emmanuel
SOLO para testing autorizado y educación
"""

import os
import sys
import subprocess
import time
import json
import socket
from datetime import datetime
from flask import Flask, render_template, jsonify, request, send_from_directory
from scapy.all import ARP, Ether, get_if_hwaddr, conf
import logging

# Configuración
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['JSON_SORT_KEYS'] = False

# Database para dispositivos infectados
INFECTED_DB = 'infected_devices.json'
LOGS_DB = 'operation_logs.json'

def load_infected_devices():
    """Cargar dispositivos infectados desde archivo"""
    if os.path.exists(INFECTED_DB):
        try:
            with open(INFECTED_DB, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_infected_devices(devices):
    """Guardar dispositivos infectados"""
    try:
        with open(INFECTED_DB, 'w') as f:
            json.dump(devices, f, indent=2)
        return True
    except Exception as e:
        logger.error(f"Error guardando dispositivos: {e}")
        return False

def add_log(action, details=""):
    """Agregar entrada al log de operaciones"""
    try:
        logs = []
        if os.path.exists(LOGS_DB):
            with open(LOGS_DB, 'r') as f:
                logs = json.load(f)
        
        logs.append({
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'details': details
        })
        
        with open(LOGS_DB, 'w') as f:
            json.dump(logs[-100:], f, indent=2)  # Guardar últimas 100 entradas
    except Exception as e:
        logger.error(f"Error guardando log: {e}")

# Variables globales
INFECTED_DEVICES = load_infected_devices()

ATTACKS = {
    'arp_spoofing': False,
    'dns_spoofing': False,
    'packet_sniff': False,
    'deauth': False
}

STATS = {
    'packets_captured': 0,
    'credentials_found': 0,
    'connected_devices': 0,
    'start_time': datetime.now().isoformat()
}

class QuantumHijack:
    """Clase principal para operaciones de hacking ético"""
    
    def __init__(self):
        self.running = False
        self.target_ip = None
        self.gateway_ip = None
        self.attacker_mac = None
        self.monitor_interface = None
        self.original_interface = None
        self.original_mode = "managed"
        
    def check_root(self):
        """Verificar si se ejecuta como root (requerido en Linux)"""
        if os.name == 'posix' and os.geteuid() != 0:
            logger.error("❌ Este programa debe ejecutarse como root (sudo)")
            return False
        return True
    
    def run_command(self, command, capture_output=True):
        """Ejecutar comando del sistema"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=capture_output,
                text=True,
                timeout=10
            )
            return result.returncode == 0, result.stdout, result.stderr
        except Exception as e:
            logger.error(f"Error ejecutando comando: {e}")
            return False, "", str(e)
    
    def get_wireless_interfaces(self):
        """Detectar interfaces wireless disponibles"""
        interfaces = []
        try:
            logger.info("🔍 Detectando interfaces wireless...")
            
            # Método 1: iwconfig
            success, output, _ = self.run_command("iwconfig 2>/dev/null")
            if success and output:
                for line in output.split('\n'):
                    if 'IEEE 802.11' in line or 'ESSID' in line:
                        iface = line.split()[0]
                        if iface and iface not in interfaces:
                            interfaces.append(iface)
            
            # Método 2: iw dev (más moderno)
            success, output, _ = self.run_command("iw dev")
            if success and output:
                for line in output.split('\n'):
                    if 'Interface' in line:
                        iface = line.split()[-1]
                        if iface and iface not in interfaces:
                            interfaces.append(iface)
            
            logger.info(f"✅ Interfaces encontradas: {interfaces if interfaces else 'Ninguna'}")
            return interfaces
        except Exception as e:
            logger.error(f"Error detectando interfaces: {e}")
            return []
    
    def set_monitor_mode(self, interface=None):
        """Activar modo monitor en la interfaz wireless"""
        try:
            # Si no se especifica, detectar automáticamente
            if not interface:
                interfaces = self.get_wireless_interfaces()
                if not interfaces:
                    logger.error("❌ No se encontraron interfaces wireless")
                    return False
                interface = interfaces[0]
            
            self.original_interface = interface
            logger.info(f"🔧 Configurando {interface} en modo monitor...")
            
            # Paso 1: Matar procesos que puedan interferir
            logger.info("   → Deteniendo procesos interferentes...")
            self.run_command("airmon-ng check kill", capture_output=False)
            time.sleep(1)
            
            # Paso 2: Bajar la interfaz
            logger.info(f"   → Bajando interfaz {interface}...")
            self.run_command(f"ip link set {interface} down")
            time.sleep(0.5)
            
            # Paso 3: Activar modo monitor
            logger.info(f"   → Activando modo monitor...")
            success, output, error = self.run_command(f"iwconfig {interface} mode monitor")
            if not success:
                logger.warning(f"   ⚠️  iwconfig falló, intentando con iw...")
                self.run_command(f"iw {interface} set monitor control")
            
            time.sleep(0.5)
            
            # Paso 4: Levantar la interfaz
            logger.info(f"   → Levantando interfaz...")
            self.run_command(f"ip link set {interface} up")
            time.sleep(1)
            
            # Verificar modo monitor
            success, output, _ = self.run_command(f"iwconfig {interface}")
            if "Mode:Monitor" in output or "monitor" in output.lower():
                self.monitor_interface = interface
                logger.info(f"✅ Modo monitor activado en {interface}")
                
                # Configurar canal
                logger.info("   → Configurando canal 6...")
                self.run_command(f"iwconfig {interface} channel 6")
                
                return True
            else:
                logger.error(f"❌ No se pudo activar modo monitor en {interface}")
                return False
                
        except Exception as e:
            logger.error(f"Error activando modo monitor: {e}")
            return False
    
    def restore_managed_mode(self):
        """Restaurar modo managed (normal) en la interfaz"""
        if not self.original_interface:
            return
        
        try:
            interface = self.original_interface
            logger.info(f"🔄 Restaurando {interface} a modo managed...")
            
            # Bajar interfaz
            self.run_command(f"ip link set {interface} down")
            time.sleep(0.5)
            
            # Volver a modo managed
            self.run_command(f"iwconfig {interface} mode managed")
            time.sleep(0.5)
            
            # Levantar interfaz
            self.run_command(f"ip link set {interface} up")
            time.sleep(0.5)
            
            # Reiniciar NetworkManager
            logger.info("   → Reiniciando NetworkManager...")
            self.run_command("systemctl restart NetworkManager")
            
            logger.info(f"✅ {interface} restaurado a modo managed")
            
        except Exception as e:
            logger.error(f"Error restaurando modo managed: {e}")
    
    def get_local_ip(self):
        """Obtener IP local"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception as e:
            logger.error(f"Error obteniendo IP local: {e}")
            return "127.0.0.1"
    
    def scan_network(self, network_range="192.168.1.0/24"):
        """Escanear red para descubrir dispositivos"""
        devices = []
        try:
            logger.info(f"🔍 Escaneando red {network_range}...")
            arp_request = ARP(pdst=network_range)
            broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
            arp_request_broadcast = broadcast/arp_request
            
            answered_list = conf.iface.send_recv(
                arp_request_broadcast, 
                timeout=2, 
                verbose=False
            )[0]
            
            for element in answered_list:
                device_dict = {
                    "ip": element[1].psrc,
                    "mac": element[1].hwsrc,
                    "timestamp": datetime.now().isoformat()
                }
                devices.append(device_dict)
                STATS['connected_devices'] = len(devices)
            
            logger.info(f"✅ {len(devices)} dispositivos encontrados")
            return devices
        except Exception as e:
            logger.error(f"Error escaneando red: {e}")
            return []
    
    def start_sniffer(self):
        """Iniciar captura de paquetes"""
        ATTACKS['packet_sniff'] = True
        logger.info("🔴 Captura de paquetes iniciada")
        STATS['packets_captured'] = 0
    
    def stop_sniffer(self):
        """Detener captura de paquetes"""
        ATTACKS['packet_sniff'] = False
        logger.info("🛑 Captura de paquetes detenida")
    
    def get_status(self):
        """Obtener estado actual"""
        return {
            "status": "running" if self.running else "stopped",
            "monitor_interface": self.monitor_interface,
            "monitor_mode_active": self.monitor_interface is not None,
            "attacks": ATTACKS,
            "stats": STATS,
            "local_ip": self.get_local_ip()
        }

# Instancia global
hijack = QuantumHijack()

# ========================
# RUTAS FLASK
# ========================

@app.route('/')
def dashboard():
    """Dashboard principal"""
    return jsonify({
        "app": "QUANTUM-HIJACK",
        "version": "2026.1",
        "status": "running",
        "message": "Accede a /api/status para más información"
    })

@app.route('/api/status')
def api_status():
    """API: Estado actual del sistema"""
    return jsonify(hijack.get_status())

@app.route('/api/scan', methods=['POST'])
def api_scan():
    """API: Escanear red"""
    try:
        network = request.json.get('network', '192.168.1.0/24')
        devices = hijack.scan_network(network)
        return jsonify({
            "success": True,
            "devices_found": len(devices),
            "devices": devices
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/attacks/start', methods=['POST'])
def api_start_attack():
    """API: Iniciar ataque"""
    try:
        attack_type = request.json.get('type', 'packet_sniff')
        if attack_type in ATTACKS:
            if attack_type == 'packet_sniff':
                hijack.start_sniffer()
            ATTACKS[attack_type] = True
            return jsonify({"success": True, "message": f"Ataque {attack_type} iniciado"})
        return jsonify({"success": False, "error": "Tipo de ataque inválido"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/attacks/stop', methods=['POST'])
def api_stop_attack():
    """API: Detener ataque"""
    try:
        attack_type = request.json.get('type', 'packet_sniff')
        if attack_type in ATTACKS:
            if attack_type == 'packet_sniff':
                hijack.stop_sniffer()
            ATTACKS[attack_type] = False
            return jsonify({"success": True, "message": f"Ataque {attack_type} detenido"})
        return jsonify({"success": False, "error": "Tipo de ataque inválido"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/stats')
def api_stats():
    """API: Estadísticas"""
    return jsonify(STATS)

@app.route('/api/devices')
def api_devices():
    """API: Dispositivos conectados"""
    return jsonify({
        "total": STATS['connected_devices'],
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/monitor')
def api_monitor():
    """API: Estado del modo monitor"""
    return jsonify({
        "monitor_active": hijack.monitor_interface is not None,
        "interface": hijack.monitor_interface,
        "original_interface": hijack.original_interface,
        "available_interfaces": hijack.get_wireless_interfaces()
    })

@app.route('/api/monitor/enable', methods=['POST'])
def api_enable_monitor():
    """API: Activar modo monitor"""
    try:
        interface = request.json.get('interface') if request.json else None
        success = hijack.set_monitor_mode(interface)
        return jsonify({
            "success": success,
            "interface": hijack.monitor_interface,
            "message": "Modo monitor activado" if success else "No se pudo activar modo monitor"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/monitor/disable', methods=['POST'])
def api_disable_monitor():
    """API: Desactivar modo monitor"""
    try:
        hijack.restore_managed_mode()
        return jsonify({
            "success": True,
            "message": "Modo managed restaurado"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

# ========================
# NUEVOS ENDPOINTS - Dashboard
# ========================

@app.route('/')
def dashboard():
    """Dashboard principal en HTML"""
    return render_template('index.html')

@app.route('/api/infected', methods=['GET'])
def api_infected():
    """API: Obtener dispositivos infectados"""
    return jsonify({
        "total": len(INFECTED_DEVICES),
        "devices": INFECTED_DEVICES
    })

@app.route('/api/infected/add', methods=['POST'])
def api_add_infected():
    """API: Agregar dispositivo a lista de infectados"""
    try:
        device = request.json
        device['timestamp'] = datetime.now().isoformat()
        device['status'] = 'Comprometido'
        
        # Evitar duplicados
        if not any(d['ip'] == device['ip'] for d in INFECTED_DEVICES):
            INFECTED_DEVICES.append(device)
            save_infected_devices(INFECTED_DEVICES)
            add_log('DEVICE_INFECTED', f"IP: {device['ip']}, MAC: {device['mac']}")
            
            return jsonify({
                "success": True,
                "message": f"Dispositivo {device['ip']} agregado"
            })
        return jsonify({
            "success": False,
            "message": "Dispositivo ya existe"
        }), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/infected/remove/<ip>', methods=['DELETE'])
def api_remove_infected(ip):
    """API: Remover dispositivo de lista de infectados"""
    global INFECTED_DEVICES
    try:
        INFECTED_DEVICES = [d for d in INFECTED_DEVICES if d['ip'] != ip]
        save_infected_devices(INFECTED_DEVICES)
        add_log('DEVICE_REMOVED', f"IP: {ip}")
        
        return jsonify({
            "success": True,
            "message": f"Dispositivo {ip} removido"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/infected/clear', methods=['DELETE'])
def api_clear_infected():
    """API: Limpiar lista de infectados"""
    global INFECTED_DEVICES
    try:
        count = len(INFECTED_DEVICES)
        INFECTED_DEVICES = []
        save_infected_devices(INFECTED_DEVICES)
        add_log('INFECTED_CLEARED', f"Total removido: {count}")
        
        return jsonify({
            "success": True,
            "message": f"{count} dispositivos removidos"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/logs', methods=['GET'])
def api_logs():
    """API: Obtener logs de operaciones"""
    try:
        if os.path.exists(LOGS_DB):
            with open(LOGS_DB, 'r') as f:
                logs = json.load(f)
            return jsonify({
                "total": len(logs),
                "logs": logs[-50:]  # Últimos 50 logs
            })
        return jsonify({
            "total": 0,
            "logs": []
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/export', methods=['GET'])
def api_export():
    """API: Exportar datos completos"""
    try:
        return jsonify({
            "timestamp": datetime.now().isoformat(),
            "infected_devices": INFECTED_DEVICES,
            "current_attacks": ATTACKS,
            "stats": STATS
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

# ========================
# Rutas anteriores (mantenidas)
# ========================

def main():
    """Función principal"""
    print("""
    ╔════════════════════════════════════════╗
    ║     QUANTUM-HIJACK 2026 v1.0           ║
    ║     Hacking Ético - Emmanuel           ║
    ║                                        ║
    ║  ⚠️  SOLO para testing autorizado      ║
    ║  ⚠️  No usar sin permiso                ║
    ╚════════════════════════════════════════╝
    """)
    
    # Verificar permisos
    if not hijack.check_root():
        sys.exit(1)
    
    # Detectar y configurar interfaz wireless en modo monitor
    print("\n[INICIALIZACIÓN]")
    print("─" * 50)
    
    interfaces = hijack.get_wireless_interfaces()
    if interfaces:
        print(f"\n💡 Se detectaron {len(interfaces)} interfaz(es) wireless:")
        for idx, iface in enumerate(interfaces, 1):
            print(f"   {idx}. {iface}")
        
        print("\n🔧 Configurando modo monitor automáticamente...")
        if hijack.set_monitor_mode():
            print(f"✅ Interfaz {hijack.monitor_interface} lista en modo monitor")
        else:
            print("⚠️  Advertencia: No se pudo activar modo monitor")
            print("   El programa continuará con funcionalidad limitada")
    else:
        print("⚠️  No se detectaron interfaces wireless")
        print("   El programa funcionará solo con interfaces de red estándar")
    
    hijack.running = True
    local_ip = hijack.get_local_ip()
    
    print(f"""
    ─────────────────────────────────────────────────
    [DASHBOARD ACTIVO]
    
    🌐 DASHBOARD WEB:  http://{local_ip}:8080
    🌐 URL Externa:    http://0.0.0.0:8080
    📡 Interfaz Monitor: {hijack.monitor_interface or 'No configurada'}
    
    [NUEVOS ENDPOINTS DASHBOARD]
    
    GET  /              - Dashboard HTML profesional
    GET  /api/infected  - Dispositivos infectados
    POST /api/infected/add - Agregar infectado
    DELETE /api/infected/remove/<ip> - Remover infectado
    DELETE /api/infected/clear - Limpiar historial
    GET  /api/logs      - Logs de operaciones
    GET  /api/export    - Exportar datos
    
    [API ENDPOINTS CLÁSICOS]
    
    GET  /api/status         - Estado del sistema
    POST /api/scan           - Escanear red local
    POST /api/attacks/start  - Iniciar ataque
    POST /api/attacks/stop   - Detener ataque
    GET  /api/stats          - Ver estadísticas
    GET  /api/devices        - Dispositivos detectados
    GET  /api/monitor        - Info modo monitor
    
    ─────────────────────────────────────────────────
    Presiona CTRL+C para detener y limpiar
    ─────────────────────────────────────────────────
    """)
    
    try:
        app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        print("\n\n⛔ DETENIENDO APLICACIÓN...")
        print("─" * 50)
        
        # Guardar datos antes de salir
        save_infected_devices(INFECTED_DEVICES)
        add_log('APP_SHUTDOWN', 'Aplicación cerrada normalmente')
        
        # Restaurar interfaz a modo managed
        if hijack.monitor_interface:
            print("🔄 Restaurando interfaz a modo normal...")
            hijack.restore_managed_mode()
        
        hijack.running = False
        print("✅ Datos guardados. Limpieza completada. ¡Hasta pronto!")
        print("─" * 50 + "\n")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error fatal: {e}")
        
        # Intentar restaurar de todos modos
        if hijack.monitor_interface:
            hijack.restore_managed_mode()
        
        sys.exit(1)

if __name__ == '__main__':
    main()
