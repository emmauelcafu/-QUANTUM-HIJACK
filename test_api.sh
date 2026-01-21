#!/bin/bash
# Script de prueba para QUANTUM-HIJACK API
# Emmanuel 2026

API_URL="http://localhost:8080"

echo "╔════════════════════════════════════════╗"
echo "║  QUANTUM-HIJACK API TEST SCRIPT        ║"
echo "╚════════════════════════════════════════╝"
echo ""

# Test 1: Estado del sistema
echo "[TEST 1] Verificando estado del sistema..."
curl -s ${API_URL}/api/status | python3 -m json.tool
echo ""
echo "─────────────────────────────────────────"
echo ""

# Test 2: Estado del modo monitor
echo "[TEST 2] Verificando modo monitor..."
curl -s ${API_URL}/api/monitor | python3 -m json.tool
echo ""
echo "─────────────────────────────────────────"
echo ""

# Test 3: Estadísticas
echo "[TEST 3] Obteniendo estadísticas..."
curl -s ${API_URL}/api/stats | python3 -m json.tool
echo ""
echo "─────────────────────────────────────────"
echo ""

# Test 4: Escanear red
echo "[TEST 4] Escaneando red (esto puede tomar unos segundos)..."
curl -s -X POST ${API_URL}/api/scan \
     -H "Content-Type: application/json" \
     -d '{"network": "192.168.1.0/24"}' | python3 -m json.tool
echo ""
echo "─────────────────────────────────────────"
echo ""

# Test 5: Dispositivos
echo "[TEST 5] Consultando dispositivos detectados..."
curl -s ${API_URL}/api/devices | python3 -m json.tool
echo ""
echo "─────────────────────────────────────────"
echo ""

echo "✅ Tests completados"
echo ""
echo "💡 Endpoints disponibles:"
echo "   GET  ${API_URL}/api/status"
echo "   GET  ${API_URL}/api/monitor"
echo "   GET  ${API_URL}/api/stats"
echo "   GET  ${API_URL}/api/devices"
echo "   POST ${API_URL}/api/scan"
echo "   POST ${API_URL}/api/attacks/start"
echo "   POST ${API_URL}/api/attacks/stop"
echo "   POST ${API_URL}/api/monitor/enable"
echo "   POST ${API_URL}/api/monitor/disable"
echo ""
