# Plan de Implementación (Spec Kit): SPEC-018 HU-03 Orquestador de Inferencia en CPU y Telemetría de Latencia

**Identificador:** `SPEC-018`  
**Feature Branch:** `feature/modelo-enfermedades-plantas`  
**Spec Asociada:** [spec.md](./spec.md)

---

## Pasos de Implementación y Verificación

1. Implementar `predict_from_bytes()` en `src/inference.py` conectando `validate_and_open_image`, `get_model_bundle`, `preprocess_image` y `process_logits`.
2. Envolver la ejecución del modelo en `with torch.no_grad():` y medir el tiempo con `time.perf_counter()`.
3. Manejar excepciones diferenciando errores de validación, carga e inferencia.
