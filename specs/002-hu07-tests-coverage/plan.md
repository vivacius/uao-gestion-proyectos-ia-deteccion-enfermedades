# Plan de Implementación (Spec Kit): HU-07 Aislamiento de Pruebas Unitarias y Cobertura

**Feature Branch:** `feature/hu07-tests-coverage`  
**Spec:** [spec.md](./spec.md)

## Enfoque Técnico
1. Mantener intactos los módulos funcionales de `src/` y `api/` asignados a José, Jhonatan y John para evitar conflictos de fusión.
2. Agregar pruebas unitarias aisladas con `unittest.mock.patch` y `SimpleNamespace` en `tests/unit/test_api_and_loader_mocked.py` cubriendo:
   - `load_model_from_disk` (camino feliz con `local_files_only=True`, `cpu`, `eval()`, mapeos `id2label`/`label2id`).
   - `get_model_bundle` (patrón singleton, `force_reload=True` y cambio de ruta).
   - `predict_from_bytes` (flujo completo con `ModelBundle` simulado, envoltura de errores inesperados en `InferenceError` y propagación directa de `ImageValidationError`).
   - `lifespan` de `api/main.py` (arranque exitoso y degradado sin lectura real de `model.safetensors`).
3. Validar con `uv run ruff check`, `uv run ruff format --check` y `uv run pytest tests/unit --cov=src --cov=api`.
4. Abrir Pull Request hacia `develop` usando `.github/PULL_REQUEST_TEMPLATE.md` y asignar a **Jhonatan Tapia** como Code Reviewer.
