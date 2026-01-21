#!/bin/bash

# ═══════════════════════════════════════════════════════════════════════════
# QUANTUM-HIJACK - SETUP INICIAL
# Prepara el sistema: modo monitor, carpetas, dependencias
# ═══════════════════════════════════════════════════════════════════════════

echo "╔════════════════════════════════════════════════════════════╗"
echo "║         🔥 QUANTUM-HIJACK SETUP - INITIALIZATION           ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Verificar permisos root
if [[ $EUID -ne 0 ]]; then
   echo "❌ Este script requiere permisos root"
   echo "Ejecuta: sudo ./setup.sh"
   exit 1
fi

echo "[*] Limpiando procesos previos..."
pkill hostapd 2>/dev/null
pkill dnsmasq 2>/dev/null
pkill airmon-ng 2>/dev/null
sleep 1

echo "[*] Desactivando modo monitor previo..."
airmon-ng stop wlan0mon 2>/dev/null
sleep 1

echo "[*] Detectando interfaz WiFi..."
INTERFACE=$(iw dev | grep "Interface" | head -1 | awk '{print $2}')

if [ -z "$INTERFACE" ]; then
    echo "❌ No se encontró interfaz WiFi"
    echo "Interfaces disponibles:"
    iw dev
    exit 1
fi

echo "[✓] Interfaz encontrada: $INTERFACE"

echo ""
echo "[*] Iniciando modo monitor en $INTERFACE..."
airmon-ng start $INTERFACE

sleep 2

MONITOR_IFACE="${INTERFACE}mon"

# Verificar que modo monitor se activó
if ! iw dev | grep -q "$MONITOR_IFACE"; then
    echo "❌ No se pudo activar modo monitor"
    exit 1
fi

echo "[✓] Modo monitor ACTIVO: $MONITOR_IFACE"

# Crear carpetas
echo ""
echo "[*] Creando estructura de directorios..."
mkdir -p logs payloads capture infected_devices

echo "[✓] Carpetas creadas"

# Guardar nombre de interfaz para otros scripts
echo "$MONITOR_IFACE" > .monitor_iface
echo "$INTERFACE" > .wifi_iface

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║              ✅ SETUP COMPLETADO                           ║"
echo "╠════════════════════════════════════════════════════════════╣"
echo "║ Interfaz WiFi: $INTERFACE"
echo "║ Modo Monitor:  $MONITOR_IFACE"
echo "║ Estado:        ✓ LISTO PARA ENTANGLE"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Próximo paso: sudo python3 entangle.py"
echo "📖 Ejecutar con:"
echo "   sudo python3 quantum_hijack_full.py"
echo ""
echo "⚠️  NOTA: El programa configurará automáticamente"
echo "   tu interfaz wireless en modo monitor"
echo ""
