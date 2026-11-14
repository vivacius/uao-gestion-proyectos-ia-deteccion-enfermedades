# Tasks (Spec Kit): SPEC-016 HU-03 Verificación de Artefactos Locales del Modelo y Pesos SafeTensors

**Feature Branch:** `feature/modelo-enfermedades-plantas` | **Spec:** [spec.md](./spec.md)

- [x] **TSK-016-01:** Versionar `config.json`, `preprocessor_config.json` y `model.safetensors` con Git LFS.
- [x] **TSK-016-02:** Implementar `verify_model_files()` en `src/model_loader.py`.
- [x] **TSK-016-03:** Validar manejo de `ModelLoadError` ante ausencia de archivos en `tests/unit/test_api_and_loader_mocked.py`.
