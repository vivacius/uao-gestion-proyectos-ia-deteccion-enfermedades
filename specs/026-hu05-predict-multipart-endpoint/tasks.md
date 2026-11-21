# Tasks (Spec Kit): SPEC-026 HU-05 Endpoint Asíncrono POST /predict para Clasificación Fitosanitaria

**Feature Branch:** `feature/modelo-enfermedades-plantas` | **Spec:** [spec.md](./spec.md) | **Plan:** [plan.md](./plan.md) | **Fecha de Implementación:** 2026-11-11 (11/11/2026) | **Documentación SDD (Retrospectiva):** 2026-11-14 (14/11/2026)

- [x] **TSK-026-01:** Implementar endpoint `POST /predict` en `api/main.py`.
- [x] **TSK-026-02:** Conectar lectura asíncrona de `UploadFile` con `predict_from_bytes`.
- [x] **TSK-026-03:** Validar respuestas 200, 400, 413, 415, 500 y 503 en pruebas unitarias e integradas.
