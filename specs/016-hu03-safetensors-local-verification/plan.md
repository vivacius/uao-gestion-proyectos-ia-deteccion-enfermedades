# Plan de Implementación (Spec Kit): SPEC-016 HU-03 Verificación de Artefactos Locales del Modelo y Pesos SafeTensors

**Identificador:** `SPEC-016`  
**Feature Branch:** `feature/modelo-enfermedades-plantas`  
**Spec Asociada:** [spec.md](./spec.md)

---

## Pasos de Implementación y Verificación

1. Configurar `.gitattributes` para gestionar `*.safetensors` mediante Git LFS.
2. Implementar `verify_model_files()` en `src/model_loader.py` comprobando existencia y tamaño $> 0$ de `REQUIRED_MODEL_FILES`.
3. Agregar pruebas unitarias simulando directorios incompletos o archivos vacíos.
