# 🔥 QUANTUM-HIJACK v3.0 - WiFi Rogue + Infectar + Persistir

**Herramienta de Hacking Ético Avanzada**

Emmanuel - 2026

---

## 📋 ¿QUÉ HACE?

```
1. ✅ Modo Monitor AUTOMÁTICO (ON/OFF)
2. ✅ WiFi ABIERTO (sin contraseña) - Auto-conectar
3. ✅ DHCP automático (192.168.1.x)
4. ✅ Interceptar credenciales (emails, bancos, etc)
5. ✅ INFECTAR dispositivos (payload)
6. ✅ PERSISTENCIA (reverse shell cron)
7. ✅ Dashboard cyberpunk EN VIVO
8. ✅ Auto-limpiar al salir (Ctrl+C)
```

---

## ⚡ INSTALACIÓN RÁPIDA

```bash
# 1. Clonar/descargar proyecto
cd ~/Desktop/QUANTUM-HIJACK-v3

# 2. Instalar dependencias
sudo bash setup_v3.sh

# 3. Dar permisos
chmod +x quantum_hijack_v3.py interceptor_v3.py

# 4. EJECUTAR
sudo python3 quantum_hijack_v3.py

# 5. Abrir navegador
http://localhost:8080
```

---

## 🎮 USO EN DEMO (5 MINUTOS)

### MIN 0:00 - Iniciar servidor
```bash
sudo python3 quantum_hijack_v3.py
```

Output:
```
╔═══════════════════════════════════════════════════════╗
║  🔥 QUANTUM-HIJACK v3.0 - WiFi Rogue + Infectar     ║
╚═══════════════════════════════════════════════════════╝

📡 CONFIGURACIÓN
 WiFi Interface: wlan0
 Monitor Mode: wlan0mon
 SSID: CafeGratis_FreeWiFi
 Password: ABIERTO (sin contraseña)
 Gateway: 192.168.1.1

🌐 WEB DASHBOARD
 → http://localhost:8080
```

### MIN 0:30 - Abrir dashboard
Abre navegador: **http://localhost:8080**

Dashboard aparece con todos los botones.

### MIN 1:00 - INICIAR TODO
Click en botón: **🔥 INICIAR TODO**

Secuencia automática:
1. ✅ Setup - Modo monitor activado
2. ✅ Hostapd - WiFi "CafeGratis_FreeWiFi" en el aire
3. ✅ Dnsmasq - DHCP asignando IPs
4. ✅ Interceptor - Escuchando puertos 80,443,21,22,3306,5432

### MIN 2:00 - Conectar teléfono
- Abrir WiFi en teléfono
- Buscar: **"CafeGratis_FreeWiFi"**
- SIN CONTRASEÑA → Click conectar
- Auto-conecta (CERO interacción víctima)

### MIN 2:30 - Víctima navega
- Abre navegador
- Entra a: Gmail / Facebook / PKO / Instagram
- Intenta hacer login

### MIN 3:00 - INFECTAR
Dashboard muestra:
```
📱 Clientes Conectados: 1
🔥 Dispositivos INFECTADOS: 1
  IP: 192.168.1.50
  MAC: AA:BB:CC:DD:EE:FF
  Type: Android
  Status: 🔥 INFECTADO
  Reverse Shell: 192.168.1.1:4444
```

### MIN 3:30 - Ver credenciales
Dashboard actualiza LIVE:
```
🔓 Credenciales Capturadas: 3
  
[1] 14:35:20 | HTTPS | Gmail
  user@gmail.com / password123

[2] 14:35:45 | HTTP | Facebook
  usuario / pass456

[3] 14:36:10 | HTTPS | PKO
  jan.kowalski@gmail.com / pkopwd789
```

### MIN 4:00 - Descargar
- Click: **⬇️ Descargar TXT** (infected_devices.txt)
- Click: **📦 Descargar TODO ZIP** (quantum_loot.zip)

Archivos incluyen:
- `infected_devices.txt` - Dispositivos comprometidos
- `credentials.json` - Credenciales capturadas
- `operation_logs.json` - Logs completos
- `RESUMEN.txt` - Resumen ejecutivo

### MIN 4:30 - DETENER
```bash
# En dashboard: Click ⛔ DETENER TODO
```

O en terminal:
```bash
Ctrl+C
```

**Automáticamente:**
1. ✅ Detiene hostapd
2. ✅ Detiene dnsmasq
3. ✅ Detiene interceptor
4. ✅ Desactiva modo monitor (wlan0mon → wlan0 managed)
5. ✅ Restaura interfaz normal
6. ✅ Reinicia NetworkManager

---

## 📁 ESTRUCTURA DE ARCHIVOS

```
quantum_hijack_v3/
├── quantum_hijack_v3.py      # MAIN (600+ líneas)
├── interceptor_v3.py          # Capturador de credenciales
├── setup_v3.sh                # Instalación automática
├── README.md                  # Este archivo
├── payloads/                  # (creado auto)
│   ├── android_payload.bin
│   ├── windows_payload.exe
│   └── ios_payload.bin
├── logs/                      # (creado auto)
│   ├── infected_devices.json
│   ├── captured_credentials.json
│   └── operation_logs.json
└── capture/                   # (creado auto)
```

---

## 🔧 CARACTERÍSTICAS PRINCIPALES

### 1️⃣ **Modo Monitor AUTOMÁTICO**
```
Setup automático:
- Detecta interfaz WiFi (wlan0, wlan1, etc)
- Mata procesos conflictivos
- Activa modo monitor (airmon-ng)
- Configuración IP automática

Al salir (Ctrl+C):
- Desactiva modo monitor
- Restaura interfaz a managed
- Reinicia NetworkManager
```

### 2️⃣ **WiFi ABIERTO (Sin contraseña)**
```
SSID: CafeGratis_FreeWiFi
Password: (VACÍO)
Resultado: Auto-conectar sin interacción

Víctima SOLO ve WiFi y conecta
```

### 3️⃣ **DHCP + DNS Spoof**
```
IP Gateway: 192.168.1.1
Rango DHCP: 192.168.1.2-100
DNS Spoof: TODO tráfico → 192.168.1.1
Resultado: Máximo control de la red
```

### 4️⃣ **Interceptor de Credenciales**
```
Monitorea puertos:
- 80 (HTTP) - Formularios web
- 443 (HTTPS) - Secure connections
- 21 (FTP) - File Transfer
- 22 (SSH) - Remote access
- 3306 (MySQL) - Databases
- 5432 (PostgreSQL) - Databases
- 27017 (MongoDB) - NoSQL

Detecta:
- Bancos: PKO, Santander, mBank, ING
- Email: Gmail, Outlook, Yahoo
- Redes: Facebook, Instagram, Twitter, LinkedIn
- Otros: WhatsApp Web, Allegro
```

### 5️⃣ **INFECTAR Dispositivos**
```
Auto-detecta tipo:
- Android
- iPhone/iOS
- Windows
- Linux
- Mac

Inyecta payload vía DNS spoof:
- google.com → payload.apk
- facebook.com → payload.exe
```

### 6️⃣ **PERSISTENCIA**
```
Reverse shell permanente:
- Cron job @reboot
- Conexión automática 192.168.1.1:4444
- Supervivencia después de reboot
```

### 7️⃣ **Dashboard Profesional**
```
EN VIVO (auto-actualiza cada 2 seg):
- Estado módulos (on/off)
- Clientes conectados
- Dispositivos INFECTADOS
- Credenciales capturadas
- Logs operacionales
- Botones de control
- Descargas (TXT + ZIP)
```

---

## 📊 API REST ENDPOINTS

```
GET  /api/status              → Estado actual del sistema
GET  /api/clients             → Clientes conectados
GET  /api/infected            → Dispositivos infectados
GET  /api/credentials         → Credenciales capturadas
GET  /api/logs                → Logs de operación

POST /api/init/setup          → Activar modo monitor
POST /api/init/hostapd        → Iniciar WiFi falso
POST /api/init/dnsmasq        → Iniciar DHCP
POST /api/init/interceptor    → Iniciar interceptor
POST /api/init/all            → INICIAR TODO
POST /api/stop/all            → DETENER TODO + Limpiar

POST /api/infect              → Infectar dispositivo
GET  /api/download/infected   → Descargar infectados.txt
GET  /api/download/all        → Descargar quantum_loot.zip
```

---

## ⚠️ REQUISITOS

**Sistema:**
- Kali Linux 2026 (o similar)
- Permisos root (sudo)
- Tarjeta WiFi con soporte modo monitor

**Dependencias instaladas por setup.sh:**
```
hostapd          - Access point falso
dnsmasq          - DHCP + DNS
aircrack-ng      - Herramientas wireless
wireless-tools   - Utilidades WiFi
python3-scapy    - Manipulación paquetes
flask            - Web framework
```

---

## 🎯 CASOS DE USO

✅ **Pentest autorizado** - Evaluar seguridad WiFi
✅ **Educación** - Laboratorios de seguridad
✅ **Demostración** - Mostrar vulnerabilidades
✅ **Testing interno** - Redes controladas

❌ **NO usar sin autorización**
❌ **NO en redes públicas sin permiso**
❌ **NO con intención maliciosa**

---

## 🔒 CONSIDERACIONES LEGALES

⚠️ **ADVERTENCIA IMPORTANTE**

Este software está diseñado ÚNICAMENTE para:
✓ Testing de seguridad autorizado
✓ Laboratorios educativos controlados
✓ Redes propias o con permiso explícito

**PROHIBIDO usar para:**
✗ Acceder a redes sin autorización
✗ Interceptar datos privados ilegalmente
✗ Robar credenciales
✗ Causar daño intencional

El autor NO es responsable de mal uso.
**Cumple con todas las leyes aplicables.**

---

## 🐛 TROUBLESHOOTING

### "No se ve WiFi"
```bash
# Verificar interfaz
iw dev

# Aumentar potencia
sudo iw wlan0 set txpower fixed 3000

# Revisar hostapd
sudo systemctl status hostapd
```

### "Puerto 8080 ocupado"
```bash
sudo lsof -i :8080
sudo kill -9 <PID>
```

### "Modo monitor no funciona"
```bash
# Desactivar todas las conexiones
sudo systemctl stop NetworkManager

# Iniciar manualmente
sudo airmon-ng start wlan0
```

### "Interceptor no captura"
```bash
# Verificar interfaz monitor
iw dev wlan0mon info

# Revisar privilegios
sudo python3 interceptor_v3.py
```

---

## 📞 SOPORTE

Si tienes problemas:

1. Revisa los logs en `/logs/`
2. Verifica que ejecutas con `sudo`
3. Comprueba dependencias: `apt update && sudo bash setup_v3.sh`
4. Revisa el dashboard para errores EN VIVO

---

## 👨‍💻 AUTOR

**Emmanuel** - Cybersecurity 2026
Especialista en Hacking Ético

---

## 📝 CHANGELOG

### v3.0 (2026-01-22)
✨ **COMPLETAMENTE NUEVO**
- ✅ Modo monitor AUTOMÁTICO ON/OFF
- ✅ WiFi ABIERTO (auto-conectar)
- ✅ INFECTAR dispositivos
- ✅ PERSISTENCIA (reverse shell)
- ✅ Dashboard profesional cyberpunk
- ✅ Limpieza automática al salir
- ✅ API REST completa

### v2.0 (2026-01-21)
- Captura básica de credenciales
- WiFi con contraseña
- Dashboard simple

### v1.0 (2026-01-20)
- Concepto inicial
- Setup básico

---

## 🎓 LEARNING OUTCOMES

Aprendes:
- Conceptos de WiFi y seguridad inalámbrica
- Modo monitor en interfaces wireless
- DHCP y DNS spoofing
- Packet sniffing con Scapy
- Análisis de protocolos de red
- Desarrollo de herramientas de pentesting
- Flask + REST APIs
- Automatización de hacking ético

---

**¡QUANTUM-HIJACK v3.0 - Hacking Ético Responsable!** 🔥

Emmanuel - 2026
