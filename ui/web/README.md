# Frontend Web Desacoplado: AgroScan AI
<!-- Grupo 2 — Maestría en IA y Ciencia de Datos | Universidad Autónoma de Occidente -->

Interfaz web estándar (HTML5, CSS3 y JavaScript Vanilla) para la captura, diagnóstico fitosanitario y visualización probabilística de patologías foliares clasificadas por DINOv2 en CPU.

---

## 1. Estructura de Archivos

```
ui/web/
├── index.html          # Estructura semántica, accesibilidad y captura móvil
├── styles.css          # Diseño AgTech responsive, microanimaciones y alertas
├── app.js              # Controlador cliente asíncrono (fetch REST a FastAPI)
├── preview_server.py   # Servidor de prueba local con endpoints simulados (/health, /predict)
└── README.md           # Esta documentación
```

---

## 2. Procedimiento de Ejecución Local

### Opción A: Modo Previsualización y Pruebas (Mock Integrado)
Permite verificar la interfaz y el comportamiento visual sin esperar la carga pesada de PyTorch ni requerir el modelo descargado en CPU:

```bash
# Iniciar servidor en el puerto por defecto (3000)
python ui/web/preview_server.py

# O especificar un puerto personalizado:
python ui/web/preview_server.py 8080
```

* Abre tu navegador en: `http://127.0.0.1:3000`
* El servidor responderá automáticamente a:
  * `GET /health` con estado operativo y arquitectura del modelo.
  * `POST /predict` con un diagnóstico simulado de prueba (*Tomate — Tizón tardío* al 88.4% y desglose Top-3).

---

### Opción B: Conexión con el Backend Real (FastAPI)
1. Inicia el servidor de FastAPI en una terminal:
   ```bash
   uv run uvicorn api.main:app --reload --port 8000
   ```
2. Inicia la interfaz web en otra terminal o ábrela directamente:
   ```bash
   python ui/web/preview_server.py 3000
   ```
3. En la interfaz web, haz clic en el ícono de ajustes ⚙️ en la esquina superior derecha y confirma que la URL apunte a:
   `http://127.0.0.1:8000`
4. Al hacer clic en "Probar Conexión", el badge superior cambiará a **API en línea (CPU)**.

---

## 3. Despliegue en Producción (Hostinger / Web Hosting)

1. En el Administrador de Archivos de Hostinger (hPanel), entra a la carpeta `public_html/`.
2. Sube los archivos `index.html`, `styles.css` y `app.js`.
3. En `app.js`, ajusta la constante `DEFAULT_API_URL` con tu subdominio de API (ej. `https://api.tudominio.com`).
4. Activa el certificado SSL gratuito en Hostinger para garantizar navegación segura por HTTPS.
