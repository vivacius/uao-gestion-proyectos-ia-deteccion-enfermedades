# Especificación Técnica (Spec Kit): SPEC-030 HU-06 Servidor Local de Previsualización Web y Mocks Aislados

**Identificador:** `SPEC-030`  
**Feature Branch:** `feature/hu-06-interfaz-web`  
**Historia / Issue Asociado:** HU-06 (Issue [#9](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/9) · PR [#22](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/pull/22))  
**Responsable:** John Restrepo Aparicio (`@JohnRestrepo-coder`)  
**Revisor Asignado:** Jhonatan Andrés Tapia Córdoba (`@JhonatanTC99`)  
**Fecha de Implementación de la Unidad:** 2026-11-12 (12/11/2026)  
**Fecha de Documentación SDD (Retrospectiva):** 2026-11-14 (14/11/2026)  
**Trazabilidad Temporal:** Especificación documentada retrospectivamente el 14/11/2026 (no elaborada antes de implementar; la fecha histórica 2026-11-12 corresponde a la implementación de la unidad)  
**Estado:** Completado y verificado en `develop` y `main` (M3)  
**Artefactos Relacionados:** [plan.md](./plan.md) · [tasks.md](./tasks.md)

---

## 1. Propósito y Alcance
Proveer en `ui/web/preview_server.py` un servidor HTTP ligero basado en la librería estándar (`http.server`) que sirve los archivos de `ui/web/static/` e incluye respuestas simuladas (*mocks*) para `GET /health` y `POST /predict`, permitiendo probar y auditar el diseño del frontend web de forma instantánea sin necesidad de cargar PyTorch ni los pesos del modelo en memoria.

## 2. Escenarios de Aceptación (Gherkin)

### AC30.1 — Servicio aislado de activos estáticos desde `ui/web/static/`
- **Dado** la ejecución de `python ui/web/preview_server.py`,
- **Cuando** un navegador solicita `/`,
- **Entonces** sirve exclusivamente el contenido de `ui/web/static/` sin exponer archivos `.py` del directorio padre.

### AC30.2 — Endpoints mock integrados para `/health` y `/predict`
- **Dado** el servidor de previsualización en ejecución,
- **Cuando** el frontend envía peticiones a `GET /health` y `POST /predict`,
- **Entonces** responde con payloads JSON compatibles con los contratos de FastAPI para verificar toda la experiencia visual.
