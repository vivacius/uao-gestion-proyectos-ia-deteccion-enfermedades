# Especificación Técnica (Spec Kit): SPEC-018 HU-03 Orquestador de Inferencia en CPU y Telemetría de Latencia

**Identificador:** `SPEC-018`  
**Feature Branch:** `feature/modelo-enfermedades-plantas`  
**Historia / Issue Asociado:** HU-03 (Issue [#6](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/6) · 3 SP)  
**Responsable:** Jhonatan Andrés Tapia Córdoba (`@JhonatanTC99`)  
**Revisor Asignado:** Santiago Correa Campaña (`@vivacius`)  
**Fecha:** 2026-11-11  
**Estado:** Completado y verificado en `develop`

---

## 1. Propósito y Alcance
Implementar en `src/inference.py` la función orquestadora `predict_from_bytes()` que integra la validación de la imagen, el preprocesamiento tensorial, el pase hacia adelante (`forward`) sobre CPU dentro de un contexto `with torch.no_grad():`, la medición precisa de latencia en milisegundos con `time.perf_counter()` (meta $< 300$ ms en CPU) y la delegación al postprocesamiento.

## 2. Escenarios de Aceptación (Gherkin)

### AC18.1 — Ejecución sin gradientes y latencia en CPU < 300 ms
- **Dado** una imagen foliar válida en bytes,
- **Cuando** se ejecuta `predict_from_bytes()` en CPU,
- **Entonces** la inferencia se realiza bajo `torch.no_grad()` con una latencia medida en `inference_time_ms` inferior a 300 ms (observada ~60 ms).

### AC18.2 — Aislamiento de fallos internos de inferencia
- **Dado** un fallo inesperado del motor PyTorch durante el pase `forward`,
- **Cuando** es capturado en `predict_from_bytes()`,
- **Entonces** se envuelve y propaga como `InferenceError` sin ocultar excepciones previas de `ImageValidationError` o `ModelLoadError`.
