# Documentación en HTML — QUANTUM-HIJACK v3

Este proyecto ahora incluye una página HTML para visualizar la documentación y checklist de forma agradable e interactiva.

## Cómo abrir

- Opción rápida (Windows): haz doble clic en `index.html` para abrirlo en tu navegador.
- Opción recomendada (servidor local): ejecuta un servidor estático y visita `http://localhost:8000`.

### Servidor local con Python

```powershell
# En PowerShell, dentro de la carpeta del proyecto
cd "c:\Users\User\OneDrive\Desktop\emmanuel\proyectosss\Nueva carpeta"
python -m http.server 8000
```

Luego abre: `http://localhost:8000/index.html`

## Funcionalidades

- Navegación por pestañas: README v3, QuickStart v3 y Checklist del evento.
- Renderizado Markdown: sin dependencias locales (usa CDN de `marked`).
- Checklist interactivo: las casillas se guardan en `localStorage` por sección.

## Consideraciones

- Todo el contenido es **educativo** y destinado a **testing autorizado**.
- No se ejecuta código del proyecto; solo se visualiza documentación.
- Si tu navegador bloquea recursos locales, usa el servidor local.

## Archivos creados

- `index.html`: página principal con navegación y render de Markdown.
- `README_HTML.md`: esta guía rápida para abrir y usar la vista HTML.

