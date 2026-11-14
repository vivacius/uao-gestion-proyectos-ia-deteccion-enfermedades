# Especificación Técnica (Spec Kit): SPEC-026 HU-05 Endpoint Asíncrono POST /predict para Clasificación Fitosanitaria

**Identificador:** `SPEC-026`  
**Feature Branch:** `feature/modelo-enfermedades-plantas`  
**Historia / Issue Asociado:** HU-05 (Issue [#8](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/8) · 3 SP)  
**Responsable:** Jhonatan Andrés Tapia Córdoba (`@JhonatanTC99`)  
**Revisor Asignado:** Santiago Correa Campaña (`@vivacius`)  
**Fecha:** 2026-11-11  
**Estado:** Completado y verificado en `develop`

---

## 1. Propósito y Alcance
Implementar en `api/main.py` el endpoint principal `POST /predict` que recibe una fotografía foliar mediante `multipart/form-data` (`UploadFile`), extrae sus bytes de forma asíncrona, delega la inferencia a `predict_from_bytes()` y retorna un `PredictionResponse` con la predicción principal, el Top-3, el tiempo de inferencia en CPU y el descargo agronómico.

## 2. Escenarios de Aceptación (Gherkin)

### AC26.1 — Clasificación exitosa de fotografías JPG y PNG
- **Dado** una imagen válida enviada en el campo `file` a `POST /predict`,
- **Cuando** se procesa la solicitud,
- **Entonces** retorna HTTP 200 con el JSON validado por `PredictionResponse`, incluyendo las 3 predicciones más probables y `inference_time_ms`.

### AC26.2 — Documentación completa de respuestas de error en OpenAPI
- **Dado** la especificación generada en `/docs` para `POST /predict`,
- **Cuando** se inspeccionan los códigos de respuesta,
- **Entonces** están documentados los estados HTTP `200`, `400`, `413`, `415`, `500` y `503` con el modelo `ErrorResponse`.
