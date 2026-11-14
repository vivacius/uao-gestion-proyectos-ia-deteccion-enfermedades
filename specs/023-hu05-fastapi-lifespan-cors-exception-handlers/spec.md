# Especificación Técnica (Spec Kit): SPEC-023 HU-05 Ciclo de Vida Lifespan, Middleware CORS y Manejadores de Excepciones en FastAPI

**Identificador:** `SPEC-023`  
**Feature Branch:** `feature/modelo-enfermedades-plantas`  
**Historia / Issue Asociado:** HU-05 (Issue [#8](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/8) · 3 SP)  
**Responsable:** Jhonatan Andrés Tapia Córdoba (`@JhonatanTC99`)  
**Revisor Asignado:** Santiago Correa Campaña (`@vivacius`)  
**Fecha:** 2026-11-11  
**Estado:** Completado y verificado en `develop`

---

## 1. Propósito y Alcance
Configurar en `api/main.py` la instancia principal de `FastAPI` con su gestor de contexto asíncrono `lifespan` para precargar el modelo DINOv2-small en memoria al arrancar el servidor, el middleware `CORSMiddleware` y los 4 manejadores globales `@app.exception_handler` para `ImageValidationError`, `ModelLoadError`, `InferenceError` y `PlantDiseaseAppError`.

## 2. Escenarios de Aceptación (Gherkin)

### AC23.1 — Precarga tolerante a fallos en el arranque (`lifespan`)
- **Dado** el inicio del servidor FastAPI,
- **Cuando** se ejecuta el bloque `lifespan`,
- **Entonces** precarga el singleton `get_model_bundle()` en CPU y, si los pesos no están disponibles aún, permite que la API arranque en modo degradado informándolo en `/health`.

### AC23.2 — Traducción automática de excepciones de dominio a JSON HTTP
- **Dado** una excepción `ImageValidationError`, `ModelLoadError` o `InferenceError` lanzada en cualquier endpoint,
- **Cuando** es interceptada por FastAPI,
- **Entonces** se transforma en un `JSONResponse` con código `400/413/415`, `503` o `500` sin exponer trazas internas del servidor.
