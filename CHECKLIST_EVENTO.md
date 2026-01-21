# ✅ QUANTUM-HIJACK v3.0 - CHECKLIST PRE-EVENTO

## 📋 ANTES DEL EVENTO (1 DÍA)

### Sistema
- [ ] Ejecutar en Kali Linux 2026+
- [ ] Usuario root/sudo habilitado
- [ ] Tarjeta WiFi con soporte modo monitor
- [ ] Comprobar: `iw dev` (debe mostrar interfaz)

### Instalación
- [ ] `cd ~/Desktop/QUANTUM-HIJACK-v3`
- [ ] `sudo bash setup_v3.sh` (sin errores)
- [ ] `chmod +x quantum_hijack_v3.py interceptor_v3.py`

### Archivos
- [ ] quantum_hijack_v3.py (600+ líneas)
- [ ] interceptor_v3.py (250+ líneas)
- [ ] setup_v3.sh (instalador)
- [ ] README_v3.md (docs)
- [ ] QUICKSTART_v3.md (quick guide)

### Dependencias
- [ ] `python3 -c "import flask; print('✅ Flask')"` → OK
- [ ] `python3 -c "import scapy; print('✅ Scapy')"` → OK
- [ ] `which hostapd` → /usr/sbin/hostapd
- [ ] `which dnsmasq` → /usr/sbin/dnsmasq
- [ ] `which airmon-ng` → /usr/bin/airmon-ng

---

## 🎯 DÍA DEL EVENTO (Antes)

### Verificación Rápida
- [ ] Laptop conectada a corriente
- [ ] WiFi en laptop APAGADO (Settings)
- [ ] Modo avión OFF
- [ ] Teléfono de prueba con WiFi (Android/iOS)
- [ ] Puerto 8080 libre: `sudo lsof -i :8080`

### Test de Ejecución
```bash
cd ~/Desktop/QUANTUM-HIJACK-v3
sudo python3 quantum_hijack_v3.py
```
Esperar output:
```
╔════════════════════════════════════════════════════════╗
║  🔥 QUANTUM-HIJACK v3.0                               ║
║  🌐 WEB DASHBOARD → http://localhost:8080             ║
╚════════════════════════════════════════════════════════╝
```

### Test de Dashboard
- [ ] Abrir http://localhost:8080 en navegador
- [ ] Dashboard carga
- [ ] Todos los botones visibles
- [ ] Terminal muestra logs EN VIVO

### Test de Módulos
- [ ] Click "Setup Monitor" → ✅ Log: "Modo monitor activado"
- [ ] Click "Hostapd WiFi" → ✅ Log: "WiFi ACTIVO: CafeGratis_FreeWiFi"
- [ ] Click "Dnsmasq DHCP" → ✅ Log: "DHCP ACTIVO"
- [ ] Click "Interceptor" → ✅ Log: "Interceptor ACTIVO"

### Test Completo
- [ ] Click "🔥 INICIAR TODO"
- [ ] Secuencia automática completa (20 segundos)
- [ ] 4 módulos en verde (ACTIVOS)
- [ ] Terminal muestra logs sin errores

### Test de WiFi
- [ ] `iw dev wlan0mon info` → Modo monitor confirmado
- [ ] WiFi "CafeGratis_FreeWiFi" visible en otros dispositivos
- [ ] Teléfono CONECTA sin contraseña

### Test de Captura
- [ ] Teléfono abre http://google.com
- [ ] Dashboard actualiza en VIVO
- [ ] Cliente aparece en "Clientes Conectados"

### Test de Descarga
- [ ] Click "📦 Descargar ZIP"
- [ ] Se descarga quantum_loot.zip
- [ ] Archivo tiene contenido

### Cleanup
```bash
Ctrl+C en terminal
```
Esperar:
```
✅ Detiene todos servicios
✅ Desactiva modo monitor
✅ Restaura interfaz
✅ Reinicia NetworkManager
```

- [ ] Laptop WiFi vuelve a funcionar normal
- [ ] Interfaz restaurada a managed mode

---

## 🎬 DURANTE EL EVENTO

### Antes de Presentar (5 min)
- [ ] Laptop conectada a proyector
- [ ] Terminal visible en pantalla grande
- [ ] Navegador abierto pero sin tabs (limpio)
- [ ] Teléfono de demo cargado (batería 80%+)

### Presentación (Escenario Ideal)
```
[SLIDE 1] "QUANTUM-HIJACK v3.0"
[DEMOSTRACIÓN EN VIVO]

MIN 0:00 → Ejecutar: sudo python3 quantum_hijack_v3.py
MIN 0:30 → Abrir: http://localhost:8080
MIN 1:00 → Click: "🔥 INICIAR TODO"
         → Punto 1: Modo monitor visible en terminal
         → Punto 2: WiFi "CafeGratis_FreeWiFi" en pantalla

MIN 2:00 → Mostrar teléfono: "Buscar WiFi"
         → Punto 3: WiFi aparece en lista
         → Punto 4: "Sin contraseña - conectar"

MIN 2:30 → Teléfono conectado
         → Dashboard: "1 Cliente conectado" ✅

MIN 3:00 → Teléfono: "Abrir Gmail"
         → Intento de login

MIN 3:30 → Dashboard LIVE: 🔥 INFECTADO
         → "user@gmail.com : password123" ✅

MIN 4:00 → Click: "⬇️ Descargar ZIP"
         → "Se descargó quantum_loot.zip"

MIN 4:30 → Mostrar archivo descargado
         → "Credenciales guardadas"

MIN 5:00 → Ctrl+C
         → Auto-limpia
         → "Modo monitor desactivado"
         → "Interfaz restaurada"
```

### Contingencias

**Si WiFi no aparece:**
- [ ] `sudo systemctl restart hostapd`
- [ ] `sudo iw wlan0 set txpower fixed 3000`
- [ ] Esperar 10 segundos

**Si cliente no conecta:**
- [ ] Activar WiFi en teléfono
- [ ] Olvidar red ("Forget")
- [ ] Re-conectar
- [ ] Si falla: reiniciar WiFi en teléfono

**Si credenciales no aparecen:**
- [ ] Interceptor puede estar sin privilegios
- [ ] Terminal: `Ctrl+C` → `sudo python3 quantum_hijack_v3.py`
- [ ] Re-intentar con teléfono en modo incognito

**Si dashboard se cuelga:**
- [ ] Refresh navegador (F5)
- [ ] O abrir pestaña nueva: http://localhost:8080

---

## 📊 TIEMPO ESTIMADO

```
Setup:           2 min (hasta WiFi en el aire)
Conexión:        1 min (teléfono conecta)
Captura:         1 min (credenciales aparecen)
Descarga:        30 seg
Cleanup:         30 seg
────────────────────────
TOTAL:           5 minutos (perfecto)
```

---

## 🎙️ SCRIPT DE PRESENTACIÓN (COPY-PASTE)

```
"Hola a todos. Les presento QUANTUM-HIJACK v3.0.

Una herramienta educativa que demuestra cómo:
1. Crear un WiFi falso
2. Capturar credenciales EN VIVO
3. Infectar dispositivos
4. Mantener persistencia

¿Listos? Comencemos.

[Ejecutar script]

1. Ven el modo monitor activándose
2. El WiFi 'CafeGratis_FreeWiFi' aparece
3. Conectamos un teléfono
4. Abrimos Gmail y intentamos login
5. ¡INSTANTÁNEAMENTE! Las credenciales aparecen en el dashboard
6. Todo guardado en un ZIP descargable

¿Creen que sus usuarios estarían seguros contra esto?
Exacto. Necesitan educación en seguridad.

Presión: Ctrl+C
[Sistema auto-limpia automáticamente]

Gracias."
```

---

## 📸 FOTOS/VIDEOS

- [ ] Captura de pantalla del dashboard con datos
- [ ] Video corto (1 min) del flujo completo
- [ ] Foto de la descarga del ZIP
- [ ] Antes/después de conectar teléfono

---

## ✨ FINAL

- [ ] Evento exitoso
- [ ] Audiencia impactada
- [ ] Punto: "Seguridad WiFi es crítica"
- [ ] Preguntas respondidas
- [ ] Gracias dados
- [ ] Sistema limpio después

---

## 🎯 OBJETIVO LOGRADO

✅ Demo impactante en 5 minutos
✅ Muestra vulnerabilidades reales
✅ Educativo pero aterrador
✅ Audiencia aprende importancia de seguridad
✅ Tu evento: **LEGENDARIO** 🔥

---

**¡ESTÁS LISTO EMMANUEL!**

Go get them! 🚀

Emmanuel - 2026
