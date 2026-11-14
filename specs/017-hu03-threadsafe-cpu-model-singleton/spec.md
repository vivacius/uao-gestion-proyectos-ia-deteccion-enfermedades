# Especificación Técnica (Spec Kit): SPEC-017 HU-03 Carga Local en CPU y Patrón Singleton Thread-Safe del Modelo

**Identificador:** `SPEC-017`  
**Feature Branch:** `feature/modelo-enfermedades-plantas`  
**Historia / Issue Asociado:** HU-03 (Issue [#6](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/6) · 3 SP)  
**Responsable:** Jhonatan Andrés Tapia Córdoba (`@JhonatanTC99`)  
**Revisor Asignado:** Santiago Correa Campaña (`@vivacius`)  
**Fecha:** 2026-11-10  
**Estado:** Completado y verificado en `develop`

---

## 1. Propósito y Alcance
Implementar en `src/model_loader.py` la estructura inmutable `ModelBundle` y el cargador singleton thread-safe (`get_model_bundle` protegido con `threading.Lock` y doble verificación) que inicializa `AutoImageProcessor` y `AutoModelForImageClassification` exclusivamente desde archivos locales (`local_files_only=True`), los ubica en `CPU` y coloca el modelo en modo evaluación (`model.eval()`).

## 2. Escenarios de Aceptación (Gherkin)

### AC17.1 — Carga estrictamente local sin descargas en tiempo de ejecución
- **Dado** los artefactos locales del modelo en `MODEL_DIR`,
- **Cuando** se invoca `load_model_bundle()`,
- **Entonces** se cargan procesador y modelo con `local_files_only=True`, en `torch.device('cpu')` y `model.eval()`.

### AC17.2 — Instancia única compartida en memoria (Singleton Thread-Safe)
- **Dado** múltiples peticiones concurrentes a la API,
- **Cuando** invocan `get_model_bundle()`,
- **Entonces** el modelo se carga en memoria RAM una única vez y se reutiliza la misma instancia `ModelBundle`.
