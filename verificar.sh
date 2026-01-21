#!/bin/bash

# ═══════════════════════════════════════════════════════════════════════════
# QUANTUM-HIJACK - VERIFICACIÓN FINAL
# Chequea que todos los archivos estén listos para ejecutar
# ═══════════════════════════════════════════════════════════════════════════

clear

echo "╔════════════════════════════════════════════════════════════╗"
echo "║      ✅ QUANTUM-HIJACK - VERIFICACIÓN FINAL                ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Contador
files_ok=0
files_missing=0

# Función para verificar archivo
check_file() {
    if [ -f "$1" ]; then
        echo "  ✅ $1"
        ((files_ok++))
    else
        echo "  ❌ $1 (FALTA)"
        ((files_missing++))
    fi
}

echo "📋 VERIFICANDO ARCHIVOS PRINCIPALES:"
echo "─────────────────────────────────────────────────────────────"

check_file "setup.sh"
check_file "entangle.py"
check_file "quantum_interceptor.py"
check_file "propagator.py"
check_file "dashboard.py"
check_file "evento.sh"

echo ""
echo "📚 DOCUMENTACIÓN:"
echo "─────────────────────────────────────────────────────────────"

check_file "README_FINAL.md"

echo ""
echo "🔧 VERIFICANDO DEPENDENCIAS:"
echo "─────────────────────────────────────────────────────────────"

# Python
if command -v python3 &> /dev/null; then
    echo "  ✅ Python3"
    ((files_ok++))
else
    echo "  ❌ Python3 (INSTALAR: sudo apt install python3)"
    ((files_missing++))
fi

# Scapy
if python3 -c "import scapy" 2>/dev/null; then
    echo "  ✅ Scapy"
    ((files_ok++))
else
    echo "  ❌ Scapy (INSTALAR: pip3 install scapy)"
    ((files_missing++))
fi

# Hostapd
if command -v hostapd &> /dev/null; then
    echo "  ✅ Hostapd"
    ((files_ok++))
else
    echo "  ❌ Hostapd (INSTALAR: sudo apt install hostapd)"
    ((files_missing++))
fi

# Dnsmasq
if command -v dnsmasq &> /dev/null; then
    echo "  ✅ Dnsmasq"
    ((files_ok++))
else
    echo "  ❌ Dnsmasq (INSTALAR: sudo apt install dnsmasq)"
    ((files_missing++))
fi

# Aircrack-ng
if command -v airmon-ng &> /dev/null; then
    echo "  ✅ Aircrack-ng"
    ((files_ok++))
else
    echo "  ❌ Aircrack-ng (INSTALAR: sudo apt install aircrack-ng)"
    ((files_missing++))
fi

# iw
if command -v iw &> /dev/null; then
    echo "  ✅ iw"
    ((files_ok++))
else
    echo "  ❌ iw (INSTALAR: sudo apt install iw)"
    ((files_missing++))
fi

echo ""
echo "⚙️  VERIFICANDO PERMISOS:"
echo "─────────────────────────────────────────────────────────────"

# Verificar permisos
if [ -x "setup.sh" ]; then
    echo "  ✅ setup.sh es ejecutable"
    ((files_ok++))
else
    echo "  ℹ️  setup.sh no es ejecutable (haciendo ejecutable...)"
    chmod +x setup.sh
fi

if [ -x "evento.sh" ]; then
    echo "  ✅ evento.sh es ejecutable"
    ((files_ok++))
else
    echo "  ℹ️  evento.sh no es ejecutable (haciendo ejecutable...)"
    chmod +x evento.sh
fi

echo ""
echo "═════════════════════════════════════════════════════════════"
echo ""
echo "📊 RESULTADO FINAL:"
echo "  ✅ Correcto: $files_ok"
echo "  ❌ Problemas: $files_missing"
echo ""

if [ $files_missing -eq 0 ]; then
    echo "✅ LISTO PARA EJECUTAR"
    echo ""
    echo "Para iniciar la demostración:"
    echo ""
    echo "  sudo ./evento.sh"
    echo ""
    echo "O ejecutar paso a paso:"
    echo ""
    echo "  Terminal 1: sudo bash setup.sh"
    echo "  Terminal 2: sudo python3 entangle.py"
    echo "  Terminal 3: sudo python3 quantum_interceptor.py"
    echo "  Terminal 4: sudo python3 propagator.py"
    echo "  Terminal 5: python3 dashboard.py"
    echo ""
else
    echo "⚠️  PROBLEMAS DETECTADOS"
    echo ""
    echo "Por favor instala las dependencias faltantes:"
    echo "  sudo apt update"
    echo "  sudo apt install -y python3 hostapd dnsmasq aircrack-ng iw"
    echo "  pip3 install scapy"
    echo ""
fi

echo "═════════════════════════════════════════════════════════════"
