# Plan de Implementación (Spec Kit): HU-01 Normalización Ruff

**Feature Branch:** `feature/hu01-ruff-format`  
**Spec:** [spec.md](./spec.md)

1. Ejecutar `uv run ruff format .` únicamente para normalizar estilo sin alterar lógica funcional.
2. Validar `uv run ruff format --check .`, `uv run ruff check .` y ausencia de `requirements*.txt`.
3. Ejecutar `uv run pytest tests/unit -v --cov=src --cov=api --cov-report=term-missing` verificando 0 regresiones.
4. Abrir PR hacia `develop` y comprobar que el workflow `Quality Gate CI (M3)` en GitHub Actions pase completo en verde.
