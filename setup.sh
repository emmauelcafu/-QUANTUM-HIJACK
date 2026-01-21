#!/bin/bash
# QUANTUM-HIJACK SETUP SCRIPT
# Emmanuel 2026

echo "🔥 QUANTUM-HIJACK SETUP"
echo "======================"
echo ""

# Verificar si es root
if [ "$EUID" -ne 0 ]; then 
   echo "❌ Ejecutar como: sudo bash setup.sh"
   exit 1
fi

echo "[1/3] Instalando dependencias..."
apt update
apt install -y python3-pip hostapd dnsmasq aircrack-ng wireless-tools iw

echo "[2/3] Instalando módulos Python..."
pip3 install flask scapy

echo "[3/3] Permisos ejecutables..."
chmod +x quantum_hijack_full.py

echo ""
echo "✅ Setup completado!"
echo ""
echo "📖 Ejecutar con:"
echo "   sudo python3 quantum_hijack_full.py"
echo ""
