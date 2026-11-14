# Tasks (Spec Kit): SPEC-020 HU-04 Cálculo de Softmax, Ranking Top-3 y Estructuración de Salidas

**Feature Branch:** `feature/modelo-enfermedades-plantas` | **Spec:** [spec.md](./spec.md)

- [x] **TSK-020-01:** Implementar `PredictionItem`, `ClassificationResult` y `process_logits` en `src/postprocessing.py`.
- [x] **TSK-020-02:** Asegurar soporte para tensores 1D `(38,)` y 2D `(1, 38)`.
- [x] **TSK-020-03:** Verificar suma de probabilidades y orden Top-3 en `tests/unit/test_labels_and_postprocessing.py`.
