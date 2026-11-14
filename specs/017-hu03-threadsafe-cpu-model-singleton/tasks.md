# Tasks (Spec Kit): SPEC-017 HU-03 Carga Local en CPU y Patrón Singleton Thread-Safe del Modelo

**Feature Branch:** `feature/modelo-enfermedades-plantas` | **Spec:** [spec.md](./spec.md) | **Plan:** [plan.md](./plan.md) | **Fecha de Implementación:** 2026-11-10 (10/11/2026) | **Documentación SDD (Retrospectiva):** 2026-11-14 (14/11/2026)

- [x] **TSK-017-01:** Implementar `ModelBundle` y `load_model_bundle` en `src/model_loader.py`.
- [x] **TSK-017-02:** Implementar caché singleton thread-safe en `get_model_bundle()`.
- [x] **TSK-017-03:** Probar concurrencia, caché y fallos de carga con mocks en `tests/unit/test_api_and_loader_mocked.py`.
