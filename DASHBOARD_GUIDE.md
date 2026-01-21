# 🎨 DASHBOARD WEB - QUANTUM-HIJACK

## 🌐 Acceso al Dashboard

Una vez que inicies el programa:

```bash
sudo python3 quantum_hijack_full.py
```

Abre tu navegador en:
```
http://localhost:8080
```

O si está en otra máquina:
```
http://[IP_DEL_SERVER]:8080
```

---

## 📊 Interfaz del Dashboard

El dashboard está dividido en varias secciones:

### 1. **Header (Barra Superior)**
- Logo y título del proyecto
- Indicador de estado en tiempo real
- Reloj digital

### 2. **Panel: Estado del Monitor** (Arriba izquierda)
- Información de la interfaz wireless
- Estado del modo monitor (Activo/Inactivo)
- IP local del servidor
- Contador de dispositivos detectados
- Botones de control rápido

### 3. **Panel: Dispositivos Detectados** (Arriba derecha)
- Lista de todos los dispositivos en la red
- IP y dirección MAC
- Estado (Activo)
- Click para ver detalles

### 4. **Panel: Dispositivos Infectados/Comprometidos** (Ancho completo)
- Lista de todos los dispositivos marcados como "infectados"
- Timestamp de cuándo fueron comprometidos
- Botones para marcar, exportar y limpiar

### 5. **Panel: Estadísticas** (Abajo izquierda)
- Paquetes capturados
- Credenciales encontradas
- Tiempo de actividad

### 6. **Panel: Consola de Comandos** (Abajo centro)
- Línea de historial de operaciones
- Campo para ingresar comandos
- Botón EXEC para ejecutar

### 7. **Panel: Control de Ataques** (Abajo derecha)
- Botones para cada tipo de ataque
- Estado actual del ataque
- Información en tiempo real

---

## 🎮 Funcionalidades Principales

### Escanear Red
```
Botón: 🔍 Escanear
Resultado: Encuentra todos los dispositivos en 192.168.1.0/24
```

### Marcar Dispositivo como Infectado
```
1. Haz click en un dispositivo de la lista
2. Se abre un modal con detalles
3. Click en "Marcar como Infectado"
4. El dispositivo aparece en la sección "Infectados"
```

### Ejecutar Ataques
```
Opciones:
- ARP Spoofing    → Manipula tabla ARP
- DNS Spoofing    → Redirige DNS
- Packet Sniff    → Captura paquetes
- Deauth          → Desconecta dispositivos
```

### Exportar Datos
```
Botón: 💾 Exportar datos
Resultado: Descarga archivo JSON con:
- Dispositivos detectados
- Dispositivos infectados
- Timestamp de operaciones
```

### Limpiar Historial
```
Botón: 🗑️ Limpiar historial
Acción: Elimina todos los dispositivos de la lista de infectados
```

---

## 📡 Nuevos Endpoints para Dashboard

### Obtener Infectados
```bash
GET /api/infected
```
**Respuesta:**
```json
{
  "total": 3,
  "devices": [
    {
      "ip": "192.168.1.100",
      "mac": "00:11:22:33:44:55",
      "timestamp": "2026-01-21T10:30:45.123456",
      "status": "Comprometido"
    }
  ]
}
```

### Agregar Dispositivo a Infectados
```bash
POST /api/infected/add
Content-Type: application/json

{
  "ip": "192.168.1.105",
  "mac": "AA:BB:CC:DD:EE:FF"
}
```

### Remover Dispositivo
```bash
DELETE /api/infected/remove/192.168.1.105
```

### Limpiar Todos
```bash
DELETE /api/infected/clear
```

### Obtener Logs
```bash
GET /api/logs
```
**Respuesta:**
```json
{
  "total": 5,
  "logs": [
    {
      "timestamp": "2026-01-21T10:30:45.123456",
      "action": "DEVICE_INFECTED",
      "details": "IP: 192.168.1.100, MAC: 00:11:22:33:44:55"
    }
  ]
}
```

### Exportar Datos Completos
```bash
GET /api/export
```

---

## 💾 Almacenamiento de Datos

### Archivo: `infected_devices.json`
Contiene lista de todos los dispositivos infectados:
```json
[
  {
    "ip": "192.168.1.100",
    "mac": "00:11:22:33:44:55",
    "timestamp": "2026-01-21T10:30:45.123456",
    "status": "Comprometido"
  }
]
```

### Archivo: `operation_logs.json`
Registro de todas las operaciones realizadas:
```json
[
  {
    "timestamp": "2026-01-21T10:30:45.123456",
    "action": "DEVICE_INFECTED",
    "details": "IP: 192.168.1.100, MAC: 00:11:22:33:44:55"
  }
]
```

---

## 🎨 Características de Diseño

### Tema Hacker Profesional
- Fondo oscuro (#0a0e27)
- Texto verde (#00ff41) - estilo terminal
- Efectos de brillo y animaciones
- Scrollbar personalizada

### Colores
- **Verde primario (#00ff41)**: Información normal
- **Amarillo (#ffbe0b)**: Advertencias
- **Rojo (#ff006e)**: Peligro/Infectados
- **Gris**: Texto secundario

### Responsive Design
- Se adapta a pantallas pequeñas
- Grilla de 2 columnas en desktop
- Una columna en móvil

---

## 🔄 Actualización en Tiempo Real

El dashboard se actualiza automáticamente cada 2 segundos:
- Estado del monitor
- Contador de dispositivos
- Estadísticas
- Reloj

---

## 📝 Ejemplo de Uso Típico

### Escenario: Auditoría de Red

```
1. Abrir http://localhost:8080 en navegador
2. Click en "🔍 Escanear"
3. Esperar a que se completen las búsqueda
4. Ver lista de dispositivos detectados
5. Click en cada dispositivo para ver detalles
6. Marcar los sospechosos como "Infectados"
7. Ejecutar ataque (ARP Spoofing, etc.)
8. Monitorear consola para ver logs
9. Click en "💾 Exportar" para generar reporte
10. Datos guardados en JSON para análisis posterior
```

---

## 🛡️ Seguridad

### Credenciales
- No requiere autenticación (asumir red controlada)
- Todos los datos se guardan localmente
- Los logs se rotan cada 100 entradas

### Datos Persistentes
- `infected_devices.json` persiste entre sesiones
- `operation_logs.json` mantiene historial
- Exportación manual disponible

---

## 🐛 Troubleshooting

### El dashboard no se carga
```
1. Verificar que el servidor está corriendo
2. Comprobar puerto 8080: netstat -an | grep 8080
3. Revisar firewall
4. Reintentar acceso
```

### Los dispositivos no aparecen
```
1. Click en "🔍 Escanear"
2. Verificar que hay dispositivos en la red
3. Comprobar rango de red: 192.168.1.0/24
```

### No se guardan los infectados
```
1. Verificar permisos de escritura en carpeta
2. Revisar logs en consola de servidor
3. Intentar exportar para forzar escritura
```

---

## 📱 Acceso Remoto

Para acceder desde otra máquina:

### Desde el mismo servidor
```
http://localhost:8080
http://127.0.0.1:8080
```

### Desde otra máquina en la red
```
http://192.168.1.100:8080  (reemplazar con IP real)
```

### Desde internet (si está expuesto)
```
http://[IP_PUBLICA]:8080
```

---

## 📊 Estadísticas y Métricas

El dashboard muestra en tiempo real:

| Métrica | Origen | Actualización |
|---------|--------|---------------|
| Dispositivos | Escaneo de red | Manual (botón) |
| Infectados | Lista local | Inmediata |
| Paquetes | Captura en vivo | Cada 2 segundos |
| Credenciales | Análisis de tráfico | Cada 2 segundos |
| Uptime | Sistema | Cada 2 segundos |

---

**Emmanuel - Cybersecurity 2026**  
Dashboard profesional para QUANTUM-HIJACK
