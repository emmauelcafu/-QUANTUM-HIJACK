#!/bin/bash
# QUANTUM-HIJACK v3.0 - Verificador de Requisitos
# Verifica que el sistema esté listo antes de ejecutar

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  QUANTUM-HIJACK v3.0 - VERIFICACIÓN DE REQUISITOS         ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Contadores
PASSED=0
FAILED=0
WARNINGS=0

check_pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASSED++))
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
    ((FAILED++))
}

check_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
    ((WARNINGS++))
}

echo "1. VERIFICANDO SISTEMA OPERATIVO"
echo "─────────────────────────────────────────────────────────────"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    check_pass "Sistema: Linux detectado"
    
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        if [[ "$ID" == "kali" || "$ID_LIKE" == *"debian"* ]]; then
            check_pass "Distribución: $NAME compatible"
        else
            check_warn "Distribución: $NAME (recomendado: Kali Linux)"
        fi
    fi
else
    check_fail "Sistema: No es Linux (requiere Linux para WiFi en modo monitor)"
    echo "  → Este proyecto SOLO funciona en Linux (Kali, Ubuntu, etc.)"
    echo "  → Estás en: $OSTYPE"
fi
echo ""

echo "2. VERIFICANDO PERMISOS"
echo "─────────────────────────────────────────────────────────────"
if [ "$EUID" -eq 0 ]; then
    check_pass "Usuario: root/sudo (requerido)"
else
    check_fail "Usuario: No root - ejecuta con: sudo bash $0"
fi
echo ""

echo "3. VERIFICANDO DEPENDENCIAS DEL SISTEMA"
echo "─────────────────────────────────────────────────────────────"

# Herramientas de red
if command -v hostapd &> /dev/null; then
    check_pass "hostapd: Instalado ($(hostapd -v 2>&1 | head -n1 | cut -d' ' -f2))"
else
    check_fail "hostapd: NO instalado - ejecuta: sudo apt install hostapd"
fi

if command -v dnsmasq &> /dev/null; then
    check_pass "dnsmasq: Instalado ($(dnsmasq -v 2>&1 | head -n1 | cut -d' ' -f3))"
else
    check_fail "dnsmasq: NO instalado - ejecuta: sudo apt install dnsmasq"
fi

if command -v airmon-ng &> /dev/null; then
    check_pass "aircrack-ng: Instalado ($(airmon-ng --version 2>&1 | head -n1 | awk '{print $3}'))"
else
    check_fail "aircrack-ng: NO instalado - ejecuta: sudo apt install aircrack-ng"
fi

if command -v iw &> /dev/null; then
    check_pass "iw (wireless tools): Instalado"
else
    check_fail "iw: NO instalado - ejecuta: sudo apt install iw wireless-tools"
fi

echo ""

echo "4. VERIFICANDO PYTHON Y LIBRERÍAS"
echo "─────────────────────────────────────────────────────────────"

if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    check_pass "Python 3: Instalado ($PYTHON_VERSION)"
    
    # Verificar pip
    if command -v pip3 &> /dev/null; then
        check_pass "pip3: Instalado"
    else
        check_fail "pip3: NO instalado - ejecuta: sudo apt install python3-pip"
    fi
    
    # Verificar librerías Python
    echo "  Verificando librerías Python..."
    
    if python3 -c "import flask" 2>/dev/null; then
        check_pass "  flask: Instalado"
    else
        check_fail "  flask: NO instalado - ejecuta: pip3 install flask"
    fi
    
    if python3 -c "import scapy" 2>/dev/null; then
        check_pass "  scapy: Instalado"
    else
        check_fail "  scapy: NO instalado - ejecuta: pip3 install scapy o sudo apt install python3-scapy"
    fi
    
    if python3 -c "import requests" 2>/dev/null; then
        check_pass "  requests: Instalado"
    else
        check_warn "  requests: NO instalado (opcional) - ejecuta: pip3 install requests"
    fi
else
    check_fail "Python 3: NO instalado - ejecuta: sudo apt install python3"
fi

echo ""

echo "5. VERIFICANDO INTERFAZ WIFI"
echo "─────────────────────────────────────────────────────────────"

if command -v iw &> /dev/null; then
    WIFI_IFACES=$(iw dev | grep Interface | awk '{print $2}')
    
    if [ -z "$WIFI_IFACES" ]; then
        check_fail "Interfaz WiFi: NO detectada"
        echo "  → Conecta un adaptador WiFi compatible con modo monitor"
    else
        for iface in $WIFI_IFACES; do
            check_pass "Interfaz WiFi: $iface detectada"
            
            # Verificar modo monitor
            if iw $iface info | grep -q "type managed"; then
                echo "    Modo actual: managed (correcto, se cambiará a monitor)"
            elif iw $iface info | grep -q "type monitor"; then
                check_warn "    Ya está en modo monitor"
            fi
        done
    fi
else
    check_warn "No se puede verificar interfaz WiFi (falta comando iw)"
fi

echo ""

echo "6. VERIFICANDO ARCHIVOS DEL PROYECTO"
echo "─────────────────────────────────────────────────────────────"

if [ -f "quantum_hijack_v3.py" ]; then
    check_pass "quantum_hijack_v3.py: Presente"
    if [ -x "quantum_hijack_v3.py" ]; then
        echo "    Permisos de ejecución: OK"
    else
        check_warn "    Sin permisos de ejecución - ejecuta: chmod +x quantum_hijack_v3.py"
    fi
else
    check_fail "quantum_hijack_v3.py: NO encontrado"
fi

if [ -f "interceptor_v3.py" ]; then
    check_pass "interceptor_v3.py: Presente"
    if [ -x "interceptor_v3.py" ]; then
        echo "    Permisos de ejecución: OK"
    else
        check_warn "    Sin permisos de ejecución - ejecuta: chmod +x interceptor_v3.py"
    fi
else
    check_fail "interceptor_v3.py: NO encontrado"
fi

if [ -f "setup_v3.sh" ]; then
    check_pass "setup_v3.sh: Presente"
else
    check_warn "setup_v3.sh: NO encontrado (opcional)"
fi

if [ -f "index.html" ]; then
    check_pass "index.html: Presente (documentación)"
else
    check_warn "index.html: NO encontrado (documentación opcional)"
fi

echo ""

echo "7. VERIFICANDO PUERTOS"
echo "─────────────────────────────────────────────────────────────"

if command -v lsof &> /dev/null || command -v netstat &> /dev/null; then
    if lsof -i :8080 >/dev/null 2>&1 || netstat -tuln 2>/dev/null | grep -q ":8080"; then
        check_warn "Puerto 8080: YA EN USO - detén el proceso antes de ejecutar"
        echo "    Ejecuta: sudo lsof -i :8080 | grep LISTEN | awk '{print \$2}' | xargs sudo kill -9"
    else
        check_pass "Puerto 8080: Disponible"
    fi
else
    check_warn "No se puede verificar puertos (instala lsof o net-tools)"
fi

echo ""

echo "═══════════════════════════════════════════════════════════════"
echo "RESUMEN"
echo "═══════════════════════════════════════════════════════════════"
echo -e "${GREEN}✓ Pasadas:${NC} $PASSED"
echo -e "${YELLOW}⚠ Advertencias:${NC} $WARNINGS"
echo -e "${RED}✗ Fallos:${NC} $FAILED"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 ¡SISTEMA LISTO!${NC}"
    echo ""
    echo "PRÓXIMOS PASOS:"
    echo "1. Ejecuta: sudo python3 quantum_hijack_v3.py"
    echo "2. Abre navegador: http://localhost:8080"
    echo "3. Click en: 🔥 INICIAR TODO"
    echo ""
elif [ $FAILED -le 2 ]; then
    echo -e "${YELLOW}⚠️ SISTEMA CASI LISTO${NC}"
    echo ""
    echo "Corrige los fallos arriba antes de continuar."
    echo "Ejecuta: sudo bash setup_v3.sh"
    echo ""
else
    echo -e "${RED}❌ SISTEMA NO LISTO${NC}"
    echo ""
    echo "Hay varios requisitos faltantes."
    echo "Ejecuta: sudo bash setup_v3.sh"
    echo ""
fi

echo "⚖️  RECORDATORIO LEGAL"
echo "─────────────────────────────────────────────────────────────"
echo "Este software es SOLO para testing autorizado y fines"
echo "educativos. El uso no autorizado puede violar leyes locales."
echo "El autor NO es responsable del mal uso."
echo ""

exit $FAILED
