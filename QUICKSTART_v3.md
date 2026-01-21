# 🔥 QUANTUM-HIJACK v3.0 - QUICK START (COPIA-PEGA)

## ⚡ 30 SEGUNDOS PARA EMPEZAR

```bash
# 1. POSICIONARSE EN CARPETA
cd ~/Desktop/QUANTUM-HIJACK-v3

# 2. INSTALAR (1 comando)
sudo bash setup_v3.sh

# 3. DAR PERMISOS
chmod +x quantum_hijack_v3.py interceptor_v3.py

# 4. EJECUTAR (1 comando)
sudo python3 quantum_hijack_v3.py
```

**Espera output:**
```
╔════════════════════════════════════════════════════════╗
║  🔥 QUANTUM-HIJACK v3.0                               ║
║  🌐 WEB DASHBOARD → http://localhost:8080             ║
╚════════════════════════════════════════════════════════╝
```

## 🌐 DASHBOARD

Abre: **http://localhost:8080**

Click: **🔥 INICIAR TODO**

¡LISTO! WiFi en el aire, esperando víctimas.

---

## 📱 DEMO CON TELÉFONO

1. Abre WiFi en teléfono
2. Busca: **"CafeGratis_FreeWiFi"**
3. CONECTA (sin contraseña)
4. Abre Gmail / Facebook
5. Intenta login

**EN EL DASHBOARD:**
```
✅ Cliente conectado
🔥 Infectado
🔓 Credenciales capturadas LIVE
```

---

## ⬇️ DESCARGAR

Dashboard tiene 2 botones:

**⬇️ Descargar TXT**
```
infected_devices.txt
- IPs infectadas
- MACs
- Reverse shells
```

**📦 Descargar ZIP**
```
quantum_loot.zip contiene:
- infected_devices.txt
- credentials.json
- operation_logs.json
- RESUMEN.txt
```

---

## 🛑 DETENER

**Opción 1:** Click ⛔ en dashboard

**Opción 2:** Terminal
```bash
Ctrl+C
```

**AUTO-LIMPIA:**
```
✅ Detiene todos servicios
✅ Desactiva modo monitor
✅ Restaura interfaz normal
✅ Reinicia NetworkManager
```

---

## 🎯 FLUJO COMPLETO (5 MIN DEMO)

```
MIN 0:00 → sudo python3 quantum_hijack_v3.py
MIN 0:30 → http://localhost:8080
MIN 1:00 → Click "🔥 INICIAR TODO"
         → WiFi en el aire

MIN 2:00 → Teléfono ve "CafeGratis_FreeWiFi"
MIN 2:30 → Teléfono conecta (sin contraseña)
MIN 3:00 → Dashboard: "1 Cliente conectado"

MIN 3:30 → Víctima abre Gmail
MIN 4:00 → Dashboard: "🔥 INFECTADO"
         → "🔓 user@gmail.com:password123"

MIN 4:30 → Click "⬇️ Descargar ZIP"
         → quantum_loot.zip guardado

MIN 5:00 → Ctrl+C → Auto-limpia
```

---

## ⚙️ ARCHIVOS PRINCIPALES

| Archivo | Qué hace |
|---------|----------|
| **quantum_hijack_v3.py** | MAIN (Flask + Control) |
| **interceptor_v3.py** | Captura credenciales |
| **setup_v3.sh** | Instala dependencias |
| **README_v3.md** | Documentación completa |

---

## 🔧 SI ALGO FALLA

### WiFi no aparece
```bash
sudo iw wlan0 set txpower fixed 3000
sudo systemctl restart hostapd
```

### Puerto 8080 ocupado
```bash
sudo lsof -i :8080
sudo kill -9 <PID>
```

### Permisos
```bash
Siempre: sudo python3 quantum_hijack_v3.py
```

---

## ✨ CARACTERÍSTICAS

- ✅ WiFi ABIERTO (auto-conectar)
- ✅ Modo monitor auto ON/OFF
- ✅ Captura credenciales LIVE
- ✅ Infecta dispositivos
- ✅ Persistencia (reverse shell)
- ✅ Dashboard cyberpunk
- ✅ Descarga automática
- ✅ Limpieza automática

---

## ⚖️ LEGAL

```
✅ SOLO para testing AUTORIZADO
✅ Laboratorios educativos
✅ Redes propias

❌ NO sin permiso
❌ NO en redes públicas
❌ NO para robar datos
```

---

## 🎓 APRENDES

- Hacking WiFi
- Inyección de payloads
- Captura de credenciales
- Python + Flask
- Scapy + Packet sniffing

---

**¡LISTO PARA TU EVENTO!** 🔥

Emmanuel - 2026
