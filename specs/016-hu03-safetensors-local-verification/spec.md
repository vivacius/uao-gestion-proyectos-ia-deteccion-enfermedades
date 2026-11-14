# Especificación Técnica (Spec Kit): SPEC-016 HU-03 Verificación de Artefactos Locales del Modelo y Pesos SafeTensors

**Identificador:** `SPEC-016`  
**Feature Branch:** `feature/modelo-enfermedades-plantas`  
**Historia / Issue Asociado:** HU-03 (Issue [#6](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/6) · 3 SP)  
**Responsable:** Jhonatan Andrés Tapia Córdoba (`@JhonatanTC99`)  
**Revisor Asignado:** Santiago Correa Campaña (`@vivacius`)  
**Fecha:** 2026-11-10  
**Estado:** Completado y verificado en `develop`

---

## 1. Propósito y Alcance
Asegurar que los tres artefactos obligatorios del modelo preentrenado `rodynaemad/plant-disease-dinov2-small` (`config.json`, `preprocessor_config.json` y `model.safetensors`) estén versionados e íntegros en disco mediante Git LFS (`.gitattributes`) y sean verificados preventivamente por `verify_model_files()` en `src/model_loader.py` antes de intentar cualquier carga en memoria.

## 2. Escenarios de Aceptación (Gherkin)

### AC16.1 — Verificación preventiva de archivos requeridos
- **Dado** una ruta de directorio del modelo,
- **Cuando** se ejecuta `verify_model_files(model_dir)` y falta alguno de los 3 archivos o está vacío (`0 bytes`),
- **Entonces** se lanza `ModelLoadError` indicando exactamente qué artefactos faltan.

### AC16.2 — Formato seguro SafeTensors sin pickle arbitrario
- **Dado** los pesos almacenados en `model.safetensors` (~88 MB),
- **Cuando** son inspeccionados y cargados por `transformers` y `safetensors`,
- **Entonces** no se utilizan archivos `.bin` basados en `pickle`, previniendo ejecución de código arbitrario al cargar el modelo.
