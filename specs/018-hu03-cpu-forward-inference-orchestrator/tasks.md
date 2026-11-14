# Tasks (Spec Kit): SPEC-018 HU-03 Orquestador de Inferencia en CPU y Telemetría de Latencia

**Feature Branch:** `feature/modelo-enfermedades-plantas` | **Spec:** [spec.md](./spec.md) | **Fecha de Implementación:** 2026-11-11 (11/11/2026) | **Documentación SDD (Retrospectiva):** 2026-11-14 (14/11/2026)

- [x] **TSK-018-01:** Implementar `predict_from_bytes` en `src/inference.py`.
- [x] **TSK-018-02:** Instrumentar medición de latencia en milisegundos con `time.perf_counter()`.
- [x] **TSK-018-03:** Verificar flujo completo con mocks y con modelo real en `tests/unit/` y `tests/integration/`.
