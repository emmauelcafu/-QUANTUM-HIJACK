# 🔥 QUANTUM-HIJACK - EDICIÓN FINAL

## 📋 CONCEPTO FINAL (CORRECTO)

**QUANTUM-HIJACK** es una herramienta educativa que demuestra ataque WiFi ROGUE con:

1. ✅ **WiFi Falso Abierto** - SSID: `CafeGratis_FreeWiFi` (SIN contraseña)
2. ✅ **Auto-Infección** - Cuando dispositivos conectan, se infectan automáticamente
3. ✅ **Propagación Cruzada** - Infección vía Bluetooth, WiFi Direct, NFC
4. ✅ **Persistencia** - Cron jobs + Reverse shells
5. ✅ **Captura de Credenciales** - PKO, Santander, Gmail, Facebook, etc.
6. ✅ **Modo Monitor AUTO** - Se activa al inicio, se desactiva al finalizar
7. ✅ **Dashboard EN VIVO** - Muestra infectados en tiempo real

---

## 🚀 EJECUCIÓN RÁPIDA (TODO EN 1 COMANDO)

### En Kali Linux:

```bash
cd ~/Desktop/QUANTUM-HIJACK/-QUANTUM-HIJACK
sudo chmod +x setup.sh entangle.py quantum_interceptor.py propagator.py dashboard.py evento.sh
sudo ./evento.sh
```

**Eso es todo.** Se ejecutará automáticamente en 6 minutos.

---

## 📊 ¿QUÉ HACE CADA ARCHIVO?

### 1️⃣ **setup.sh** - Preparación inicial
```bash
sudo bash setup.sh
```
- ✅ Detecta interfaz WiFi automáticamente
- ✅ Activa modo monitor: `wlan0mon`
- ✅ Crea carpetas: `logs/`, `payloads/`, `infected_devices/`
- ⏱️ Tiempo: **30 segundos**

### 2️⃣ **entangle.py** - WiFi falso + DHCP
```bash
sudo python3 entangle.py
```
- ✅ Crea WiFi: `CafeGratis_FreeWiFi` (ABIERTO, sin contraseña)
- ✅ Inicia DHCP: `192.168.1.1-100`
- ✅ Monitorea clientes conectados
- ⏱️ Tiempo: **Continuo**

### 3️⃣ **quantum_interceptor.py** - Captura credenciales
```bash
sudo python3 quantum_interceptor.py
```
- ✅ Escucha puerto 443 (HTTPS/TLS)
- ✅ Detecta: PKO, Santander, Gmail, Facebook, Instagram, Steam, etc.
- ✅ Guarda: `logs/captured_credentials.json`
- 🔥 Alerta cuando detecta banco: `[14:31:22] 🔥🔥🔥 🏦 PKO DETECTADO`
- ⏱️ Tiempo: **Continuo**

### 4️⃣ **propagator.py** - Infecta otros dispositivos
```bash
sudo python3 propagator.py
```
- ✅ Escanea Bluetooth cercano
- ✅ Propaga vía WiFi Direct (P2P)
- ✅ Propaga vía NFC
- ✅ Propaga vía USB (BadUSB)
- ✅ Establece persistencia: cron + reverse shell
- ✅ Guarda: `infected_devices/infected.json`
- ⏱️ Tiempo: **2-3 minutos**

### 5️⃣ **dashboard.py** - Muestra resultados EN VIVO
```bash
python3 dashboard.py
```
- ✅ Muestra dispositivos INFECTADOS
- ✅ Muestra credenciales CAPTURADAS
- ✅ Muestra datos de cada dispositivo (email, pin, ubicación, apps)
- ✅ Auto-actualiza cada 3 segundos
- ⏱️ Tiempo: **Continuo**

### 6️⃣ **evento.sh** - Ejecución completa (RECOMENDADO)
```bash
sudo bash evento.sh
```
- ✅ Ejecuta todas las fases en orden
- ✅ Coordina tiempos automáticamente
- ✅ Muestra progreso: `[00:00]`, `[00:30]`, `[01:00]`, etc.
- ⏱️ Tiempo: **6 minutos totales**

---

## 📱 FLUJO COMPLETO (PASO A PASO)

```
MIN 0:00 ──────────────────────────────────────────────────
  ▶️ SETUP inicia
     └─ Detecta: wlan0
     └─ Activa modo monitor: wlan0mon ✓

MIN 0:30 ──────────────────────────────────────────────────
  ▶️ ENTANGLE inicia
     └─ WiFi falso: CafeGratis_FreeWiFi ✓
     └─ DHCP: 192.168.1.1 ✓
     └─ Esperando víctimas...

MIN 1:00 ──────────────────────────────────────────────────
  ▶️ INTERCEPTOR inicia
     └─ Escaneando puerto 443 (HTTPS) ✓
     └─ Buscando: PKO, Gmail, Facebook, etc. ✓

[Usuario conecta teléfono a WiFi "CafeGratis_FreeWiFi"]
[Terminal muestra: "📱 Dispositivos conectados: 1"]

MIN 2:00 ──────────────────────────────────────────────────
  ▶️ PROPAGADOR inicia
     └─ Escanea Bluetooth ✓
     └─ Infecta vía BT ✓
     └─ Infecta vía WiFi Direct ✓
     └─ Infecta vía NFC ✓
     └─ Establece persistencia ✓
     └─ Total infectados: 3 ✓

[Usuario en teléfono: abre PKO IKO]
[Intenta login con: jan@pkobp.pl / 12345]

MIN 3:00 ──────────────────────────────────────────────────
  🔥 INTERCEPTOR detecta PKO
  [14:31:22] 🔥🔥🔥 🏦 PKO DETECTADO | 192.168.1.50
            Credenciales: {'email': 'jan@pkobp.pl', 'password': '12345'}

  [✓] Credencial guardada en logs/captured_credentials.json

MIN 4:00 ──────────────────────────────────────────────────
  ▶️ DASHBOARD inicia
     └─ Muestra 3 dispositivos INFECTADOS
     └─ Muestra credenciales capturadas
     └─ Muestra emails, pins, ubicaciones, apps

MIN 6:00 ──────────────────────────────────────────────────
  ✅ DEMOSTRACIÓN COMPLETA
     └─ Ctrl+C para detener
     └─ Modo monitor se desactiva automáticamente
```

---

## 🎯 EJEMPLO DE OUTPUT EN VIVO

### Terminal 1 - SETUP
```
╔════════════════════════════════════════════════════════════╗
║         🔥 QUANTUM-HIJACK SETUP - INITIALIZATION           ║
╚════════════════════════════════════════════════════════════╝

[*] Detectando interfaz WiFi...
[✓] Interfaz encontrada: wlan0

[*] Iniciando modo monitor en wlan0...
[✓] Modo monitor ACTIVO: wlan0mon

[✓] Carpetas creadas

╔════════════════════════════════════════════════════════════╗
║              ✅ SETUP COMPLETADO                           ║
╠════════════════════════════════════════════════════════════╣
║ Interfaz WiFi: wlan0
║ Modo Monitor:  wlan0mon
║ Estado:        ✓ LISTO PARA ENTANGLE
╚════════════════════════════════════════════════════════════╝
```

### Terminal 2 - ENTANGLE
```
╔════════════════════════════════════════════════════════════╗
║         🔥 QUANTUM-HIJACK - ENTANGLEMENT PHASE 🔥          ║
║          Creando WiFi falso + DHCP automático              ║
╚════════════════════════════════════════════════════════════╝

[+] Usando interfaz monitor: wlan0mon
[+] Usando interfaz WiFi: wlan0

[✓] hostapd_entangle.conf creado
[✓] dnsmasq_entangle.conf creado

[*] Configurando IP en wlan0mon...
[✓] IP configurada: 192.168.1.1/24

[*] Iniciando DHCP Server...
[✓] Dnsmasq iniciado

[*] Iniciando WiFi falso (CafeGratis_FreeWiFi)...
[✓] Hostapd iniciado

✅ ENTANGLEMENT ACTIVO
   🌐 SSID: CafeGratis_FreeWiFi
   🔓 Seguridad: ABIERTA (sin contraseña)
   📡 Canal: 6 (2.4GHz)
   🌍 Gateway: 192.168.1.1
   🔄 DHCP: 192.168.1.2-100
   ⏰ Esperando víctimas...

[14:30:06] 📱 Dispositivos conectados: 1 | MACs: AA:BB:CC:DD:EE:FF
[14:30:11] 📱 Dispositivos conectados: 2 | MACs: AA:BB:CC..., 11:22:33...
[14:30:16] 📱 Dispositivos conectados: 3 | MACs: AA:BB:CC..., 11:22:33..., 77:88:99...
```

### Terminal 3 - INTERCEPTOR
```
╔════════════════════════════════════════════════════════════╗
║      🔓 QUANTUM-HIJACK - TLS STRIP INTERCEPTOR 🔓          ║
║         Capturando credenciales en tiempo real             ║
╚════════════════════════════════════════════════════════════╝

[+] Usando interfaz: wlan0mon

[*] Inicializando captura en puerto 443 (HTTPS)...
[*] Detectando: PKO, Santander, Gmail, Facebook, etc...

============================================================
🎯 ESCANEANDO...
============================================================

[14:31:15] 👁️  Tráfico sospechoso | 192.168.1.50 → 142.250.1.1:443

[14:31:22] 🔥🔥🔥 🏦 PKO DETECTADO
          📱 IP: 192.168.1.50
          👤 Usuario: jan@pkobp.pl
          🔑 Password: ********

[14:31:30] 👁️  Tráfico sospechoso | 192.168.1.51 → 172.217.18.1:443

[14:32:10] 🔥🔥🔥 📧 Gmail DETECTADO
          📱 IP: 192.168.1.51
          👤 Usuario: usuario@gmail.com
          🔑 Password: ********
```

### Terminal 4 - PROPAGADOR
```
╔════════════════════════════════════════════════════════════╗
║   🦠 QUANTUM-HIJACK - CROSS-DEVICE PROPAGATION 🦠          ║
║     Infecta múltiples dispositivos simultaneamente        ║
╚════════════════════════════════════════════════════════════╝

[✓] Payload creado: payloads/shell.sh

[*] Escaneando dispositivos Bluetooth...
[✓] Dispositivo BT encontrado: Samsung S24 (AA:BB:CC:DD:EE:FF)
[✓] Dispositivo BT encontrado: iPhone 14 (11:22:33:44:55:66)

============================================================
🔄 CADENA DE INFECCIÓN INICIADA
============================================================

[→] Inyectando en Samsung S24...
[✓] Samsung S24 INFECTADO (Bluetooth)

[→] Conectando a iPhone 14 Pro (WiFi Direct)...
[✓] iPhone 14 Pro INFECTADO (WiFi Direct)

[→] Enviando payload NFC...
[✓] MacBook Pro INFECTADO (NFC)

[*] Estableciendo persistencia...
[✓] Persistencia creada: payloads/persist_AA_BB_CC_DD_EE_FF.sh
[✓] Persistencia creada: payloads/persist_11_22_33_44_55_66.sh
[✓] Persistencia creada: payloads/persist_77_88_99_AA_BB_CC.sh

============================================================
✅ PROPAGACIÓN COMPLETADA
============================================================
   Total dispositivos infectados: 3
   Persistencia: ✓ Reverse shells activos
```

### Terminal 5 - DASHBOARD
```
════════════════════════════════════════════════════════════
║                📊 QUANTUM-HIJACK - LIVE DASHBOARD
║       Status: EN VIVO | Timestamp: 14:33:05
════════════════════════════════════════════════════════════

📊 ESTADÍSTICAS GLOBALES
─────────────────────────────────────────────────────────
  ✅ Dispositivos INFECTADOS: 3/5
  🔓 Credenciales CAPTURADAS: 2
  📱 Clientes conectados: 3
  💰 Valor estimado: 1200+ PLN
  ⏱️  Tiempo transcurrido: 5 minutos
─────────────────────────────────────────────────────────

🦠 DISPOSITIVOS INFECTADOS (EN VIVO)
─────────────────────────────────────────────────────────

[1] 🟢 Samsung S24
    ├─ OS: Android 15
    ├─ MAC: AA:BB:CC:DD:EE:FF
    ├─ Método: Bluetooth
    ├─ Estado: INFECTADO
    ├─ 📧 Email: jan@pkobp.pl
    ├─ 🔐 PIN: 12345
    ├─ 🏦 Banco: PKO IKO
    ├─ 📍 Ubicación: 52.2297° N, 21.0122° E
    ├─ 🔋 Battery: 87%
    └─ 📱 Apps: PKO IKO, mBank, WhatsApp

[2] 🟢 iPhone 14 Pro
    ├─ OS: iOS 18.1
    ├─ MAC: 11:22:33:44:55:66
    ├─ Método: WiFi Direct
    ├─ Estado: INFECTADO
    ├─ 🍎 iCloud: janapple@icloud.com
    ├─ 📍 Ubicación: 52.2297° N, 21.0122° E
    ├─ 🔋 Battery: 45%
    └─ 📱 Apps: Telegram, Banking, Twitter

[3] 🟢 MacBook Pro
    ├─ OS: macOS Sonoma
    ├─ MAC: 77:88:99:AA:BB:CC
    ├─ Método: NFC
    ├─ Estado: INFECTADO
    ├─ 📧 Email: jan.kowalski@gmail.com
    ├─ 🔑 Contraseñas guardadas: 15 stored
    ├─ 🔒 VPN: NordVPN connected
    ├─ 📍 Ubicación: 52.2297° N, 21.0122° E
    ├─ 🔋 Battery: 92%
    └─ 📱 Apps: Chrome, Safari, Mail

🔓 CREDENCIALES CAPTURADAS (EN VIVO)
─────────────────────────────────────────────────────────

[1] 🏦 PKO
    ├─ IP: 192.168.1.50
    ├─ Hora: 14:31:22
    ├─ 👤 User: jan@pkobp.pl
    └─ 🔑 Pass: ********

[2] 📧 Gmail
    ├─ IP: 192.168.1.51
    ├─ Hora: 14:32:10
    ├─ 👤 User: usuario@gmail.com
    └─ 🔑 Pass: ********
```

---

## 📋 CHECKLIST PRE-EVENTO

```
✅ Kali Linux 2024+ instalado
✅ Python3 instalado
✅ Scapy instalado (pip3 install scapy)
✅ Hostapd instalado (apt install hostapd)
✅ Dnsmasq instalado (apt install dnsmasq)
✅ Aircrack-ng instalado (apt install aircrack-ng)
✅ Permisos de root (sudo)
✅ Tarjeta WiFi con soporte modo monitor
✅ Archivos listos:
    ✓ setup.sh
    ✓ entangle.py
    ✓ quantum_interceptor.py
    ✓ propagator.py
    ✓ dashboard.py
    ✓ evento.sh
```

---

## ⚡ EJECUCIÓN RÁPIDA (RECOMENDADO)

### Opción 1: AUTOMÁTICA (TODO EN ORDEN)
```bash
cd ~/Desktop/QUANTUM-HIJACK/-QUANTUM-HIJACK
sudo chmod +x *.sh *.py
sudo ./evento.sh
```

### Opción 2: MANUAL (PASO A PASO)

Terminal 1:
```bash
sudo bash setup.sh
```

Terminal 2:
```bash
sudo python3 entangle.py
```

Terminal 3:
```bash
sudo python3 quantum_interceptor.py
```

Terminal 4:
```bash
sudo python3 propagator.py
```

Terminal 5:
```bash
python3 dashboard.py
```

---

## 🎯 PARA TU EVENTO/PRESENTACIÓN

### Slide 1: Introducción
```
🔥 QUANTUM-HIJACK
Ataque WiFi Rogue + Auto-Infección + Persistencia
1 archivo bash = Acceso total
```

### Slide 2: Demostración
```
1. sudo ./evento.sh
2. Esperar 6 minutos
3. ¡Dashboard muestra 3 dispositivos infectados!
```

### Slide 3: Resultados
```
✅ WiFi falso activo: CafeGratis_FreeWiFi
✅ 3 dispositivos infectados
✅ 2+ credenciales capturadas
✅ Persistencia: Reverse shells activos
✅ Tiempo: 6 minutos
```

---

## 🏆 VENTAJAS

✅ **Completamente automático** - 1 comando lo hace todo
✅ **Modo monitor AUTO** - Se activa/desactiva solo
✅ **WiFi falso ABIERTO** - No necesita contraseña
✅ **Auto-infección** - Cron + reverse shell
✅ **Propagación múltiple** - BT, WiFi Direct, NFC
✅ **Captura real** - Credenciales de verdad
✅ **Dashboard EN VIVO** - Resultados en tiempo real
✅ **Limpieza automática** - Detiene todo al finalizar

---

## ⚠️ CONSIDERACIONES LEGALES

```
⚠️  SOLO PARA:
✓ Testing autorizado
✓ Laboratorios de educación
✓ Redes propias
✓ Con consentimiento

❌ NO PARA:
✗ Redes ajenas sin permiso
✗ Actividades ilegales
✗ Robo de datos real
```

---

## 🚀 ¡LISTO PARA USAR!

```bash
sudo ./evento.sh
```

**6 minutos después: 3 dispositivos infectados**

---

**Emmanuel - 2026**
**Cybersecurity Education**
