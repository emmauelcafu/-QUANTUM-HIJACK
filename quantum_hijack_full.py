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
from flask import Flask, render_template, jsonify, request
from scapy.all import ARP, Ether, get_if_hwaddr, conf
import logging

# Configuración
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Variables globales
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
        
    def check_root(self):
        """Verificar si se ejecuta como root (requerido en Linux)"""
        if os.name == 'posix' and os.geteuid() != 0:
            logger.error("❌ Este programa debe ejecutarse como root (sudo)")
            return False
        return True
    
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

# ========================
# FUNCIÓN PRINCIPAL
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
    
    hijack.running = True
    local_ip = hijack.get_local_ip()
    
    print(f"""
    ✅ Iniciando dashboard en http://{local_ip}:8080
    📊 API disponible en http://{local_ip}:8080/api/status
    
    Endpoints disponibles:
    - GET  /api/status         - Estado del sistema
    - POST /api/scan           - Escanear red
    - POST /api/attacks/start  - Iniciar ataque
    - POST /api/attacks/stop   - Detener ataque
    - GET  /api/stats          - Estadísticas
    - GET  /api/devices        - Dispositivos
    
    Presiona CTRL+C para salir
    """)
    
    try:
        app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False)
    except KeyboardInterrupt:
        print("\n\n⛔ Deteniendo aplicación...")
        hijack.running = False
        logger.info("✅ Limpieza completada")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error fatal: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
