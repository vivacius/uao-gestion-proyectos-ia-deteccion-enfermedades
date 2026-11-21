# Tasks (Spec Kit): SPEC-031 HU-06 Montaje Estático de la Interfaz Web en la Raíz de FastAPI y Same-Origin

**Feature Branch:** `feature/hu06-fastapi-web-mount` | **Spec:** [spec.md](./spec.md) | **Plan:** [plan.md](./plan.md) | **Fecha de Implementación:** 2026-11-12 (12/11/2026) | **Documentación SDD (Retrospectiva):** 2026-11-14 (14/11/2026)

- [x] **TSK-031-01:** Mover activos públicos a `ui/web/static/` y montar `StaticFiles` en `api/main.py` (commits `3c4d78c`, `bf13a7c`).
- [x] **TSK-031-02:** Verificar no exposición de `preview_server.py` mediante `TestClient` en `tests/unit/test_web_ui.py`.
- [x] **TSK-031-03:** Fusionar PR #27 hacia `develop`.
