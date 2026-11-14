# Plan de Implementación (Spec Kit): SPEC-035 HU-07 Pruebas de Integración Extremo a Extremo con el Modelo Real DINOv2 en CPU

**Identificador:** `SPEC-035`  
**Feature Branch:** `feature/hu07-tests-coverage`  
**Spec Asociada:** [spec.md](./spec.md)

---

## Pasos de Implementación y Verificación

1. Crear `tests/integration/test_api_and_model.py` con verificación de disponibilidad local del modelo.
2. Implementar pruebas de integración para `get_model_bundle()`, `predict_from_bytes()`, `GET /health` y `POST /predict`.
3. Mantener separación estricta entre `tests/unit/` (con mocks para CI rápido) y `tests/integration/` (con pesos reales).
