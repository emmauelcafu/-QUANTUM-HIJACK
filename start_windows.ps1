# QUANTUM-HIJACK v3.0 - Launcher para Windows
# Este script solo abre la documentación HTML, ya que el proyecto requiere Linux

Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  QUANTUM-HIJACK v3.0 - Documentación                      ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

Write-Host "⚠️  AVISO: PLATAFORMA INCORRECTA" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host ""
Write-Host "Este proyecto requiere LINUX (Kali, Ubuntu, etc.) para funcionar." -ForegroundColor White
Write-Host "Windows NO soporta las herramientas necesarias:" -ForegroundColor White
Write-Host "  • airmon-ng (modo monitor WiFi)" -ForegroundColor Gray
Write-Host "  • hostapd (access point)" -ForegroundColor Gray
Write-Host "  • dnsmasq (DHCP + DNS)" -ForegroundColor Gray
Write-Host "  • ifconfig/iw (configuración de red)" -ForegroundColor Gray
Write-Host ""

Write-Host "📖 DOCUMENTACIÓN DISPONIBLE" -ForegroundColor Green
Write-Host "─────────────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host ""
Write-Host "Abriendo documentación HTML en tu navegador..." -ForegroundColor White
Write-Host ""

# Verificar si existe index.html
$indexPath = Join-Path $PSScriptRoot "index.html"

if (Test-Path $indexPath) {
    Write-Host "✓ Abriendo: $indexPath" -ForegroundColor Green
    Start-Process $indexPath
    Start-Sleep -Seconds 2
    
    Write-Host ""
    Write-Host "La documentación incluye:" -ForegroundColor White
    Write-Host "  • README completo" -ForegroundColor Gray
    Write-Host "  • Guía rápida (QuickStart)" -ForegroundColor Gray
    Write-Host "  • Checklist para eventos/demos" -ForegroundColor Gray
    Write-Host ""
} else {
    Write-Host "✗ No se encontró index.html" -ForegroundColor Red
    Write-Host ""
}

Write-Host "🐧 PARA EJECUTAR EL PROYECTO" -ForegroundColor Cyan
Write-Host "─────────────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host ""
Write-Host "1. Usa una máquina Linux o máquina virtual:" -ForegroundColor White
Write-Host "   • Kali Linux (recomendado)" -ForegroundColor Gray
Write-Host "   • Ubuntu / Debian" -ForegroundColor Gray
Write-Host "   • Cualquier distro con soporte WiFi" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Copia estos archivos a Linux:" -ForegroundColor White
Write-Host "   • quantum_hijack_v3.py" -ForegroundColor Gray
Write-Host "   • interceptor_v3.py" -ForegroundColor Gray
Write-Host "   • setup_v3.sh" -ForegroundColor Gray
Write-Host "   • Todos los .md (documentación)" -ForegroundColor Gray
Write-Host ""
Write-Host "3. En Linux, ejecuta:" -ForegroundColor White
Write-Host "   sudo bash setup_v3.sh" -ForegroundColor Yellow
Write-Host "   sudo python3 quantum_hijack_v3.py" -ForegroundColor Yellow
Write-Host ""

Write-Host "⚖️  AVISO LEGAL" -ForegroundColor Magenta
Write-Host "─────────────────────────────────────────────────────────────" -ForegroundColor Gray
Write-Host "Solo para testing autorizado y propósitos educativos." -ForegroundColor White
Write-Host "El uso no autorizado puede violar leyes locales." -ForegroundColor White
Write-Host ""

Write-Host "Presiona cualquier tecla para salir..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
