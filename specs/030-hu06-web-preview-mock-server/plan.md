# Plan de Implementación (Spec Kit): SPEC-030 HU-06 Servidor Local de Previsualización Web y Mocks Aislados

**Identificador:** `SPEC-030`  
**Feature Branch:** `feature/hu-06-interfaz-web`  
**Spec Asociada:** [spec.md](./spec.md)

---

## Pasos de Implementación y Verificación

1. Implementar `PreviewHandler(SimpleHTTPRequestHandler)` en `ui/web/preview_server.py` fijando `directory` en `ui/web/static`.
2. Implementar respuestas mock para `GET /health` y `POST /predict`.
3. Agregar pruebas unitarias de aislamiento en `tests/unit/test_web_ui.py`.
