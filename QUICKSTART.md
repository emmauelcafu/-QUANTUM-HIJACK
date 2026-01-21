# 📋 GUÍA DE EJECUCIÓN RÁPIDA

## ⚡ Quick Start (3 pasos)

```bash
# 1. Instalar
sudo bash setup.sh

# 2. Ejecutar
sudo python3 quantum_hijack_full.py

# 3. Probar API
./test_api.sh
```

---

## 📺 Output Esperado

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
INFO:__main__:🔍 Detectando interfaces wireless...
INFO:__main__:✅ Interfaces encontradas: ['wlan0']

💡 Se detectaron 1 interfaz(es) wireless:
   1. wlan0

🔧 Configurando modo monitor automáticamente...
INFO:__main__:🔧 Configurando wlan0 en modo monitor...
INFO:__main__:   → Deteniendo procesos interferentes...
INFO:__main__:   → Bajando interfaz wlan0...
INFO:__main__:   → Activando modo monitor...
INFO:__main__:   → Levantando interfaz...
INFO:__main__:   → Configurando canal 6...
INFO:__main__:✅ Modo monitor activado en wlan0
✅ Interfaz wlan0 lista en modo monitor

─────────────────────────────────────────────────
[DASHBOARD ACTIVO]

🌐 URL Local:  http://192.168.1.100:8080
🌐 URL Externa: http://0.0.0.0:8080
📡 Interfaz Monitor: wlan0

[API ENDPOINTS]

GET  /api/status         - Estado del sistema
POST /api/scan           - Escanear red local
POST /api/attacks/start  - Iniciar ataque
POST /api/attacks/stop   - Detener ataque
GET  /api/stats          - Ver estadísticas
GET  /api/devices        - Dispositivos detectados
GET  /api/monitor        - Info modo monitor

─────────────────────────────────────────────────
Presiona CTRL+C para detener y limpiar
─────────────────────────────────────────────────

 * Serving Flask app 'quantum_hijack_full'
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
 * Running on http://192.168.1.100:8080
```

### Al presionar Ctrl+C:

```
^C

⛔ DETENIENDO APLICACIÓN...
──────────────────────────────────────────────────
🔄 Restaurando interfaz a modo normal...
INFO:__main__:🔄 Restaurando wlan0 a modo managed...
INFO:__main__:   → Reiniciando NetworkManager...
INFO:__main__:✅ wlan0 restaurado a modo managed
✅ Limpieza completada. ¡Hasta pronto!
──────────────────────────────────────────────────
```

---

## 🧪 Probar la API

### Opción 1: Script automático
```bash
chmod +x test_api.sh
./test_api.sh
```

### Opción 2: Comandos manuales
```bash
# Ver estado
curl http://localhost:8080/api/status | python3 -m json.tool

# Ver modo monitor
curl http://localhost:8080/api/monitor | python3 -m json.tool

# Escanear red
curl -X POST http://localhost:8080/api/scan \
  -H "Content-Type: application/json" \
  -d '{"network": "192.168.1.0/24"}' | python3 -m json.tool
```

### Opción 3: Navegador web
```
Abrir: http://localhost:8080/api/status
```

---

## 🔧 Solución de Problemas

### Error: "No se encontraron interfaces wireless"
**Solución:** Verifica que tu adaptador WiFi esté conectado
```bash
iwconfig
iw dev
```

### Error: "No se pudo activar modo monitor"
**Solución:** Algunos drivers no soportan modo monitor
```bash
# Verifica tu driver
lsmod | grep -i wifi
airmon-ng
```

### Error: "Permission denied"
**Solución:** Debes ejecutar como root
```bash
sudo python3 quantum_hijack_full.py
```

### NetworkManager interfiere
**Solución:** El programa lo maneja automáticamente con:
```bash
airmon-ng check kill
```

---

## 💡 Consejos Pro

1. **Usa tmux o screen** para mantener sesiones activas
   ```bash
   tmux new -s hijack
   sudo python3 quantum_hijack_full.py
   # Ctrl+B, D para desconectar
   ```

2. **Monitorea logs en tiempo real** en otra terminal
   ```bash
   tail -f /var/log/syslog | grep quantum
   ```

3. **Verifica modo monitor manualmente**
   ```bash
   iwconfig wlan0
   # Debe decir "Mode:Monitor"
   ```

4. **Captura tráfico con tcpdump** (paralelo)
   ```bash
   sudo tcpdump -i wlan0 -w capture.pcap
   ```

---

## ⚙️ Configuración Avanzada

### Cambiar canal WiFi
Edita en `quantum_hijack_full.py` línea ~145:
```python
self.run_command(f"iwconfig {interface} channel 11")  # Cambiar 6 por 11
```

### Cambiar puerto del servidor
Edita en `quantum_hijack_full.py` línea ~420:
```python
app.run(host='0.0.0.0', port=9090, ...)  # Cambiar 8080 por 9090
```

### Habilitar debug mode
```python
app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
```

---

## 📊 Métricas de Rendimiento

- **Tiempo de inicio:** ~3-5 segundos
- **Configuración modo monitor:** ~2-3 segundos
- **Escaneo de red (24 hosts):** ~2-3 segundos
- **Uso de RAM:** ~50-80 MB
- **Uso de CPU:** 5-10% en idle

---

## 🎓 Recursos Adicionales

- [Documentación Scapy](https://scapy.readthedocs.io/)
- [Aircrack-ng Tutorial](https://www.aircrack-ng.org/)
- [Flask REST API Guide](https://flask.palletsprojects.com/)
- [Wireless Security Basics](https://wiki.archlinux.org/title/Wireless)

---

**Creado por Emmanuel - 2026**  
**SOLO para hacking ético y educación**
