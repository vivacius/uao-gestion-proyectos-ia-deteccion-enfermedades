# Frontend Web Desacoplado: AgroScan AI
<!-- Grupo 2 — Maestría en IA y Ciencia de Datos | Universidad Autónoma de Occidente -->

Interfaz web estándar (HTML5, CSS3 y JavaScript Vanilla) para la captura, diagnóstico fitosanitario y visualización probabilística de patologías foliares clasificadas por DINOv2 en CPU.

---

## 1. Estructura de Archivos y Aislamiento de Seguridad

Para evitar la exposición HTTP involuntaria de código fuente Python (`preview_server.py`, `__init__.py`), los recursos públicos para el navegador están estrictamente aislados en el subdirectorio `static/`:

```
ui/web/
├── static/                 # Recursos públicos servidos al navegador
│   ├── index.html          # Estructura semántica, accesibilidad y captura móvil
│   ├── styles.css          # Diseño AgTech responsive, microanimaciones y alertas
│   └── app.js              # Controlador cliente asíncrono (same-origin / REST a FastAPI)
├── preview_server.py       # Servidor local de prueba y mock aislado (no expuesto vía FastAPI)
├── __init__.py             # Módulo Python
└── README.md               # Esta documentación
```

---

## 2. Procedimiento de Ejecución Local

### Opción A: Ejecución Unificada con Backend Real (Recomendada - FastAPI Mount)
FastAPI monta automáticamente los activos de `ui/web/static/` en la raíz (`/`):

1. Iniciar FastAPI:
   ```bash
   uv run uvicorn api.main:app --reload --port 8000
   ```
2. Abrir en el navegador: `http://127.0.0.1:8000`
3. **Mismo Origen (Same-Origin):** La interfaz detecta automáticamente `window.location.origin` y consume directamente los endpoints `/health` y `/predict` del mismo host, sin configuraciones manuales ni riesgos de CORS.

---

### Opción B: Modo Previsualización y Pruebas Aisladas (Mock Integrado)
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

## 3. Integración con Docker (HU-08)

La imagen de la API copia `ui/web/static` en la etapa `runtime` del `Dockerfile`, de modo que FastAPI monta la interfaz en `/` y expone simultáneamente la API REST/OpenAPI en el puerto `8000`.

Para la orquestación con Docker Compose se agrega un servicio `web` basado en `nginx:1.27-alpine` que:

- Sirve los archivos de `ui/web/static` en `http://localhost:8080`.
- Aplica un proxy *same-origin* hacia `api:8000` para `/health`, `/model-info`, `/predict`, `/docs`, `/redoc` y `/openapi.json`.
- Espera a que el servicio `api` supere su *healthcheck* antes de arrancar.

De esta manera, el frontend y el backend quedan desacoplados en contenedores separados, pero el navegador sigue consumiendo un único origen sin problemas de CORS.

---

## 4. Despliegue en Producción (Render / Cloud / Hostinger)

1. **Despliegue unificado (FastAPI + Web):**
   Al desplegar el backend en plataformas como Render o mediante Docker, FastAPI sirve la web en la raíz de forma transparente bajo HTTPS con su propio dominio o subdominio.
2. **Despliegue estático desacoplado (opcional):**
   Si se decide alojar el frontend en un hosting estático (ej. Hostinger `public_html/`), únicamente deben copiarse los archivos de `ui/web/static/` (`index.html`, `styles.css`, `app.js`). El usuario puede ingresar la URL de la API en el panel de configuración ⚙️ de la interfaz, la cual se persiste en `localStorage`.
