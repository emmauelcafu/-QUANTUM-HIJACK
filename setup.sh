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

echo "[1/4] Actualizando repositorios..."
apt update

echo "[2/4] Instalando dependencias del sistema..."
apt install -y python3-pip \
               hostapd \
               dnsmasq \
               aircrack-ng \
               wireless-tools \
               iw \
               net-tools \
               network-manager

echo "[3/4] Instalando módulos Python..."
pip3 install --upgrade pip
pip3 install flask==3.0.0 \
             scapy==2.5.0 \
             requests==2.31.0 \
             netaddr==0.10.0 \
             paramiko==3.4.0 \
             dnspython==2.4.2 \
             pycryptodome==3.19.0 \
             colorama==0.4.6

echo "[4/4] Configurando permisos..."
chmod +x quantum_hijack_full.py

echo ""
echo "✅ Setup completado correctamente!"
echo ""
echo "📡 Características instaladas:"
echo "   ✓ Detección automática de interfaces wireless"
echo "   ✓ Modo monitor automático"
echo "   ✓ Herramientas aircrack-ng completas"
echo "   ✓ API REST con control total"
echo ""
echo "📖 Ejecutar con:"
echo "   sudo python3 quantum_hijack_full.py"
echo ""
echo "⚠️  NOTA: El programa configurará automáticamente"
echo "   tu interfaz wireless en modo monitor"
echo ""
