# 🔓 QUANTUM-HIJACK v2.0 - GUÍA FINAL COMPLETA

## 📋 RESUMEN EJECUTIVO

**QUANTUM-HIJACK v2.0** es una herramienta de hacking ético que implementa el concepto ORIGINAL de **Rogue WiFi + Interception**:

1. **Setup** → Antena a modo monitor
2. **Hostapd** → WiFi falso (CafeWiFi_Quantum)
3. **Dnsmasq** → DHCP + DNS spoofing
4. **Interceptor** → Captura de credenciales en vivo
5. **Dashboard** → Mostrador terminal en tiempo real
6. **Web Control** → Panel web para controlar todo

---

## 🚀 INSTALACIÓN EN KALI LINUX

### Paso 1: Verificar dependencias

```bash
sudo apt update
sudo apt install -y python3-flask python3-pip hostapd dnsmasq airmon-ng scapy iw
pip3 install flask-cors
```

### Paso 2: Navegar al proyecto

```bash
cd /root/Desktop/QUANTUM-HIJACK
ls -la
```

**Debería ver:**
```
setup.sh                 ← Script de setup
hostapd_1.conf          ← Config del AP falso
dnsmasq.conf            ← Config de DHCP
interceptor.py          ← Capturador de credenciales
dashboard_terminal.py   ← Mostrador en terminal
quantum_hijack_full.py  ← Backend Flask (PRINCIPAL)
templates/index_hijack.html  ← Dashboard web
requirements.txt        ← Dependencias Python
```

---

## 🎯 FLUJO DE EJECUCIÓN

### OPCIÓN 1: AUTOMÁTICO (Recomendado)

**Terminal 1 - Inicio del servidor:**
```bash
cd /root/Desktop/QUANTUM-HIJACK
sudo python3 quantum_hijack_full.py
```

**Verás:**
```
══════════════════════════════════════════════════════════
  🔓 QUANTUM-HIJACK v2.0 - ROGUE WIFI + INTERCEPTOR
  Control centralizado del concepto completo
══════════════════════════════════════════════════════════

📡 CONFIGURACIÓN
══════════════════════════════════════════════════════════
  WiFi Interface: wlan0
  Monitor Mode: wlan0mon
  SSID: CafeWiFi_Quantum
  Password: 12345678
  Gateway: 192.168.1.1

🌐 WEB DASHBOARD
══════════════════════════════════════════════════════════
  → http://localhost:8080
```

**Navegador - Panel Web:**
```
http://localhost:8080
```

**Botón Rojo GRANDE:**
```
🔥 INICIAR QUANTUM-HIJACK COMPLETO
```

Presiona el botón y se ejecutarán automáticamente:
- ✓ Setup (Modo Monitor)
- ✓ Hostapd (WiFi Falso)
- ✓ Dnsmasq (DHCP)
- ✓ Interceptor (Captura)
- ✓ Dashboard Terminal

---

### OPCIÓN 2: MANUAL (Más control)

**Terminal 1:**
```bash
sudo python3 quantum_hijack_full.py
```

**Navegador:**
```
http://localhost:8080
```

Luego presiona cada botón en orden:
1. [ Ejecutar ] en módulo "Setup"
2. [ Ejecutar ] en módulo "Hostapd"
3. [ Ejecutar ] en módulo "Dnsmasq"
4. [ Ejecutar ] en módulo "Interceptor"
5. [ Ejecutar ] en módulo "Dashboard"

---

## 📊 QUÉ VER EN CADA PANTALLA

### Dashboard Web (http://localhost:8080)

```
HEADER:
  SSID: CafeWiFi_Quantum
  Gateway: 192.168.1.1
  Clientes: 0 (va aumentando)
  Credenciales: 0 (se capturan)

MÓDULOS (Estado en vivo):
  ☑ Setup        ← Verde = ✓ ACTIVO
  ☑ Hostapd      ← Verde = ✓ ACTIVO
  ☑ Dnsmasq      ← Verde = ✓ ACTIVO
  ☑ Interceptor  ← Verde = ✓ ACTIVO
  ☑ Dashboard    ← Verde = ✓ ACTIVO

TABLAS:
  📱 Clientes Conectados
     └─ MAC | IP | Conectado | Señal
  
  🔥 Credenciales Capturadas
     └─ Hora | Protocolo | Usuario | Contraseña | Origen
  
  📋 Operaciones en Vivo
     └─ Logs de todo lo que está pasando
```

---

## 🔌 CÓMO FUNCIONA EL ATAQUE

### Paso 1: Teléfono se conecta al WiFi

```
Teléfono:
  ├─ Busca redes WiFi
  ├─ Ve: "CafeWiFi_Quantum"
  ├─ Se conecta (pass: 12345678)
  └─ Obtiene IP: 192.168.1.X (de dnsmasq)
```

### Paso 2: Dashboard detecta cliente

```
Panel Web:
  📱 Clientes Conectados: 1 ↑
  └─ MAC: AA:BB:CC:DD:EE:FF
     IP: 192.168.1.5
     Conectado: 14:23:45
```

### Paso 3: Usuario navega a Google/Facebook

```
Teléfono:
  └─ Usuario abre Chrome
  └─ Navega: google.com
  └─ Intenta login
```

### Paso 4: Interceptor captura credenciales

```
Dashboard Web - Credenciales:
  [14:24:10] HTTPS
    usuario@gmail.com
    p@ssw0rd123
    Origen: 192.168.1.5:52341
```

---

## 🔑 CREDENCIALES CAPTURADAS

El interceptor detecta automáticamente:

| Protocolo | Puertos | Tipo | Ejemplo |
|-----------|---------|------|---------|
| **HTTPS** | 443 | Encriptado | Facebook, Gmail, Instagram |
| **HTTP** | 80 | Texto plano | Cualquier web antigua |
| **FTP** | 21 | Usuario:Pass | Servidores FTP |
| **SSH** | 22 | Credenciales | Acceso remoto |
| **MySQL** | 3306 | BD | Conexiones DB |
| **PostgreSQL** | 5432 | BD | Conexiones DB |
| **MongoDB** | 27017 | BD | Conexiones DB |

---

## 📱 CASOS DE USO

### Caso 1: Capturar credenciales de WiFi gratis

```
┌─ Café WiFi Falso ─────────────────┐
│ SSID: CafeWiFi_Quantum            │
│ Password: 12345678                │
│ Signal: -50dBm (muy fuerte)       │
└───────────────────────────────────┘
         │
         ├─ Cliente 1 se conecta
         ├─ Cliente 2 se conecta
         └─ Cliente 3 se conecta
         
Resultado: 3 clientes, 5 credenciales capturadas
```

### Caso 2: Monitoreo en eventos

```
Estadio de fútbol:
  └─ Desplegamos WiFi rogue
  └─ 50+ teléfonos se conectan
  └─ Capturamos credenciales en vivo
  └─ Exportamos datos (JSON)
```

### Caso 3: Pentesting corporativo

```
Empresa Cliente:
  └─ Implementamos WiFi rogue
  └─ Testamos seguridad
  └─ Generamos reporte
  └─ Recomendamos mitigaciones
```

---

## 🎮 CONTROLES DEL DASHBOARD

### Botones de Módulo

```
[ Ejecutar ]   ← Inicia ese módulo
[ Detener ]    ← Detiene ese módulo
[ Estado ]     ← Muestra estado actual
```

### Botón Global

```
🔥 INICIAR QUANTUM-HIJACK COMPLETO
   └─ Ejecuta todo en secuencia correcta
   └─ Setup → Hostapd → Dnsmasq → Interceptor → Dashboard
```

```
⛔ DETENER TODO
   └─ Para todos los módulos gracefully
   └─ Limpia procesos
   └─ Cierra conexiones
```

---

## 📊 MONITOREO EN VIVO

### Terminal 1 (Flask Server)
```bash
[2026-01-21 14:23:10] [INFO] Iniciando QUANTUM-HIJACK Backend...
[2026-01-21 14:23:12] [SUCCESS] Interfaz WiFi detectada: wlan0
[2026-01-21 14:23:15] [PROCESS] [INICIANDO] Setup - Modo Monitor
[2026-01-21 14:23:18] [STEP] Bajando interfaz wlan0...
[2026-01-21 14:23:20] [SUCCESS] [✓] Setup completado
```

### Terminal 2 (Hostapd - en segundo plano)
```bash
wlan0mon: interface mode change from station to master
...
wlan0mon: STA aa:bb:cc:dd:ee:ff IEEE 802.11: authenticated
wlan0mon: STA aa:bb:cc:dd:ee:ff IEEE 802.11: associated
```

### Terminal 3 (Interceptor - en segundo plano)
```bash
[14:24:10] HTTPS | 192.168.1.5 → 142.250.80.46:443
          Credenciales: {'email': 'user@gmail.com', 'password': 'secret123'}
```

### Dashboard Web (Actualiza cada 2s)
```
✓ Setup       ACTIVO
✓ Hostapd     ACTIVO
✓ Dnsmasq     ACTIVO
✓ Interceptor ACTIVO
✓ Dashboard   ACTIVO

Clientes: 3
Credenciales: 7
```

---

## 🔍 TROUBLESHOOTING

### "No se ve ningún cliente"

**Causa:** Clientes no se conectan al WiFi falso

**Solución:**
```bash
# 1. Verificar que hostapd está corriendo
sudo ps aux | grep hostapd

# 2. Ver si hay errores
sudo grep hostapd /var/log/syslog | tail -20

# 3. Aumentar potencia de señal
sudo iw wlan0mon set txpower fixed 3000

# 4. Cambiar canal
# Editar hostapd_1.conf:
#   channel=6  →  channel=11  (menos usado)
```

### "Puerto 8080 ya en uso"

```bash
# Encontrar proceso
sudo lsof -i :8080

# Matar proceso
sudo kill -9 [PID]

# O cambiar puerto en quantum_hijack_full.py
# app.run(host='0.0.0.0', port=8081)
```

### "Modo monitor no se activa"

```bash
# Verificar que airmon-ng esté instalado
sudo apt install airmon-ng

# Ver interfaces
iw dev

# Forzar modo monitor
sudo ip link set wlan0 down
sudo iw wlan0 set type monitor
sudo ip link set wlan0 up
```

### "Dnsmasq no asigna IPs"

```bash
# Verificar configuración
sudo cat /etc/dnsmasq.conf

# Reiniciar
sudo systemctl restart dnsmasq

# Ver logs
sudo tail -f /var/log/dnsmasq.log
```

---

## 📈 FLUJO COMPLETO VISUAL

```
[1] USUARIO PRESIONA: 🔥 INICIAR QUANTUM-HIJACK COMPLETO
    ↓
[2] Backend ejecuta en orden:
    ├─ init_setup()         → Modo monitor activado
    ├─ init_hostapd()       → WiFi falso en aire
    ├─ init_dnsmasq()       → DHCP listo
    ├─ init_interceptor()   → Sniffing activo
    └─ init_dashboard()     → Terminal actualizada
    ↓
[3] Dashboard Web actualiza (cada 2 segundos):
    ├─ GET /api/status      → Estados de módulos
    ├─ GET /api/clients     → Clientes conectados
    ├─ GET /api/credentials → Credenciales capturadas
    └─ GET /api/logs        → Operaciones en vivo
    ↓
[4] Teléfono se conecta a WiFi:
    ├─ Busca "CafeWiFi_Quantum"
    ├─ Se conecta (12345678)
    ├─ Obtiene IP: 192.168.1.5 (dnsmasq DHCP)
    └─ Aparece en Dashboard Web
    ↓
[5] Usuario navega web:
    ├─ Intenta login: gmail.com
    ├─ Envía: user@gmail.com + password123
    └─ Interceptor lo captura
    ↓
[6] Dashboard Web muestra:
    🔥 CREDENCIALES CAPTURADAS
    [14:24:10] HTTPS
      user@gmail.com
      ••••••••••
      Origen: 192.168.1.5:52341
    ↓
[7] Admin presiona: 💾 EXPORTAR JSON
    └─ export_20260121_142445.json descargado
```

---

## 💾 EXPORTAR DATOS

### Opción 1: Dashboard Web
```
Botón: 💾 EXPORTAR JSON
└─ Descarga automáticamente:
   export_20260121_142445.json
```

### Opción 2: API directo
```bash
curl http://localhost:8080/api/export > datos.json
```

### Contenido del export:
```json
{
  "timestamp": "2026-01-21T14:24:45.123456",
  "state": {
    "setup_done": true,
    "hostapd_running": true,
    "dnsmasq_running": true,
    "interceptor_running": true,
    "clients_connected": 3,
    "credentials_captured": 7
  },
  "clients": [
    {"mac": "AA:BB:CC:DD:EE:FF", "ip": "192.168.1.5", ...}
  ],
  "credentials": [
    {"timestamp": "14:24:10", "protocol": "HTTPS", "username": "user@gmail.com", ...}
  ],
  "logs": [
    "[14:23:10] [INFO] Iniciando...",
    "[14:23:15] [SUCCESS] Setup completado"
  ]
}
```

---

## ⚖️ NOTAS LEGALES

⚠️ **SOLO PARA TESTING AUTORIZADO**

- Solo usar en redes que controlas
- Solo para educación y pentesting autorizado
- Respeta leyes locales sobre privacidad
- Los registros son guardados automáticamente
- Obtén consentimiento antes de cualquier test

---

## 🎓 EDUCACIÓN

**¿Qué aprendes?**
- Modo monitor en WiFi
- Creación de Access Points falsos
- DHCP y DNS spoofing
- Packet sniffing con Scapy
- Captura de credenciales
- Arquitectura de hacking tools
- Frontend/Backend integration
- API REST con Flask

**¿Por qué es importante?**
- Entender vulnerabilidades WiFi
- Defenderse contra ataques similares
- Pentest en entornos autorizados
- Investigación de seguridad

---

## 🔧 PERSONALIZACIÓN

### Cambiar SSID

Edita `quantum_hijack_full.py`:
```python
state = {
    'ssid': 'MiWiFi_Personalizado',  # ← Cambiar aquí
    ...
}
```

### Cambiar contraseña

```python
state = {
    'password': 'mipassword123',  # ← Cambiar aquí
    ...
}
```

### Cambiar canal WiFi

Edita `hostapd_1.conf`:
```
channel=6     # 1-14 disponibles (menos usado = menos interferencia)
```

---

## ✅ CHECKLIST PRE-OPERACIÓN

- [ ] Estoy en Kali Linux
- [ ] Tengo permisos root (sudo)
- [ ] WiFi está conectada
- [ ] `quantum_hijack_full.py` en el directorio correcto
- [ ] Archivos .conf presentes (hostapd_1.conf, dnsmasq.conf)
- [ ] Scripts Python presentes (interceptor.py, dashboard_terminal.py)
- [ ] Flask instalado (`pip3 install flask flask-cors`)
- [ ] Dependencias del sistema (`apt install hostapd dnsmasq airmon-ng`)
- [ ] Puerto 8080 disponible (`sudo lsof -i :8080`)
- [ ] Terminal con buena visibilidad de logs

---

## 🚀 EJECUCIÓN RÁPIDA

```bash
# 1. En Kali
cd /root/Desktop/QUANTUM-HIJACK
sudo python3 quantum_hijack_full.py

# 2. En navegador
http://localhost:8080

# 3. Presiona el botón rojo
🔥 INICIAR QUANTUM-HIJACK COMPLETO

# 4. Espera a que todo esté verde ✓

# 5. Teléfono se conecta a "CafeWiFi_Quantum"
# Password: 12345678

# 6. Navega web en el teléfono
# gmail.com, facebook.com, etc.

# 7. Ve las credenciales en el dashboard

# 8. Presiona "⛔ DETENER TODO" cuando termines
```

---

## 📞 SOPORTE

Si algo falla:

1. Revisa la terminal de Flask (errores)
2. Revisa el Dashboard Web (logs)
3. Verifica que estés en Kali Linux
4. Verifica que ejecutes con `sudo`
5. Verifica que las dependencias estén instaladas

---

**¡LISTO PARA USAR!** 🔓

Cualquier duda o problema, consulta los logs en vivo en el dashboard.
