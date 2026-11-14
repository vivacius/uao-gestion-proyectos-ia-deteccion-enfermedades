# Plan de Implementación (Spec Kit): SPEC-031 HU-06 Montaje Estático de la Interfaz Web en la Raíz de FastAPI y Same-Origin

**Identificador:** `SPEC-031`  
**Feature Branch:** `feature/hu06-fastapi-web-mount`  
**Spec Asociada:** [spec.md](./spec.md)

---

## Pasos de Implementación y Verificación

1. Aislar los recursos públicos (`index.html`, `styles.css`, `app.js`) dentro de `ui/web/static/`.
2. Montar `app.mount('/', StaticFiles(directory=str(WEB_STATIC_DIR), html=True), name='web_ui')` al final de `api/main.py`.
3. Actualizar `app.js` para resolver por defecto el mismo origen (`window.location.origin`) cuando se sirve por HTTP/HTTPS.
