# Plan de Implementación (Spec Kit): SC-02 Validación E2E y Benchmarks

**Feature Branch:** `feature/sc02-e2e-benchmarks`  
**Issue:** #30 | **Spec:** [spec.md](./spec.md)

1. Verificar entorno `uv`, `ruff check .`, `ruff format --check .`, `pytest tests/unit` y `pytest tests/integration` sobre el HEAD de `develop` (`c51e3fb`).
2. Implementar `scripts/validate_e2e_and_benchmark.py` usando únicamente dependencias existentes en `.venv` (sin modificar `pyproject.toml` ni `uv.lock`) para:
   - Validar `GET /`, `GET /health`, `GET /model-info`, `GET /docs` y `POST /predict` (válida + error HTTP 400/415).
   - Medir por separado inferencia CPU pura (`predict_from_bytes`) y latencia HTTP E2E (`POST /predict` secuencial y concurrente con `ThreadPoolExecutor`), calculando min, media, p50, p95, max, RAM (RSS) y CPU.
3. Ejecutar el script y registrar las salidas reales en `docs/qa-e2e-benchmarks.md`.
4. Verificar Ruff en los archivos nuevos, hacer commit, push y abrir PR hacia `develop` para revisión de `@JhonatanTC99`.
