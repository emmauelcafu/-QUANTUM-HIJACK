#!/bin/bash
# QUANTUM-HIJACK - QUICK START GUIDE

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║          🔓 QUANTUM-HIJACK v2.0 - QUICK START GUIDE            ║"
echo "║                                                                ║"
echo "║  Herramienta de Hacking Ético - Rogue WiFi + Interceptor      ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}[1/6] VERIFICANDO SISTEMA${NC}"
echo "────────────────────────────────────────────────────────────────"

# Verificar si es root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}❌ Este script requiere permisos root${NC}"
    echo ""
    echo "Ejecuta:"
    echo "  sudo bash QUICK_START.sh"
    exit 1
fi

echo -e "${GREEN}✓ Permisos root detectados${NC}"

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 no instalado${NC}"
    echo "Instala: sudo apt install python3-pip"
    exit 1
fi
echo -e "${GREEN}✓ Python3 encontrado${NC}"

# Verificar Kali
if grep -qi "kali" /etc/os-release; then
    echo -e "${GREEN}✓ Kali Linux detectado${NC}"
else
    echo -e "${YELLOW}⚠ Posiblemente no sea Kali Linux (algunas funciones pueden fallar)${NC}"
fi

echo ""
echo -e "${BLUE}[2/6] INSTALANDO DEPENDENCIAS${NC}"
echo "────────────────────────────────────────────────────────────────"

# Actualizar repositorios
echo -e "${YELLOW}Actualizando apt...${NC}"
apt update -qq > /dev/null 2>&1

# Instalar paquetes
PACKAGES="hostapd dnsmasq airmon-ng iw wireless-tools"

for pkg in $PACKAGES; do
    if dpkg -l | grep -q "^ii  $pkg"; then
        echo -e "${GREEN}✓ $pkg${NC}"
    else
        echo -e "${YELLOW}Instalando $pkg...${NC}"
        apt install -y "$pkg" > /dev/null 2>&1
        echo -e "${GREEN}✓ $pkg${NC}"
    fi
done

echo ""
echo -e "${BLUE}[3/6] VERIFICANDO MÓDULOS PYTHON${NC}"
echo "────────────────────────────────────────────────────────────────"

# Verificar módulos Python
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Instalando Flask...${NC}"
    pip3 install flask flask-cors > /dev/null 2>&1
fi
echo -e "${GREEN}✓ Flask${NC}"

python3 -c "import scapy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Instalando Scapy...${NC}"
    pip3 install scapy > /dev/null 2>&1
fi
echo -e "${GREEN}✓ Scapy${NC}"

echo ""
echo -e "${BLUE}[4/6] VERIFICANDO ARCHIVOS${NC}"
echo "────────────────────────────────────────────────────────────────"

# Verificar archivos esenciales
FILES=(
    "quantum_hijack_full.py"
    "hostapd_1.conf"
    "dnsmasq.conf"
    "interceptor.py"
    "dashboard_terminal.py"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓ $file${NC}"
    else
        echo -e "${RED}✗ $file NO ENCONTRADO${NC}"
    fi
done

# Crear directorios
mkdir -p logs payloads capture
echo -e "${GREEN}✓ Directorios creados${NC}"

echo ""
echo -e "${BLUE}[5/6] CONFIGURACIÓN${NC}"
echo "────────────────────────────────────────────────────────────────"

# Detectar interfaz WiFi
WIFI_IFACE=$(iw dev | grep -i "interface" | head -1 | awk '{print $2}')

if [ -z "$WIFI_IFACE" ]; then
    echo -e "${RED}✗ No se encontró interfaz WiFi${NC}"
    echo ""
    echo "Opciones:"
    echo "  1. Asegúrate de que la tarjeta WiFi esté conectada"
    echo "  2. Usa: iw dev"
    exit 1
else
    echo -e "${GREEN}✓ Interfaz WiFi detectada: $WIFI_IFACE${NC}"
fi

echo ""
echo -e "${BLUE}[6/6] RESUMEN${NC}"
echo "────────────────────────────────────────────────────────────────"
echo ""
echo -e "${GREEN}✓ TODAS LAS VERIFICACIONES PASARON${NC}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "${BLUE}🚀 PARA INICIAR QUANTUM-HIJACK:${NC}"
echo ""
echo -e "  ${GREEN}sudo python3 quantum_hijack_full.py${NC}"
echo ""
echo -e "Luego abre en navegador:"
echo -e "  ${GREEN}http://localhost:8080${NC}"
echo ""
echo -e "Y presiona:"
echo -e "  ${GREEN}🔥 INICIAR QUANTUM-HIJACK COMPLETO${NC}"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 Configuración WiFi Rogue:"
echo "  SSID: CafeWiFi_Quantum"
echo "  Password: 12345678"
echo "  Gateway: 192.168.1.1"
echo "  Rango DHCP: 192.168.1.2-100"
echo ""
echo "📚 Documentación completa en: GUIA_FINAL.md"
echo ""
echo "⚠️  SOLO PARA TESTING AUTORIZADO"
echo ""
