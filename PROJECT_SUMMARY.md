# 🎯 QUANTUM-HIJACK v1.0 - Resumen del Proyecto

## 📦 Archivos del Proyecto

```
quantum-hijack/
├── quantum_hijack_full.py  (450+ líneas) ⭐ ARCHIVO PRINCIPAL
├── setup.sh                (50 líneas)   🔧 Instalación
├── test_api.sh             (60 líneas)   🧪 Testing
├── requirements.txt        (8 líneas)    📦 Dependencias
├── README.md               (450+ líneas) 📖 Documentación
├── QUICKSTART.md           (200+ líneas) 🚀 Guía rápida
└── Inicio - Acceso directo.lnk          🔗 Atajo
```

---

## ⚡ CARACTERÍSTICAS PRINCIPALES

### 🆕 **MODO MONITOR AUTOMÁTICO**

✅ **Detección automática** de interfaces wireless  
✅ **Configuración automática** en modo monitor  
✅ **Restauración automática** al salir (Ctrl+C)  
✅ **Manejo inteligente** de procesos interferentes  
✅ **Configuración de canal** WiFi automática  

**Proceso completo:**
```
1. Detecta: wlan0, wlan1, etc.
2. Mata: NetworkManager, wpa_supplicant
3. Configura: iwconfig modo monitor
4. Verifica: Mode:Monitor activo
5. Al salir: Restaura modo managed
```

---

## 🔌 API REST - 9 Endpoints

| # | Método | Endpoint | Función |
|---|--------|----------|---------|
| 1 | GET | `/api/status` | Estado completo del sistema |
| 2 | GET | `/api/monitor` | 🆕 Info modo monitor |
| 3 | POST | `/api/monitor/enable` | 🆕 Activar modo monitor |
| 4 | POST | `/api/monitor/disable` | 🆕 Desactivar modo monitor |
| 5 | POST | `/api/scan` | Escanear red local |
| 6 | POST | `/api/attacks/start` | Iniciar ataque |
| 7 | POST | `/api/attacks/stop` | Detener ataque |
| 8 | GET | `/api/stats` | Estadísticas |
| 9 | GET | `/api/devices` | Dispositivos detectados |

---

## 🛠️ Herramientas Instaladas

### Python (pip3)
- Flask 3.0.0 - Servidor web
- Scapy 2.5.0 - Manipulación de paquetes
- Requests 2.31.0 - Cliente HTTP
- netaddr 0.10.0 - Direcciones de red
- paramiko 3.4.0 - SSH/SCP
- dnspython 2.4.2 - DNS
- pycryptodome 3.19.0 - Crypto
- colorama 0.4.6 - Colores

### Sistema (apt)
- aircrack-ng - Suite wireless
- hostapd - Access Point falso
- dnsmasq - DNS/DHCP server
- wireless-tools - iwconfig
- iw - Herramienta moderna
- net-tools - ifconfig
- network-manager - Gestión de redes

---

## 🎨 Interfaz Profesional

### Al iniciar:
```
╔════════════════════════════════════════╗
║     QUANTUM-HIJACK 2026 v1.0           ║
║     Hacking Ético - Emmanuel           ║
║                                        ║
║  ⚠️  SOLO para testing autorizado      ║
║  ⚠️  No usar sin permiso                ║
╚════════════════════════════════════════╝

[INICIALIZACIÓN]
──────────────────────────────────────────────────
🔍 Detectando interfaces wireless...
✅ Interfaces encontradas: ['wlan0']

💡 Se detectaron 1 interfaz(es) wireless:
   1. wlan0

🔧 Configurando modo monitor automáticamente...
   → Deteniendo procesos interferentes...
   → Bajando interfaz wlan0...
   → Activando modo monitor...
   → Levantando interfaz...
   → Configurando canal 6...
✅ Interfaz wlan0 lista en modo monitor

─────────────────────────────────────────────────
[DASHBOARD ACTIVO]

🌐 URL Local:  http://192.168.1.100:8080
🌐 URL Externa: http://0.0.0.0:8080
📡 Interfaz Monitor: wlan0
```

---

## 📝 Funciones de la Clase QuantumHijack

```python
class QuantumHijack:
    # Nuevas funciones para modo monitor
    get_wireless_interfaces()    # Detecta tarjetas WiFi
    set_monitor_mode()          # Activa modo monitor
    restore_managed_mode()      # Restaura modo normal
    run_command()               # Ejecuta comandos sistema
    
    # Funciones de red
    scan_network()              # Escanea LAN
    start_sniffer()             # Inicia captura
    stop_sniffer()              # Detiene captura
    
    # Utilidades
    check_root()                # Verifica sudo
    get_local_ip()              # Obtiene IP
    get_status()                # Estado completo
```

---

## 🧪 Testing Automático

### Script: `test_api.sh`

Prueba todos los endpoints automáticamente:

```bash
chmod +x test_api.sh
./test_api.sh
```

**Output:**
```
╔════════════════════════════════════════╗
║  QUANTUM-HIJACK API TEST SCRIPT        ║
╚════════════════════════════════════════╝

[TEST 1] Verificando estado del sistema...
{
  "status": "running",
  "monitor_interface": "wlan0",
  "monitor_mode_active": true,
  ...
}
─────────────────────────────────────────
[TEST 2] Verificando modo monitor...
[TEST 3] Obteniendo estadísticas...
[TEST 4] Escaneando red...
[TEST 5] Consultando dispositivos...

✅ Tests completados
```

---

## 🎯 Ventajas Profesionales

### 1. **Automatización Completa**
- No requiere configuración manual
- Detecta hardware automáticamente
- Limpieza automática al salir

### 2. **Manejo Robusto de Errores**
- Try/catch en todas las operaciones
- Logging detallado
- Fallbacks alternativos (iwconfig → iw)

### 3. **API REST Profesional**
- Respuestas JSON estructuradas
- Códigos HTTP correctos
- Documentación completa

### 4. **Documentación Exhaustiva**
- README técnico (450+ líneas)
- QUICKSTART para principiantes
- Ejemplos de uso reales
- Scripts de testing

### 5. **Seguridad y Limpieza**
- Restaura estado original
- Reinicia NetworkManager
- Manejo de señales (Ctrl+C)

---

## 📊 Comparación: Antes vs Ahora

| Característica | Antes | Ahora |
|----------------|-------|-------|
| **Código principal** | ❌ Vacío | ✅ 450+ líneas |
| **Modo monitor** | ❌ Manual | ✅ Automático |
| **Detección WiFi** | ❌ No | ✅ Automática |
| **API endpoints** | ❌ 0 | ✅ 9 endpoints |
| **Restauración** | ❌ Manual | ✅ Automática |
| **Testing** | ❌ No | ✅ Script incluido |
| **Documentación** | ⚠️ Básica | ✅ Completa |
| **Dependencies** | ⚠️ 3 | ✅ 8 + tools |

---

## 🚀 Uso Típico

### Escenario 1: Testing de red WiFi
```bash
sudo python3 quantum_hijack_full.py
# Interfaz automáticamente en modo monitor
curl http://localhost:8080/api/scan -X POST
# Ctrl+C para salir (restaura automáticamente)
```

### Escenario 2: API programática
```python
import requests

# Estado
status = requests.get('http://localhost:8080/api/status').json()
print(f"Monitor: {status['monitor_interface']}")

# Escanear
scan = requests.post('http://localhost:8080/api/scan',
                    json={'network': '192.168.1.0/24'}).json()
print(f"Dispositivos: {scan['devices_found']}")
```

### Escenario 3: Monitoreo continuo
```bash
# Terminal 1
sudo python3 quantum_hijack_full.py

# Terminal 2
watch -n 5 'curl -s http://localhost:8080/api/stats | jq .'
```

---

## 🏆 Nivel de Profesionalismo

### ⭐⭐⭐⭐⭐ Características Pro:
- ✅ Detección automática de hardware
- ✅ Configuración sin intervención
- ✅ API REST completa
- ✅ Manejo robusto de errores
- ✅ Logging profesional
- ✅ Documentación exhaustiva
- ✅ Scripts de testing
- ✅ Limpieza automática

---

**Emmanuel - Cybersecurity 2026**  
**Proyecto educativo de hacking ético**

---

## 📄 Licencia y Uso

⚠️ **IMPORTANTE:**
- Solo para testing autorizado
- Solo en redes propias
- Solo con fines educativos
- Cumplir leyes locales

🔒 El autor NO es responsable del mal uso.
