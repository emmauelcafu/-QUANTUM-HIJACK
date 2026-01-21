# 🔥 QUANTUM-HIJACK v3.0 - WiFi Rogue + Infectar + Persistir

**Herramienta Educativa de Hacking Ético Avanzada**

Emmanuel - 2026

[![Platform](https://img.shields.io/badge/Platform-Linux-success)](https://www.kali.org/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Educational-red)](LICENSE)

---

## ⚠️ AVISO LEGAL IMPORTANTE

**Este software es EXCLUSIVAMENTE para:**
- ✅ Testing de seguridad autorizado
- ✅ Laboratorios educativos controlados
- ✅ Redes propias o con permiso explícito por escrito

**PROHIBIDO usar para:**
- ❌ Acceder a redes sin autorización
- ❌ Interceptar datos privados ilegalmente
- ❌ Robar credenciales
- ❌ Causar daño intencional

El autor NO es responsable del mal uso. **Cumple con todas las leyes aplicables.**

---

## 📋 ¿QUÉ HACE?

```
1. ✅ Modo Monitor AUTOMÁTICO (ON/OFF)
2. ✅ WiFi ABIERTO (sin contraseña) - Auto-conectar
3. ✅ DHCP automático (192.168.1.x)
4. ✅ Interceptar credenciales (emails, bancos, etc)
5. ✅ INFECTAR dispositivos (payload)
6. ✅ PERSISTENCIA (reverse shell cron)
7. ✅ Dashboard cyberpunk EN VIVO
8. ✅ Auto-limpiar al salir (Ctrl+C)
```

---

## 🖥️ REQUISITOS DEL SISTEMA

### Plataforma
- **Sistema Operativo:** Linux (Kali recomendado, Ubuntu/Debian compatible)
- **Permisos:** root/sudo
- **Hardware:** Tarjeta WiFi con soporte modo monitor

> ⚠️ **WINDOWS NO SOPORTADO**: Este proyecto requiere herramientas Linux exclusivas (airmon-ng, hostapd, dnsmasq). En Windows solo puedes ver la documentación HTML.

### Dependencias
Instaladas automáticamente con `setup_v3.sh`:
- hostapd (Access point)
- dnsmasq (DHCP + DNS)
- aircrack-ng (Herramientas wireless)
- wireless-tools, iw (Utilidades WiFi)
- python3-pip
- python3-scapy
- flask, scapy, requests (Python)

---

## ⚡ INSTALACIÓN RÁPIDA (Linux)

```bash
# 1. Clonar o descargar proyecto
cd ~/Desktop
git clone <tu-repo> QUANTUM-HIJACK-v3
cd QUANTUM-HIJACK-v3

# 2. Verificar requisitos (RECOMENDADO)
sudo bash verify_requirements.sh

# 3. Instalar dependencias
sudo bash setup_v3.sh

# 4. Dar permisos de ejecución
chmod +x quantum_hijack_v3.py interceptor_v3.py

# 5. EJECUTAR (requiere sudo)
sudo python3 quantum_hijack_v3.py

# 6. Abrir navegador
http://localhost:8080
```

---

## 📁 ESTRUCTURA DEL PROYECTO

```
QUANTUM-HIJACK-v3/
├── quantum_hijack_v3.py        # ⭐ MAIN - Servidor Flask + Control
├── interceptor_v3.py           # 🔓 Capturador de credenciales
├── setup_v3.sh                 # 🔧 Instalador automático (Linux)
├── verify_requirements.sh      # ✅ Verificador de requisitos
├── start_windows.ps1           # 🪟 Launcher Windows (solo docs)
│
├── index.html                  # 📖 Documentación interactiva HTML
├── README.md                   # 📄 Este archivo
├── README_v3.md                # 📚 README completo original
├── README_HTML.md              # 📋 Guía para usar index.html
├── QUICKSTART_v3.md            # ⚡ Guía rápida
├── CHECKLIST_EVENTO.md         # ✅ Checklist para demos/eventos
│
├── logs/                       # 📊 (auto-creado) Logs y capturas
│   ├── infected_devices.json
│   ├── captured_credentials.json
│   └── operation_logs.json
├── payloads/                   # 💉 (auto-creado) Payloads de infección
└── capture/                    # 📦 (auto-creado) Capturas adicionales
```

---

## 🎮 USO RÁPIDO (5 MINUTOS)

### 1. Iniciar servidor
```bash
sudo python3 quantum_hijack_v3.py
```

### 2. Abrir dashboard
Navegador → **http://localhost:8080**

### 3. Click "🔥 INICIAR TODO"
- Se activa modo monitor automáticamente
- WiFi "CafeGratis_FreeWiFi" en el aire (ABIERTO, sin contraseña)
- DHCP asignando IPs
- Interceptor escuchando tráfico

### 4. Conectar dispositivo víctima
- Buscar WiFi: **"CafeGratis_FreeWiFi"**
- Conectar (sin contraseña)
- Dashboard actualiza EN VIVO

### 5. Capturar credenciales
- Víctima navega (Gmail, Facebook, bancos, etc.)
- Dashboard muestra credenciales capturadas
- Descargar: TXT o ZIP completo

### 6. Detener
```bash
Ctrl+C
```
O click **"⛔ DETENER TODO"** en dashboard.

**Auto-limpia:** Restaura interfaz WiFi a modo normal.

---

## 📊 API REST ENDPOINTS

```
GET  /api/status              → Estado actual del sistema
GET  /api/clients             → Clientes conectados
GET  /api/infected            → Dispositivos infectados
GET  /api/credentials         → Credenciales capturadas
GET  /api/logs                → Logs de operación

POST /api/init/setup          → Activar modo monitor
POST /api/init/hostapd        → Iniciar WiFi falso
POST /api/init/dnsmasq        → Iniciar DHCP
POST /api/init/interceptor    → Iniciar interceptor
POST /api/init/all            → INICIAR TODO
POST /api/stop/all            → DETENER TODO + Limpiar

POST /api/infect              → Infectar dispositivo
GET  /api/download/infected   → Descargar infectados.txt
GET  /api/download/all        → Descargar quantum_loot.zip
```

---

## 🔧 CARACTERÍSTICAS AVANZADAS

### Modo Monitor Automático
- Detecta interfaz WiFi automáticamente
- Activa/desactiva modo monitor sin intervención
- Restaura al estado original al salir

### WiFi Abierto (Sin Contraseña)
- SSID: `CafeGratis_FreeWiFi` (configurable)
- Sin autenticación → auto-conectar
- Máxima compatibilidad con dispositivos

### Interceptor Inteligente
Monitorea puertos:
- 80 (HTTP), 443 (HTTPS)
- 21 (FTP), 22 (SSH)
- 3306 (MySQL), 5432 (PostgreSQL), 27017 (MongoDB)

Detecta bancos/servicios:
- PKO, Santander, mBank, ING
- Gmail, Outlook, Yahoo
- Facebook, Instagram, Twitter, LinkedIn
- WhatsApp Web, Allegro

### Dashboard EN VIVO
- Auto-actualización cada 2 segundos
- Estado de módulos en tiempo real
- Clientes conectados
- Dispositivos infectados
- Credenciales capturadas
- Logs operacionales

---

## 🐛 TROUBLESHOOTING

### "No se ve el WiFi"
```bash
# Verificar interfaz
iw dev

# Aumentar potencia
sudo iw wlan0 set txpower fixed 3000

# Revisar hostapd
sudo systemctl status hostapd
```

### "Puerto 8080 ocupado"
```bash
sudo lsof -i :8080
sudo kill -9 <PID>
```

### "Modo monitor no funciona"
```bash
# Desactivar NetworkManager
sudo systemctl stop NetworkManager

# Iniciar manualmente
sudo airmon-ng start wlan0
```

### "Interceptor no captura"
```bash
# Verificar interfaz monitor
iw dev wlan0mon info

# Asegurar privilegios
sudo python3 interceptor_v3.py
```

### "Error en Windows"
**Respuesta:** Este proyecto NO funciona en Windows. Usa Linux o VM.
En Windows puedes abrir `index.html` para ver documentación.

---

## 🎯 CASOS DE USO LEGÍTIMOS

✅ **Pentest autorizado** - Evaluar seguridad WiFi de organizaciones
✅ **Educación** - Enseñar conceptos de seguridad inalámbrica
✅ **Demostración** - Mostrar vulnerabilidades en eventos/conferencias
✅ **Testing interno** - Validar protecciones en redes controladas

---

## 📖 DOCUMENTACIÓN

- **README_v3.md**: Documentación original completa
- **QUICKSTART_v3.md**: Guía ultra-rápida
- **CHECKLIST_EVENTO.md**: Checklist para demos/eventos
- **index.html**: Vista interactiva con todas las guías (abre en navegador)

### Ver documentación HTML
```bash
# Linux/Mac
xdg-open index.html

# Windows (solo documentación)
start index.html
# O ejecuta: start_windows.ps1
```

---

## 🔍 VERIFICACIÓN ANTES DE EJECUTAR

Antes de ejecutar en producción/demo:

```bash
sudo bash verify_requirements.sh
```

Esto verifica:
- Sistema operativo compatible
- Permisos root
- Dependencias instaladas
- Interfaz WiFi disponible
- Puerto 8080 libre
- Archivos del proyecto presentes

---

## 👨‍💻 AUTOR

**Emmanuel** - Cybersecurity Researcher 2026  
Especialista en Hacking Ético y Seguridad Ofensiva

---

## 📝 CHANGELOG

### v3.0 (2026-01-22) - COMPLETAMENTE NUEVO
✨ **Características:**
- Modo monitor automático ON/OFF
- WiFi ABIERTO (auto-conectar sin contraseña)
- Captura avanzada de credenciales
- Infección de dispositivos con payloads
- Persistencia (reverse shell + cron)
- Dashboard profesional cyberpunk
- Limpieza automática al salir
- API REST completa
- Verificador de requisitos
- Documentación HTML interactiva

### v2.0 (2026-01-21)
- Captura básica de credenciales
- WiFi con contraseña
- Dashboard simple

### v1.0 (2026-01-20)
- Concepto inicial
- Setup básico

---

## 🎓 LEARNING OUTCOMES

Al trabajar con este proyecto aprendes:
- Conceptos de WiFi y seguridad inalámbrica
- Modo monitor en interfaces wireless
- DHCP y DNS spoofing
- Packet sniffing con Scapy
- Análisis de protocolos de red (HTTP, HTTPS, FTP, SSH)
- Detección de patrones de credenciales
- Desarrollo de herramientas de pentesting
- Flask + REST APIs
- Automatización de hacking ético
- Bash scripting avanzado
- Gestión de procesos Linux

---

## 📞 SOPORTE

Si tienes problemas:

1. Revisa los logs en `logs/`
2. Verifica que ejecutas con `sudo`
3. Ejecuta el verificador: `sudo bash verify_requirements.sh`
4. Comprueba dependencias: `sudo bash setup_v3.sh`
5. Revisa el dashboard para errores EN VIVO

---

## 🛡️ MEJORES PRÁCTICAS

### Para Pentesters
- Documenta autorización por escrito antes de comenzar
- Define alcance claro del engagement
- Notifica hallazgos inmediatamente
- Destruye capturas al finalizar (o según política)
- Genera reportes profesionales

### Para Educadores
- Usa solo en entornos de laboratorio aislados
- Informa a estudiantes sobre aspectos legales
- Supervisa uso en todo momento
- No permitas conexiones a redes productivas
- Enfatiza ética y responsabilidad

### Para Investigadores
- Valida en entornos controlados
- Contribuye mejoras al proyecto
- Reporta vulnerabilidades responsablemente
- Cita apropiadamente en publicaciones

---

## 🌟 CONTRIBUIR

¿Mejoras? ¿Bugs? ¡Contribuciones bienvenidas!

1. Fork el proyecto
2. Crea tu feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push branch (`git push origin feature/AmazingFeature`)
5. Abre Pull Request

---

## 📜 LICENSE

Este proyecto es para **fines educativos únicamente**.

**Disclaimer:** El autor no se hace responsable del uso indebido de este software. El usuario asume toda la responsabilidad legal derivada del uso de esta herramienta. Usar sin autorización puede resultar en consecuencias legales graves.

---

**¡QUANTUM-HIJACK v3.0 - Hacking Ético Responsable!** 🔥

Emmanuel - 2026

---

## ⚡ QUICK LINKS

- 📖 [Documentación Completa](README_v3.md)
- ⚡ [Guía Rápida](QUICKSTART_v3.md)
- ✅ [Checklist Evento](CHECKLIST_EVENTO.md)
- 🌐 [Documentación HTML](index.html)
- 🔍 [Verificar Requisitos](verify_requirements.sh)
