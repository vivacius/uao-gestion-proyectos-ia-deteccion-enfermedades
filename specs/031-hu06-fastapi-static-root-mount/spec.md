# Especificación Técnica (Spec Kit): SPEC-031 HU-06 Montaje Estático de la Interfaz Web en la Raíz de FastAPI y Same-Origin

**Identificador:** `SPEC-031`  
**Feature Branch:** `feature/hu06-fastapi-web-mount`  
**Historia / Issue Asociado:** HU-06 (Issue [#9](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/9) · PR [#27](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/pull/27))  
**Responsable:** John Restrepo Aparicio (`@JohnRestrepo-coder`)  
**Revisor Asignado:** Jhonatan Andrés Tapia Córdoba (`@JhonatanTC99`)  
**Fecha:** 2026-11-12  
**Estado:** Completado y verificado en `develop`

---

## 1. Propósito y Alcance
Integrar el frontend web estático (`ui/web/static/`) directamente en la raíz (`/`) de la aplicación FastAPI (`api/main.py`) mediante `StaticFiles(html=True)` después de declarar los endpoints REST, y configurar en `app.js` la resolución automática de `window.location.origin` (*Same-Origin*) para que el servicio pueda desplegarse de manera unificada o detrás de Nginx sin errores de CORS.

## 2. Escenarios de Aceptación (Gherkin)

### AC31.1 — Entrega de la interfaz web en `GET /` sin interferir con rutas de API
- **Dado** la aplicación FastAPI en ejecución,
- **Cuando** se realiza `GET /`,
- **Entonces** retorna `index.html` (`200 OK`), mientras que `/health`, `/model-info`, `/predict` y `/docs` continúan respondiendo normalmente.

### AC31.2 — Aislamiento de seguridad del directorio `ui/web/static/`
- **Dado** el montaje `StaticFiles` en `api/main.py`,
- **Cuando** un cliente intenta acceder por HTTP a `/preview_server.py` o `/__init__.py`,
- **Entonces** el servidor responde `404 Not Found` porque solo el subdirectorio `ui/web/static/` está expuesto.
