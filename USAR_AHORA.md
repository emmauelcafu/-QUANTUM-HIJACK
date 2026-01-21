# 🔓 QUANTUM-HIJACK v2.0 - GUÍA DE USO INMEDIATO

## ✅ ESTADO ACTUAL

- ✅ Backend completo con detección automática de tipos de dispositivos
- ✅ Dashboard reparado sin errores de sintaxis
- ✅ Mostrador de tipo de dispositivo: 📱 Celular | 💻 PC | 📺 TV | 🌐 Router
- ✅ Tabla de infectados con checkboxes y multi-selección
- ✅ Loading overlay, toasts, auto-refresh
- ✅ Todo funciona en Kali Linux

---

## 🚀 EJECUCIÓN EN KALI (3 PASOS)

### PASO 1: Navegar al proyecto
```bash
cd ~/Desktop/QUANTUM-HIJACK/-QUANTUM-HIJACK
```

### PASO 2: Iniciar el servidor
```bash
sudo python3 quantum_hijack_full.py
```

**Verás:**
```
╔════════════════════════════════════════╗
║   QUANTUM-HIJACK 2026 - ACTIVO        ║
║   Herramienta de Hacking Ético v2.0   ║
╚════════════════════════════════════════╝

✓ Servicio Flask iniciado en 0.0.0.0:8080
✓ Interfaz de red detectada: wlan0
✓ Modo Monitor: Activado

🌐 DASHBOARD WEB:
   http://localhost:8080
```

### PASO 3: Abre en navegador
```
http://localhost:8080
```

---

## 🎮 CÓMO USAR EL DASHBOARD

### 1️⃣ ESCANEAR RED
- Botón grande verde: **🔍 ESCANEAR**
- Detecta automáticamente tu rango de red
- Muestra cada dispositivo con su tipo:
  - **📱 Celular** - Smartphones (iPhone, Android)
  - **💻 PC/Laptop** - Computadoras de escritorio
  - **📺 Smart TV** - Televisores inteligentes
  - **🌐 Router** - Routers y switches
  - **🔊 Smart Device** - Alexa, Google Home, etc.
  - **❓ Desconocido** - Dispositivos no identificados

### 2️⃣ MARCAR INFECTADOS
**Opción A: Uno por uno**
- Click en el dispositivo en la lista
- Modal muestra detalles
- Click en "✓ Marcar como Infectado"
- Aparece en tabla roja abajo

**Opción B: Masivo**
- (Próximamente) Checkboxes en lista de dispositivos

### 3️⃣ EJECUTAR ATAQUES
En el panel "⚡ Panel de Control":
- **ARP Spoofing** - Envenenamiento ARP
- **DNS Hijack** - Redirección DNS
- **Packet Sniff** - Captura de paquetes
- **Deauth** - Desconexión WiFi

O desde botón "⚔️ ATAQUES" en el header

### 4️⃣ CONTROLES PRINCIPALES

| Botón | Función |
|-------|---------|
| 🔍 ESCANEAR | Busca dispositivos en la red |
| 🦠 INFECTAR ✓ | Marca seleccionado como infectado |
| ⚔️ ATAQUES | Muestra panel de control de ataques |
| 📡 Monitor | Activa/desactiva WiFi monitor mode |
| ⚡ Iniciar/🛑 Detener | Control de ataques |
| 🗑️ Remover seleccionados | Borra infectados checked |
| 💾 Exportar JSON | Descarga datos |
| 🧹 Limpiar todo | Limpia historial |

---

## 📊 TABLA DE INFECTADOS

Muestra:
- ☑️ Checkbox (seleccionar múltiples)
- 📱/💻/🌐 Tipo de dispositivo + IP
- 🔗 MAC address
- ✓ Status (Comprometido)
- 📅 Fecha/Hora
- ❌ Botón individual para remover

---

## 🔄 ACTUALIZACIÓN AUTOMÁTICA

- **Estado**: Cada 5 segundos
- **Contador de paquetes**: Con animación
- **Logs de operaciones**: En consola
- **Exportación**: Cada 10 minutos
- **Toasts**: Notificaciones flotantes (verde/amarillo/rojo)

---

## 📱 IDENTIFICACIÓN DE DISPOSITIVOS

El sistema ahora detecta automáticamente:

```
Apple Devices        → 📱/💻 iPhone, Mac
Samsung             → 📱 Celular Android
Xiaomi              → 📱 Celular Android
Huawei              → 📱 Celular Android
Intel/Realtek       → 💻 PC/Laptop
Cisco               → 🌐 Router/Switch
Netgear/TP-Link     → 🌐 Router
LG Smart TV         → 📺 Smart TV
Amazon Echo         → 🔊 Smart Speaker
Otros               → ❓ Desconocido
```

---

## ⚠️ TROUBLESHOOTING

### "0 dispositivos encontrados"
```bash
# Verifica tu IP y gateway
ip addr show
ip route

# Verifica que estés en una red
iwconfig
# Busca "ESSID:" con un nombre de red (no vacío)

# Si no hay red, asegúrate de estar conectado a WiFi
```

### "Offline" en el header (indicador rojo)
- Verifica que el servidor Flask esté corriendo
- Refreshea el navegador (Ctrl+Shift+R)
- Reinicia con: `sudo python3 quantum_hijack_full.py`

### Funciones no responden
- Abre consola del navegador: **F12**
- Verifica que no haya errores JavaScript
- Hard refresh: **Ctrl+Shift+R**
- Cierra y reabre el navegador

### Puerto 8080 ocupado
```bash
# Encuentra el proceso
sudo lsof -i :8080

# Termínalo
sudo kill -9 [PID]

# Reinicia la app
sudo python3 quantum_hijack_full.py
```

---

## 📝 ARCHIVO DE DATOS

Los datos se guardan automáticamente:
- **infected_devices.json** - Dispositivos marcados como infectados
- **operation_logs.json** - Historial de operaciones

Descargar con botón 💾 **Exportar JSON**

---

## 🎯 FLUJO TÍPICO DE USO

```
1. Iniciar: sudo python3 quantum_hijack_full.py
2. Abrir: http://localhost:8080
3. Escanear: Click en 🔍 ESCANEAR
4. Esperar overlay "Escaneando..."
5. Ver dispositivos con tipos
6. Click en dispositivo → detalles
7. Click "✓ Marcar como Infectado"
8. Dispositivo aparece en tabla roja abajo
9. Seleccionar ataque en ⚡ Panel
10. Monitorear en 💻 Consola
```

---

## 🔐 NOTAS DE SEGURIDAD

- ⚠️ Solo para testing autorizado
- ⚠️ Requiere permisos root/sudo
- ⚠️ Solo funcionan en redes que controlas
- ⚠️ Respeta leyes locales
- ⚠️ Los logs son registrados automáticamente

---

## 💡 TIPS

- **Scroll consola**: Se actualiza automáticamente
- **Toast notifications**: Aparecen 4s abajo a la derecha
- **Loading overlay**: Muestra "Escaneando..." durante operaciones
- **Semáforo**: Verde=OK | Amarillo=Escaneando | Rojo=Error
- **Auto-export**: Descarga datos cada 10 minutos automáticamente

---

## ✅ VERIFICACIÓN RÁPIDA

Después de iniciar, deberías ver:

```
En Terminal:
✓ "Servicio Flask iniciado en 0.0.0.0:8080"

En Dashboard:
✓ Indicador verde en header
✓ "IP: xxx.xxx.xxx.xxx" en header derecho
✓ Hora actual en header
✓ Botones grandes funcionando
✓ Consola mostrando "[+] Dashboard iniciado"
```

---

**¡LISTO PARA USAR!** 🚀

Cualquier duda o error, revisa la consola del navegador (F12) y/o los logs en la terminal.
