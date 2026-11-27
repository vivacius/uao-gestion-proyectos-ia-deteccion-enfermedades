# Plan de Implementación: Expansión de Suite Unitaria (`SPEC-051`)

1. `tests/unit/test_taxonomy_and_postprocessing_exhaustive.py`: pruebas parametrizadas sobre las 38 clases de `config.json`, `parse_category_label`, `clean_identifier` y `process_logits`.
2. `tests/unit/test_schemas_exceptions_and_preprocessing_unit.py`: pruebas de validación de `api/schemas.py`, jerarquía de `src/exceptions.py`, constantes/rutas de `src/config.py` y casos borde de `src/preprocessing.py`.
3. `tests/unit/test_client_scripts_and_m4_contracts.py`: pruebas con mocks de `ui/api_client.py`, helpers de `scripts/run_mlflow_benchmark.py` y `scripts/validate_e2e_and_benchmark.py`, y contratos de archivos M4 (`.gitlab-ci.yml`, `.github/workflows/mirror-to-gitlab.yml`, `deploy/docker-compose.prod.yml`).
4. Validación final con `ruff check .`, `ruff format --check .` y `pytest tests/unit --cov=src --cov=api`.
