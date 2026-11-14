# Especificación Técnica (Spec Kit): SPEC-020 HU-04 Cálculo de Softmax, Ranking Top-3 y Estructuración de Salidas

**Identificador:** `SPEC-020`  
**Feature Branch:** `feature/modelo-enfermedades-plantas`  
**Historia / Issue Asociado:** HU-04 (Issue [#7](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/7) · 2 SP)  
**Responsable:** John Restrepo Aparicio (`@JohnRestrepo-coder`)  
**Revisor Asignado:** Jhonatan Andrés Tapia Córdoba (`@JhonatanTC99`)  
**Fecha:** 2026-11-11  
**Estado:** Completado y verificado en `develop`

---

## 1. Propósito y Alcance
Implementar en `src/postprocessing.py` (`process_logits`) la conversión de los logits crudos del modelo en una distribución de probabilidad mediante `torch.softmax(dim=-1)`, la selección ordenada de las $k=3$ categorías más probables (`torch.topk`) y la construcción de los objetos de dominio `PredictionItem` y `ClassificationResult` con porcentajes redondeados y metadatos bilingües.

## 2. Escenarios de Aceptación (Gherkin)

### AC20.1 — Normalización probabilística y ordenamiento Top-3
- **Dado** un tensor de logits de forma `(1, 38)` o `(38,)`,
- **Cuando** se invoca `process_logits(logits, id2label, inference_time_ms, top_k=3)`,
- **Entonces** las probabilidades suman 1.0 y `top_predictions` contiene las 3 clases más probables en orden estrictamente descendente (`rank` 1, 2 y 3).

### AC20.2 — Validación defensiva de dimensiones de logits
- **Dado** un tensor vacío o con dimensiones mayores a 2D,
- **Cuando** se pasa a `process_logits()`,
- **Entonces** se lanza `InferenceError` de forma controlada.
