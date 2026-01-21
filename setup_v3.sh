#!/bin/bash
# QUANTUM-HIJACK v3.0 SETUP
# Instalar dependencias y preparar entorno

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  QUANTUM-HIJACK v3.0 - SETUP & INSTALACIÓN                ║"
echo "║  Emmanuel 2026                                             ║"
echo "╚════════════════════════════════════════════════════════════╝"

# Verificar si es root
if [[ $EUID -ne 0 ]]; then
   echo "❌ Este script debe ejecutarse con sudo"
   echo "Ejecuta: sudo bash setup.sh"
   exit 1
fi

echo ""
echo "[1/4] Actualizando repositorios..."
apt update -y > /dev/null 2>&1

echo "[2/4] Instalando dependencias del sistema..."
apt install -y \
    hostapd \
    dnsmasq \
    aircrack-ng \
    wireless-tools \
    iw \
    python3-pip \
    python3-scapy \
    git \
    > /dev/null 2>&1

echo "[3/4] Instalando dependencias Python..."
pip3 install -q \
    flask \
    scapy \
    requests

echo "[4/4] Creando estructura de directorios..."
mkdir -p logs payloads capture

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║  ✅ INSTALACIÓN COMPLETADA                                 ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "🚀 PRÓXIMOS PASOS:"
echo ""
echo "1. Dar permisos de ejecución:"
echo "   chmod +x quantum_hijack_v3.py interceptor_v3.py"
echo ""
echo "2. Ejecutar la aplicación:"
echo "   sudo python3 quantum_hijack_v3.py"
echo ""
echo "3. Abrir en navegador:"
echo "   http://localhost:8080"
echo ""
echo "4. Click en '🔥 INICIAR TODO'"
echo ""
echo "✨ ¡Listo!"
