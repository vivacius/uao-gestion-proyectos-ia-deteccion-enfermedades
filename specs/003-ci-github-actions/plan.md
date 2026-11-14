# Plan de Implementación (Spec Kit): T-04 Quality Gate en GitHub Actions

**Feature Branch:** `feature/ci-github-actions`  
**Spec:** [spec.md](./spec.md)

## Enfoque Técnico
1. Definir `.github/workflows/ci.yml` con `ubuntu-latest`, `actions/checkout@v4` y `astral-sh/setup-uv@v5` (Python 3.13).
2. Ejecutar únicamente controles ligeros compatibles con runners sin GPU ni pesos locales:
   - `uv sync --frozen`
   - `uv run ruff check .`
   - `uv run ruff format --check .`
   - `uv run pytest tests/unit -v --cov=src --cov=api --cov-report=term-missing`
3. Abrir Pull Request hacia `develop` usando `.github/PULL_REQUEST_TEMPLATE.md` y verificar la ejecución real del workflow en GitHub Actions.
