# 📸 DEMO DEL DASHBOARD

## Vista Previa del Dashboard

### Secciones principales:

```
┌─────────────────────────────────────────────────────────────────┐
│  🔓 QUANTUM-HIJACK 2026            ● En línea  🕐 10:30:45     │
└─────────────────────────────────────────────────────────────────┘
```

### Grid de Paneles:

```
┌──────────────────────────┬──────────────────────────┐
│ 📡 Estado del Monitor    │ 🖥️ Dispositivos Detectados│
│                          │                          │
│ Interfaz: wlan0          │ 192.168.1.1 (Router)    │
│ Modo Monitor: ✅ Activo  │ 192.168.1.100 (PC)      │
│ IP Local: 192.168.1.50   │ 192.168.1.105 (Phone)   │
│                          │ 192.168.1.110 (Tablet)  │
│ Dispositivos: 4          │ 192.168.1.115 (TV)      │
│ Infectados: 2            │                          │
│                          │                          │
│ [🔍] [📡] [⚡] [🛑]     │                          │
└──────────────────────────┴──────────────────────────┘

┌──────────────────────────────────────────────────────┐
│ ⚔️ Dispositivos Infectados/Comprometidos             │
│                                                      │
│ ⚔️ 192.168.1.100 | MAC: AA:BB:CC:DD:EE:FF           │
│    Comprometido | 2026-01-21 10:25:30               │
│                                                      │
│ ⚔️ 192.168.1.105 | MAC: 11:22:33:44:55:66           │
│    Comprometido | 2026-01-21 10:30:15               │
│                                                      │
│ [🎯 Marcar] [💾 Exportar] [🗑️ Limpiar]            │
└──────────────────────────────────────────────────────┘

┌──────────────────────────┬──────────────────────────┐
│ 📊 Estadísticas          │ 💻 Consola de Comandos   │
│                          │                          │
│  Paquetes: 1,234         │ [10:25:30] [+] Escaneo   │
│  Credenciales: 3         │ [10:25:35] [+] 5 dispositivos
│                          │ [10:25:40] [*] Iniciado  │
│  Tiempo: 00:05:42        │ [10:30:15] [+] Infectado │
│                          │                          │
│  ╔═════════════════════╗ │ > _                      │
│  ║ Uptime: 00:05:42    ║ │ [EXEC]                  │
│  ╚═════════════════════╝ │                          │
└──────────────────────────┴──────────────────────────┘

┌──────────────────────────┐
│ ⚡ Control de Ataques    │
│                          │
│ [ARP Spoofing]           │
│ [DNS Spoofing]           │
│ [Packet Sniff]           │
│ [Deauth]                 │
│                          │
│ Estado: Packet Sniff     │
│ activo                   │
│                          │
│ Control de ataques...    │
└──────────────────────────┘
```

---

## 🎬 Ejemplo Interactivo

### Paso 1: Iniciar Escaneo

**Usuario:** Click en botón "🔍 Escanear"

**Consola:**
```
[10:25:30] [*] Iniciando escaneo de red...
[10:25:35] [+] 5 dispositivos encontrados
```

**Panel de Dispositivos se actualiza:**
```
192.168.1.1     | Activo
192.168.1.100   | Activo ← NEW
192.168.1.105   | Activo ← NEW
192.168.1.110   | Activo ← NEW
192.168.1.115   | Activo ← NEW
```

### Paso 2: Seleccionar Dispositivo

**Usuario:** Click en dispositivo "192.168.1.100"

**Modal aparece:**
```
┌─────────────────────────────────────┐
│ Detalles del Dispositivo         [×]│
├─────────────────────────────────────┤
│                                     │
│ IP:         192.168.1.100          │
│ MAC:        AA:BB:CC:DD:EE:FF      │
│ Timestamp:  2026-01-21T10:25:35   │
│                                     │
│ [Marcar como Infectado]  [Atacar]  │
│                                     │
└─────────────────────────────────────┘
```

### Paso 3: Marcar como Infectado

**Usuario:** Click en "Marcar como Infectado"

**Consola:**
```
[10:25:40] [+] 192.168.1.100 marcado como infectado
```

**Panel de Infectados se actualiza:**
```
⚔️ 192.168.1.100 | MAC: AA:BB:CC:DD:EE:FF
   Comprometido | 2026-01-21 10:25:40
```

**Contador actualizado:**
```
Infectados: 1 → Infectados: 2
```

### Paso 4: Ejecutar Ataque

**Usuario:** Click en "ARP Spoofing"

**Consola:**
```
[10:30:00] [+] ARP Spoofing iniciado
```

**Panel de Control se actualiza:**
```
Estado: ARP Spoofing activo
```

### Paso 5: Exportar Datos

**Usuario:** Click en "💾 Exportar datos"

**Descarga:** `quantum-hijack-1674316800.json`

**Contenido:**
```json
{
  "timestamp": "2026-01-21T10:30:45.123456",
  "devices": [
    {
      "ip": "192.168.1.1",
      "mac": "FF:FF:FF:FF:FF:FF",
      "timestamp": "2026-01-21T10:25:35.000000"
    },
    {
      "ip": "192.168.1.100",
      "mac": "AA:BB:CC:DD:EE:FF",
      "timestamp": "2026-01-21T10:25:35.000000"
    }
  ],
  "infected": [
    {
      "ip": "192.168.1.100",
      "mac": "AA:BB:CC:DD:EE:FF",
      "timestamp": "2026-01-21T10:25:40.000000",
      "status": "Comprometido"
    }
  ]
}
```

---

## 🔌 API Calls en Tiempo Real

### Escaneo
```bash
POST /api/scan
{
  "network": "192.168.1.0/24"
}

Response:
{
  "success": true,
  "devices_found": 5,
  "devices": [
    {
      "ip": "192.168.1.1",
      "mac": "FF:FF:FF:FF:FF:FF",
      "timestamp": "2026-01-21T10:25:35.123456"
    }
  ]
}
```

### Marcar Infectado
```bash
POST /api/infected/add
{
  "ip": "192.168.1.100",
  "mac": "AA:BB:CC:DD:EE:FF"
}

Response:
{
  "success": true,
  "message": "Dispositivo 192.168.1.100 agregado"
}
```

### Ver Infectados
```bash
GET /api/infected

Response:
{
  "total": 2,
  "devices": [
    {
      "ip": "192.168.1.100",
      "mac": "AA:BB:CC:DD:EE:FF",
      "timestamp": "2026-01-21T10:25:40.123456",
      "status": "Comprometido"
    }
  ]
}
```

---

## 🎨 Características Visuales

### Animaciones
- **Pulso del indicador de estado**: 2s infinito
- **Cambio de color al hover**: 0.3s smooth
- **Glitch en log importante**: 0.3s
- **Scroll suave**: Todo el contenido

### Colores en Acción
- **Verde (#00ff41)**: Información, dispositivos activos
- **Rojo (#ff006e)**: Dispositivos infectados, botones peligrosos
- **Amarillo (#ffbe0b)**: IP addresses, warnings
- **Gris**: Texto secundario, MACs

### Efectos
- **Box shadow**: Cada elemento tiene brillo
- **Borde luminoso**: Al hacer hover
- **Fondo degradado**: Header con efecto hacker
- **Bordes con colores**: Verde normal, rojo para infectados

---

## 📊 Métricas en Vivo

El dashboard muestra:

| Métrica | Actualización | Ejemplo |
|---------|---------------|---------|
| Hora | Cada segundo | 🕐 10:30:45 |
| Dispositivos detectados | Manual (botón) | 5 dispositivos |
| Dispositivos infectados | Inmediata | 2 infectados |
| Paquetes capturados | Cada 2 segundos | 1,234 paquetes |
| Credenciales encontradas | Cada 2 segundos | 3 credenciales |
| Uptime | Cada segundo | 00:05:42 |
| Ataque activo | Inmediata | ARP Spoofing activo |

---

## 💾 Almacenamiento Persistente

### Sesión 1:
```
Día 1 - 10:30:
- Detectados 5 dispositivos
- Infectados 2: 192.168.1.100, 192.168.1.105
- Guardado en: infected_devices.json
```

### Sesión 2 (Día siguiente):
```
Día 2 - 09:00:
- Inicia programa
- Lee infected_devices.json
- Muestra 2 infectados del día anterior
- Agrega 1 nuevo
- Total: 3 infectados
```

---

## 🎯 Casos de Uso

### 1. Auditoría de Red
```
1. Abrir dashboard
2. Escanear red completa
3. Ver todos los dispositivos
4. Exportar para reporte
```

### 2. Testing de Seguridad
```
1. Identificar dispositivos
2. Marcar como objetivo
3. Ejecutar ataques específicos
4. Monitorear en consola
5. Guardar logs
```

### 3. Monitoreo Continuo
```
1. Dejar corriendo 24/7
2. Revisar periódicamente
3. Mantener lista de infectados
4. Exportar reportes diarios
```

---

**Este dashboard es una interfaz profesional para QUANTUM-HIJACK**

Emmanuel - Cybersecurity 2026
