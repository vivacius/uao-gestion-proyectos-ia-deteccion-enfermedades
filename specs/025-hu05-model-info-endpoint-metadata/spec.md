# Especificación Técnica (Spec Kit): SPEC-025 HU-05 Endpoint GET /model-info para Metadatos Técnicos del Modelo

**Identificador:** `SPEC-025`  
**Feature Branch:** `feature/m3-model-info`  
**Historia / Issue Asociado:** HU-05 (Issue [#8](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/8) · PR [#20](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/pull/20))  
**Responsable:** Jhonatan Andrés Tapia Córdoba (`@JhonatanTC99`)  
**Revisor Asignado:** Santiago Correa Campaña (`@vivacius`)  
**Fecha:** 2026-11-12  
**Estado:** Completado y verificado en `develop`

---

## 1. Propósito y Alcance
Implementar el endpoint `GET /model-info` en `api/main.py` y el esquema `ModelInfoResponse` en `api/schemas.py` para exponer de forma dedicada los metadatos arquitectónicos del clasificador (`model_name`, `architecture`, `device`, `num_classes`, `model_available`, `model_path`).

## 2. Escenarios de Aceptación (Gherkin)

### AC25.1 — Consulta de metadatos técnicos del modelo
- **Dado** el servicio FastAPI activo con el modelo cargado,
- **Cuando** se realiza una petición `GET /model-info`,
- **Entonces** retorna HTTP 200 con `ModelInfoResponse` indicando `rodynaemad/plant-disease-dinov2-small`, `Dinov2ForImageClassification`, `cpu` y `38` clases.

### AC25.2 — Respuesta controlada cuando el modelo no está disponible
- **Dado** un entorno donde `get_model_bundle()` lanza `ModelLoadError`,
- **Cuando** se consulta `GET /model-info`,
- **Entonces** retorna HTTP 200 con `model_available=False`, `num_classes=0` y `architecture=None`.
