# Especificación Técnica (Spec Kit): SPEC-035 HU-07 Pruebas de Integración Extremo a Extremo con el Modelo Real DINOv2 en CPU

**Identificador:** `SPEC-035`  
**Feature Branch:** `feature/hu07-tests-coverage`  
**Historia / Issue Asociado:** HU-07 (Issue [#10](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/10) · 3 SP)  
**Responsable:** Santiago Correa Campaña (`@vivacius`)  
**Revisor Asignado:** Jhonatan Andrés Tapia Córdoba (`@JhonatanTC99`)  
**Fecha:** 2026-11-11  
**Estado:** Completado y verificado en `develop`

---

## 1. Propósito y Alcance
Implementar en `tests/integration/test_api_and_model.py` las pruebas de integración reales que cargan el modelo `rodynaemad/plant-disease-dinov2-small` (`model.safetensors`) en CPU y verifican de extremo a extremo la carga local del `ModelBundle`, la inferencia directa con `predict_from_bytes` y las peticiones HTTP contra FastAPI (`GET /health`, `POST /predict` con JPG, PNG, RGBA e imágenes inválidas).

## 2. Escenarios de Aceptación (Gherkin)

### AC35.1 — Inferencia real en CPU sobre las 38 clases
- **Dado** los pesos reales `model.safetensors` presentes localmente,
- **Cuando** se ejecuta `uv run pytest tests/integration -v`,
- **Entonces** las 6 pruebas de integración pasan verificando que el modelo carga en CPU con 38 etiquetas y genera predicciones reales con `0.0 <= confidence <= 1.0`.

### AC35.2 — Comportamiento E2E de los endpoints REST con el modelo real
- **Dado** el `TestClient(app)` conectado al modelo real,
- **Cuando** se envían imágenes JPG/PNG/RGBA válidas y archivos inválidos a `POST /predict`,
- **Entonces** responde `200 OK` con Top-3 para las válidas y `400/415` para las inválidas.
