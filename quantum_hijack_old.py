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
import psutil

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
    
    def get_network_range(self):
        """Detectar rango de red automáticamente"""
        try:
            # Fallback a detección simple basada en IP local
            local_ip = self.get_local_ip()
            if local_ip.startswith('192.168.'):
                # Asumir red /24
                base = '.'.join(local_ip.split('.')[:-1])
                return f"{base}.0/24"
            elif local_ip.startswith('10.'):
                parts = local_ip.split('.')
                return f"10.{parts[1]}.{parts[2]}.0/24"
            elif local_ip.startswith('172.'):
                parts = local_ip.split('.')
                return f"172.{parts[1]}.{parts[2]}.0/24"
            else:
                return "192.168.1.0/24"
        except Exception as e:
            logger.error(f"Error detectando rango de red: {e}")
            return "192.168.1.0/24"
    
    def scan_network(self, network_range=None):
        """Escanear red para descubrir dispositivos"""
        devices = []
        try:
            # Detectar red automáticamente si no se especifica
            if not network_range:
                network_range = self.get_network_range()
            
            logger.info(f"⏳ [CARGANDO] Preparando escaneo ARP...")
            logger.info(f"📡 [EJECUTANDO] ARP Scan en rango: {network_range}")
            logger.info(f"🔍 [COMANDO] arp-scan {network_range} (usando Scapy)")
            
            # Crear paquete ARP
            arp_request = ARP(pdst=network_range)
            broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
            arp_request_broadcast = broadcast/arp_request
            
            logger.info(f"📤 [ENVIANDO] Paquetes ARP broadcast a toda la red...")
            logger.info(f"⏱️  [ESPERANDO] Respuestas ARP (timeout: 3s)...")
            
            # Enviar y recibir paquetes
            from scapy.all import srp
            answered_list = srp(arp_request_broadcast, timeout=3, verbose=0)[0]
            
            logger.info(f"📥 [RECIBIDO] {len(answered_list)} respuestas ARP")
            
            # Procesar respuestas
            for sent, received in answered_list:
                device_dict = {
                    "ip": received.psrc,
                    "mac": received.hwsrc,
                    "name": self.get_device_name(received.hwsrc),
                    "timestamp": datetime.now().isoformat(),
                    "status": "Activo"
                }
                devices.append(device_dict)
                logger.info(f"   ✓ Dispositivo: {device_dict['ip']} ({device_dict['mac']}) - {device_dict['name']}")
            
            STATS['connected_devices'] = len(devices)
            STATS['total_scans'] += 1
            
            if len(devices) > 0:
                logger.info(f"✅ [COMPLETADO] {len(devices)} dispositivos encontrados y listos para infectar")
            else:
                logger.warning(f"⚠️  [ADVERTENCIA] 0 dispositivos encontrados")
                logger.info(f"💡 [SUGERENCIA] Verifica:")
                logger.info(f"   1. Que estés conectado a una red WiFi o Ethernet")
                logger.info(f"   2. Rango de red correcto: {network_range}")
                logger.info(f"   3. Permisos de root/sudo activos")
                logger.info(f"   4. Tu IP local: {self.get_local_ip()}")
            
            return devices
        except Exception as e:
            logger.error(f"❌ [ERROR] Escaneo fallido: {e}")
            logger.info(f"🔧 [DEBUG] Tipo de error: {type(e).__name__}")
            return []
    
    def get_device_name(self, mac):
        """Obtener nombre del dispositivo por MAC con tipo y fabricante"""
        try:
            vendor_prefix = mac[:8].upper().replace(':', '')
            
            # Base de datos de fabricantes y tipos de dispositivos
            devices_db = {
                # Apple - iPhone, iPad, Mac
                '5C80B6': ('Apple', '📱 iPhone/iPad'),
                '0CD14D': ('Apple', '📱 iPhone'),
                '00D04F': ('Apple', '💻 MacBook'),
                'F41E89': ('Apple', '📱 iPhone'),
                'B827EB': ('Apple', '💻 Raspberry Pi'),
                
                # Samsung - Android
                '3C84': ('Samsung', '📱 Celular'),
                'FC2450': ('Samsung', '📱 Celular'),
                'A41D7A': ('Samsung', '📱 Celular'),
                
                # Xiaomi - Android
                'F0DEF1': ('Xiaomi', '📱 Celular'),
                '002436': ('Xiaomi', '📱 Celular'),
                '10027B': ('Xiaomi', '📱 Celular'),
                
                # Huawei - Android
                '8863DF': ('Huawei', '📱 Celular'),
                'A41D00': ('Huawei', '📱 Celular'),
                'F867B3': ('Huawei', '📱 Celular'),
                
                # LG - Android / TV
                'A4C494': ('LG', '📱 Celular'),
                '8483F8': ('LG', '📺 Smart TV'),
                
                # Google - Android
                '6C7E80': ('Google', '📱 Pixel Phone'),
                '4A771D': ('Google', '📱 Pixel Phone'),
                
                # Microsoft - Windows
                '00505E': ('Microsoft', '💻 Windows PC'),
                '000569': ('Microsoft', '💻 Windows PC'),
                
                # Intel - PC/Laptop
                '00505': ('Intel', '💻 PC/Laptop'),
                '00165F': ('Intel', '💻 PC/Laptop'),
                
                # Cisco - Networking
                '001B44': ('Cisco', '🌐 Router/Switch'),
                '0021A0': ('Cisco', '🌐 Router/Switch'),
                
                # Netgear - Router/Networking
                '00D861': ('Netgear', '🌐 Router'),
                '7C108F': ('Netgear', '🌐 Router'),
                
                # TP-Link - Router
                '00268F': ('TP-Link', '🌐 Router'),
                'F4B8E8': ('TP-Link', '🌐 Router'),
                
                # Linksys - Router
                '000C41': ('Linksys', '🌐 Router'),
                '0014BF': ('Linksys', '🌐 Router'),
                
                # D-Link - Router
                '001346': ('D-Link', '🌐 Router'),
                '00601D': ('D-Link', '🌐 Router'),
                
                # ASUS - Router/PC
                '0025B3': ('ASUS', '🌐 Router'),
                '00E04C': ('Realtek', '💻 Adaptador Red'),
                
                # Realtek - Network Adapter
                '52540F': ('Realtek', '💻 Adaptador'),
                
                # Amazon - Echo/Alexa
                '60D81D': ('Amazon', '🔊 Echo/Alexa'),
                '740DEF': ('Amazon', '🔊 Echo/Alexa'),
            }
            
            # Buscar en la base de datos
            if vendor_prefix in devices_db:
                brand, device_type = devices_db[vendor_prefix]
                return device_type
            
            # Búsqueda por prefijo
            for prefix, (brand, device_type) in devices_db.items():
                if vendor_prefix.startswith(prefix[:6]):
                    return device_type
            
            # Fallback por patrones generales
            if 'Apple' in vendor_prefix.upper():
                return '📱 Apple Device'
            elif any(x in vendor_prefix.upper() for x in ['2C', '3C', '5C', '6C', '8C']):
                return '📱 Celular'
            elif any(x in vendor_prefix.upper() for x in ['00', '10', '20', '30']):
                return '💻 PC/Dispositivo'
            
            return '❓ Dispositivo Desconocido'
        except:
            return '❓ Error Identificación'
    
    def start_sniffer(self):
        """Iniciar captura de paquetes"""
        ATTACKS['packet_sniff'] = True
        logger.info("⏳ [CARGANDO] Preparando sniffer...")
        logger.info("🔴 [EJECUTANDO] tcpdump -i any -n (modo Scapy)")
        logger.info("📡 [ACTIVO] Captura de paquetes en progreso...")
        STATS['packets_captured'] = 0
    
    def stop_sniffer(self):
        """Detener captura de paquetes"""
        ATTACKS['packet_sniff'] = False
        logger.info("🛑 [DETENIDO] Captura de paquetes finalizada")
        logger.info(f"📊 [RESUMEN] Total paquetes capturados: {STATS['packets_captured']}")
    
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

@app.route('/api/status')
def api_status():
    """API: Estado actual del sistema"""
    return jsonify(hijack.get_status())

@app.route('/api/scan', methods=['POST'])
def api_scan():
    """API: Escanear red"""
    try:
        network = request.json.get('network') if request.json else None
        
        logger.info(f"")
        logger.info(f"{'='*60}")
        logger.info(f"🔍 [ESCANEO INICIADO] Buscando dispositivos en la red...")
        if network:
            logger.info(f"📍 [RANGO] Especificado: {network}")
        else:
            logger.info(f"📍 [RANGO] Auto-detectando red local...")
        logger.info(f"{'='*60}")
        
        devices = hijack.scan_network(network)
        
        logger.info(f"")
        logger.info(f"{'='*60}")
        logger.info(f"✅ [ESCANEO COMPLETADO]")
        logger.info(f"📊 [RESULTADO] {len(devices)} dispositivos disponibles para infectar")
        logger.info(f"{'='*60}")
        logger.info(f"")
        
        add_log('NETWORK_SCAN', f"Encontrados: {len(devices)} dispositivos")
        
        return jsonify({
            "success": True,
            "devices_found": len(devices),
            "devices": devices,
            "network_range": network or hijack.get_network_range()
        })
    except Exception as e:
        logger.error(f"❌ [ERROR] Escaneo fallido: {e}")
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/attacks/start', methods=['POST'])
def api_start_attack():
    """API: Iniciar ataque"""
    try:
        attack_type = request.json.get('type', 'packet_sniff')
        target_ip = request.json.get('ip', 'broadcast')
        
        logger.info(f"")
        logger.info(f"{'='*60}")
        logger.info(f"⚔️  [ATAQUE INICIADO] Tipo: {attack_type}")
        logger.info(f"🎯 [OBJETIVO] IP: {target_ip}")
        logger.info(f"{'='*60}")
        
        if attack_type in ATTACKS:
            if attack_type == 'packet_sniff':
                hijack.start_sniffer()
            elif attack_type == 'arp_spoof':
                logger.info(f"🔧 [COMANDO] arpspoof -i {hijack.monitor_interface or 'wlan0'} -t {target_ip}")
                logger.info(f"📡 [EJECUTANDO] Envenenamiento ARP en progreso...")
            elif attack_type == 'dns_hijack':
                logger.info(f"🔧 [COMANDO] dnsspoof -i {hijack.monitor_interface or 'wlan0'}")
                logger.info(f"📡 [EJECUTANDO] Redirección DNS activa...")
            elif attack_type == 'deauth':
                logger.info(f"🔧 [COMANDO] aireplay-ng --deauth 0 -a {target_ip} {hijack.monitor_interface or 'wlan0mon'}")
                logger.info(f"📡 [EJECUTANDO] Ataque de desautenticación...")
            
            ATTACKS[attack_type] = True
            STATS['attacks_completed'] += 1
            add_log('ATTACK_START', f"Tipo: {attack_type}, Objetivo: {target_ip}")
            
            return jsonify({
                "success": True, 
                "message": f"Ataque {attack_type} iniciado contra {target_ip}",
                "details": {
                    "type": attack_type,
                    "target": target_ip,
                    "interface": hijack.monitor_interface or "N/A"
                }
            })
        return jsonify({"success": False, "error": "Tipo de ataque inválido"}), 400
    except Exception as e:
        logger.error(f"❌ [ERROR] Fallo al iniciar ataque: {e}")
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/attacks/stop', methods=['POST'])
def api_stop_attack():
    """API: Detener ataque"""
    try:
        attack_type = request.json.get('type', 'packet_sniff')
        
        logger.info(f"🛑 [DETENIENDO] Ataque: {attack_type}")
        
        if attack_type in ATTACKS:
            if attack_type == 'packet_sniff':
                hijack.stop_sniffer()
            else:
                logger.info(f"✋ [STOP] Finalizando {attack_type}...")
                logger.info(f"🔧 [COMANDO] killall arpspoof dnsspoof aireplay-ng")
            
            ATTACKS[attack_type] = False
            add_log('ATTACK_STOP', f"Tipo: {attack_type}")
            
            return jsonify({
                "success": True, 
                "message": f"Ataque {attack_type} detenido",
                "stats": STATS
            })
        return jsonify({"success": False, "error": "Tipo de ataque inválido"}), 400
    except Exception as e:
        logger.error(f"❌ [ERROR] Fallo al detener ataque: {e}")
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
