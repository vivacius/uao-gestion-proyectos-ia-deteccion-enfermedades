# Plan de Implementación (Spec Kit): SPEC-021 HU-04 Umbral de Confianza (tau=0.60) y Descargo de Responsabilidad Agronómica

**Identificador:** `SPEC-021`  
**Feature Branch:** `feature/modelo-enfermedades-plantas`  
**Spec Asociada:** [spec.md](./spec.md) | **Tasks:** [tasks.md](./tasks.md)  
**Fecha de Implementación de la Unidad:** 2026-11-11 (11/11/2026)  
**Fecha de Documentación SDD (Retrospectiva):** 2026-11-14 (14/11/2026)

---

## Pasos de Implementación y Verificación

1. Vincular `AGRONOMIC_DISCLAIMER` por defecto en `ClassificationResult` y `PredictionResponse`.
2. Implementar evaluación del umbral $\tau = 0.60$ en las capas de interfaz (`ui/desktop_app.py` y `ui/web/static/app.js`) y scripts de evaluación.
3. Validar presencia del descargo en todas las pruebas unitarias e integradas.
