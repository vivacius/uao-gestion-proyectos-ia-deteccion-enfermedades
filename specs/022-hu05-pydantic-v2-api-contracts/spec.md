# Especificación Técnica (Spec Kit): SPEC-022 HU-05 Contratos de Datos y Esquemas OpenAPI con Pydantic v2

**Identificador:** `SPEC-022`  
**Feature Branch:** `feature/modelo-enfermedades-plantas`  
**Historia / Issue Asociado:** HU-05 (Issue [#8](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/8) · 3 SP)  
**Responsable:** Jhonatan Andrés Tapia Córdoba (`@JhonatanTC99`)  
**Revisor Asignado:** Santiago Correa Campaña (`@vivacius`)  
**Fecha:** 2026-11-11  
**Estado:** Completado y verificado en `develop`

---

## 1. Propósito y Alcance
Definir en `api/schemas.py` los modelos de datos estrictos con **Pydantic v2** (`TopPredictionItem`, `PredictionResponse`, `HealthResponse`, `ModelInfoResponse` y `ErrorResponse`) con restricciones de rango (`ge=0.0`, `le=1.0`, `ge=1`), descripciones detalladas para OpenAPI y ejemplos documentados.

## 2. Escenarios de Aceptación (Gherkin)

### AC22.1 — Validación estricta de rangos y tipos en Pydantic v2
- **Dado** los esquemas `PredictionResponse` y `TopPredictionItem` en `api/schemas.py`,
- **Cuando** serializan el resultado de una inferencia,
- **Entonces** validan que `confidence` esté en `[0.0, 1.0]`, `confidence_percentage` en `[0.0, 100.0]`, `rank >= 1` y `inference_time_ms >= 0.0`.

### AC22.2 — Esquema estandarizado de errores HTTP (`ErrorResponse`)
- **Dado** cualquier excepción de dominio capturada por FastAPI,
- **Cuando** se responde al cliente HTTP,
- **Entonces** sigue la estructura `{"detail": "...", "error_type": "..."}` documentada en Swagger UI.
