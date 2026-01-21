# 🔓 QUANTUM-HIJACK v2.0

**Herramienta de Hacking Ético - Rogue WiFi + Interceptor**

## 📋 Descripción

QUANTUM-HIJACK es una herramienta educativa que implementa el concepto clásico de ataque WiFi rogue:

1. **WiFi Falso** - Crea un Access Point con un nombre atractivo
2. **DHCP Automático** - Asigna IPs a clientes que se conectan
3. **DNS Spoofing** - Redirige todo tráfico DNS
4. **Interceptor** - Captura credenciales de tráfico HTTP/HTTPS
5. **Dashboard Web** - Control centralizado de todo el sistema
6. **Mostrador Terminal** - Estadísticas en vivo en terminal

## ⚡ Características

- ✅ Setup automático del modo monitor
- ✅ WiFi rogue configurable (SSID, password, canal)
- ✅ Captura de credenciales en múltiples protocolos
- ✅ Dashboard web con control centralizado
- ✅ Estadísticas en vivo (clientes, credenciales, logs)
- ✅ Exportación de datos en JSON
- ✅ Detección automática de interfaz WiFi
- ✅ Procesos en background con control individual

## 🔧 Requisitos

**Sistema:**
- Kali Linux o similar
- Permisos root (sudo)
- Tarjeta WiFi con soporte a modo monitor

**Software:**
```bash
sudo apt update
sudo apt install -y python3-flask python3-scapy hostapd dnsmasq aircrack-ng iw

# Verificar instalación
python3 -c "import flask, scapy; print('✅ Dependencias OK')"
```

## 🚀 Instalación Rápida

```bash
# 1. Clonar/descargar proyecto
cd /root/Desktop/QUANTUM-HIJACK

# 2. Verificar archivos
ls -la
# Debe haber: quantum_hijack_full.py, hostapd_1.conf, dnsmasq.conf, etc.

# 3. Dar permisos de ejecución
chmod +x quantum_hijack_full.py interceptor.py dashboard_terminal.py
```

## 🎮 Ejecución

### Opción 1: Automático (Recomendado)

```bash
sudo python3 quantum_hijack_full.py
```

Luego abre en navegador:
```
http://localhost:8080
```

Presiona el botón rojo:
```
🔥 INICIAR QUANTUM-HIJACK COMPLETO
```

¡Todo se inicia automáticamente!

### Opción 2: Manual (Más control)

1. Inicia el servidor: `sudo python3 quantum_hijack_full.py`
2. Abre: `http://localhost:8080`
3. Presiona cada botón de módulo en orden:
   - [ Ejecutar ] Setup
   - [ Ejecutar ] Hostapd
   - [ Ejecutar ] Dnsmasq
   - [ Ejecutar ] Interceptor
   - [ Ejecutar ] Dashboard

## 📊 Archivos del Proyecto

| Archivo | Descripción |
|---------|------------|
| `quantum_hijack_full.py` | Backend Flask principal |
| `interceptor.py` | Capturador de credenciales |
| `dashboard_terminal.py` | Mostrador en terminal |
| `hostapd_1.conf` | Config del AP falso |
| `dnsmasq.conf` | Config de DHCP |
| `setup.sh` | Script de preparación |
| `templates/index_hijack.html` | Dashboard web |
| `logs/` | Directorio de logs |
| `GUIA_FINAL.md` | Documentación completa |

## 🔑 Credenciales WiFi

```
SSID: CafeWiFi_Quantum
Contraseña: 12345678
IP Gateway: 192.168.1.1
Rango DHCP: 192.168.1.2-100
```

## 📱 Cómo Usar

### Paso 1: Iniciar servidor
```bash
sudo python3 quantum_hijack_full.py
```

### Paso 2: Abrir dashboard
```
http://localhost:8080
```

### Paso 3: Iniciar todo
```
Presiona: 🔥 INICIAR QUANTUM-HIJACK COMPLETO
```

### Paso 4: Conectar teléfono
- Buscar WiFi: "CafeWiFi_Quantum"
- Contraseña: 12345678
- Conectarse

### Paso 5: Usar el teléfono
- Abrir navegador
- Ir a: google.com, facebook.com, gmail.com
- Intentar login
- ¡Credenciales capturadas!

### Paso 6: Ver resultados
Dashboard web muestra:
- ✓ Clientes conectados
- ✓ Credenciales capturadas
- ✓ Logs en vivo
- ✓ Protocolos detectados

## 🔍 Monitoreo en Vivo

### Terminal (Servidor Flask)
```
[INICIANDO] Setup - Modo Monitor
[INICIANDO] Hostapd - WiFi Rogue
[✓] WiFi rogue ACTIVO: CafeWiFi_Quantum
[Clientes Conectados] AA:BB:CC:DD:EE:FF
[🔥 PKO DETECTADO] user@gmail.com
```

### Dashboard Web
```
Módulos: ✅ Setup ✅ Hostapd ✅ Dnsmasq ✅ Interceptor
Clientes: 3
Credenciales: 7
Protocolo HTTPS → user@gmail.com → ••••••••
```

## 📈 Protocolos Capturados

| Protocolo | Puerto | Tipo | Uso |
|-----------|--------|------|-----|
| HTTPS | 443 | Encriptado | Webs, Gmail, Facebook |
| HTTP | 80 | Texto plano | Webs antiguas |
| FTP | 21 | Texto plano | Servidores FTP |
| SSH | 22 | Encriptado | Acceso remoto |
| MySQL | 3306 | Texto plano | Bases de datos |
| PostgreSQL | 5432 | Texto plano | Bases de datos |
| MongoDB | 27017 | Texto plano | NoSQL DB |

## 🛑 Detener el Ataque

### Opción 1: Dashboard Web
```
Botón: ⛔ DETENER TODO
```

### Opción 2: Terminal
```bash
Ctrl+C  (en la terminal del servidor)
```

## 📋 Troubleshooting

### "No se ven clientes"
```bash
# Verificar hostapd
sudo ps aux | grep hostapd

# Aumentar potencia
sudo iw wlan0mon set txpower fixed 3000

# Ver logs de hostapd
sudo grep hostapd /var/log/syslog | tail -20
```

### "Puerto 8080 ocupado"
```bash
sudo lsof -i :8080
sudo kill -9 [PID]
```

### "Modo monitor no funciona"
```bash
sudo apt install airmon-ng
sudo airmon-ng start wlan0
iw dev
```

## 📚 Documentación Completa

Ver archivo: **GUIA_FINAL.md**

Incluye:
- Flujo detallado de ejecución
- Casos de uso reales
- Customización de parámetros
- Troubleshooting completo
- Ejemplos de datos capturados
- Checklist pre-operación

## ⚖️ Consideraciones Legales

⚠️ **SOLO PARA TESTING AUTORIZADO**

- ✓ Usar en redes propias
- ✓ Usar en pentesting autorizado
- ✓ Usar en educación
- ✗ NO usar para actividades ilegales
- ✗ NO usar sin consentimiento
- ✗ Respeta las leyes locales
- ✗ La privacidad de otros

**Los logs se guardan automáticamente para auditoría.**

## 🎓 Qué Aprendes

- Conceptos de WiFi y seguridad
- Modos de monitoreo en interfaces de red
- DHCP y DNS spoofing
- Packet sniffing con Scapy
- Análisis de protocolos de red
- Desarrollo de herramientas de pentesting
- Integración Frontend/Backend
- APIs REST con Flask

## 📧 Soporte

Si tienes problemas:

1. Revisa la terminal (errores del servidor)
2. Revisa el Dashboard (logs en vivo)
3. Consulta GUIA_FINAL.md
4. Verifica que ejecutes con `sudo`
5. Verifica las dependencias instaladas

---

**🔓 QUANTUM-HIJACK v2.0** - Hacking Ético Responsable

*Emmanuel 2026*

---

## 📊 CÓMO FUNCIONA

### Arquitectura General

```
┌─────────────────────────────────────────┐
│     quantum_hijack_full.py              │
│  (Aplicación principal)                 │
├─────────────────────────────────────────┤
│  Clase QuantumHijack                    │
│  ├─ scan_network()      → Escanea LAN   │
│  ├─ start_sniffer()     → Captura datos │
│  ├─ get_status()        → Estado actual │
│  └─ check_root()        → Verifica sudo │
└─────────────────────────────────────────┘
          ↓
  ┌───────────────────┐
  │  Flask API REST   │
  │  (Puerto 8080)    │
  └───────────────────┘
          ↓
  ┌───────────────────┐
  │  Endpoints REST   │
  │  (JSON responses) │
  └───────────────────┘
```

### Flujo de Operación

1. **Verificación** → Comprueba permisos root
2. **Inicialización** → Carga configuración y estadísticas
3. **Dashboard** → Inicia servidor Flask en puerto 8080
4. **Escucha** → API REST lista para recibir comandos
5. **Ejecución** → Realiza ataques bajo demanda
6. **Reporte** → Retorna datos en JSON

---

## 🔌 API REST - Endpoints Disponibles

### 1. **Estado del Sistema**
```bash
GET /api/status
```
Retorna estado actual y lista de ataques activos.

**Respuesta:**
```json
{
  "status": "running",
  "local_ip": "192.168.1.100",
  "attacks": {
    "arp_spoofing": false,
    "dns_spoofing": false,
    "packet_sniff": false,
    "deauth": false
  },
  "stats": {
    "packets_captured": 0,
    "credentials_found": 0,
    "connected_devices": 0,
    "start_time": "2026-01-21T..."
  }
}
```

### 2. **Escanear Red**
```bash
POST /api/scan
Content-Type: application/json

{
  "network": "192.168.1.0/24"
}
```
Detecta dispositivos en la red local.

**Respuesta:**
```json
{
  "success": true,
  "devices_found": 5,
  "devices": [
    {
      "ip": "192.168.1.1",
      "mac": "00:11:22:33:44:55",
      "timestamp": "2026-01-21T..."
    }
  ]
}
```

### 3. **Iniciar Ataque**
```bash
POST /api/attacks/start
Content-Type: application/json

{
  "type": "packet_sniff"
}
```
Inicia captura de paquetes (tipos: `arp_spoofing`, `dns_spoofing`, `packet_sniff`, `deauth`).

**Respuesta:**
```json
{
  "success": true,
  "message": "Ataque packet_sniff iniciado"
}
```

### 4. **Detener Ataque**
```bash
POST /api/attacks/stop
Content-Type: application/json

{
  "type": "packet_sniff"
}
```

### 5. **Estadísticas**
```bash
GET /api/stats
```
Retorna métricas de la sesión actual.

### 6. **Dispositivos Conectados**
```bash
GET /api/devices
```
Retorna número de dispositivos detectados.

---

## 💻 EJEMPLOS DE USO

### Ejemplo 1: Iniciar el servicio
```bash
sudo python3 quantum_hijack_full.py

# Output:
# ╔════════════════════════════════════════╗
# ║     QUANTUM-HIJACK 2026 v1.0           ║
# ║     Hacking Ético - Emmanuel           ║
# ║                                        ║
# ║  ⚠️  SOLO para testing autorizado      ║
# ║  ⚠️  No usar sin permiso                ║
# ╚════════════════════════════════════════╝
#
# ✅ Iniciando dashboard en http://192.168.1.100:8080
```

### Ejemplo 2: Verificar estado (curl)
```bash
curl -s http://localhost:8080/api/status | python3 -m json.tool
```

### Ejemplo 3: Escanear red (curl)
```bash
curl -X POST http://localhost:8080/api/scan \
  -H "Content-Type: application/json" \
  -d '{"network": "192.168.1.0/24"}'
```

### Ejemplo 4: Iniciar captura (curl)
```bash
curl -X POST http://localhost:8080/api/attacks/start \
  -H "Content-Type: application/json" \
  -d '{"type": "packet_sniff"}'
```

### Ejemplo 5: Detener ataque (curl)
```bash
curl -X POST http://localhost:8080/api/attacks/stop \
  -H "Content-Type: application/json" \
  -d '{"type": "packet_sniff"}'
```

---

## 📁 ESTRUCTURA DE ARCHIVOS

| Archivo | Descripción |
|---------|-------------|
| `quantum_hijack_full.py` | Aplicación principal (260+ líneas) |
| `setup.sh` | Script de instalación automática |
| `requirements.txt` | Dependencias Python con versiones |
| `README.md` | Este archivo (documentación) |

---

## 🔧 DEPENDENCIAS INSTALADAS

```
Flask 3.0.0          - Framework web
Scapy 2.5.0          - Manipulación de paquetes
Requests 2.31.0      - Cliente HTTP
netaddr 0.10.0       - Manejo de redes
paramiko 3.4.0       - SSH/SCP
dnspython 2.4.2      - Resolución DNS
pycryptodome 3.19.0  - Criptografía
colorama 0.4.6       - Terminal coloreado
```

**Herramientas del sistema:**
- `hostapd` - Crear puntos de acceso falsos
- `dnsmasq` - Servidor DNS/DHCP
- `aircrack-ng` - Suite wireless
- `wireless-tools` - Herramientas WiFi

---

## 🎯 FUNCIONALIDADES PRINCIPALES

✅ **Escaneo de Red** - Detecta dispositivos en LAN  
✅ **Captura de Paquetes** - Monitorea tráfico en tiempo real  
✅ **ARP Spoofing** - Manipulación de tabla ARP  
✅ **DNS Spoofing** - Redirige tráfico DNS  
✅ **API REST** - Control completo via HTTP  
✅ **Dashboard** - Interfaz JSON para monitoreo  
✅ **Estadísticas** - Métricas de sesión  
✅ **Logging** - Registro de operaciones  

---

## ⚠️ NOTAS LEGALES Y DE SEGURIDAD

### ⛔ ADVERTENCIA IMPORTANTE
```
Este software está diseñado ÚNICAMENTE para:
✓ Testing de seguridad autorizado
✓ Laboratorios educativos controlados
✓ Redes propias o con permiso explícito

❌ PROHIBIDO usar para:
✗ Acceder a redes sin autorización
✗ Interceptar datos privados
✗ Robar credenciales
✗ Causar daño intencional

El autor NO es responsable de mal uso.
Cumple con todas las leyes aplicables.
```

---

## 👨‍💻 AUTOR

**Emmanuel** - Cybersecurity 2026  
Especialista en Hacking Ético

---

## 📞 SOPORTE Y CONTACTO

Para reportar errores o sugerencias, contactar directamente al autor.

---

## 📝 CHANGELOG

### v1.0 (2026-01-21)
- ✨ Implementación completa de QuantumHijack
- ✨ API REST con 6 endpoints principales
- ✨ Sistema de estadísticas
- ✨ Documentación detallada
#   - Q U A N T U M - H I J A C K 
 
 