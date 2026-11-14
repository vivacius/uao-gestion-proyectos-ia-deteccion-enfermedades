# Plan de Implementación (Spec Kit): SPEC-017 HU-03 Carga Local en CPU y Patrón Singleton Thread-Safe del Modelo

**Identificador:** `SPEC-017`  
**Feature Branch:** `feature/modelo-enfermedades-plantas`  
**Spec Asociada:** [spec.md](./spec.md)

---

## Pasos de Implementación y Verificación

1. Definir el dataclass `ModelBundle` (`model`, `processor`, `device`, `id2label`, `label2id`, `model_dir`, `architecture`).
2. Implementar `load_model_bundle()` forzando `local_files_only=True`, `.to('cpu')` y `.eval()`.
3. Implementar `get_model_bundle()` y `clear_model_bundle_cache()` con `threading.Lock()`.
