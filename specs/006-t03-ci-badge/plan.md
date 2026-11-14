# Plan de Implementación (Spec Kit): T-03 Badge Real de CI

**Feature Branch:** `feature/t03-ci-badge`  
**Spec:** [spec.md](./spec.md)

1. Agregar el badge enlazado a `.github/workflows/ci.yml?branch=develop` en `README.md`.
2. Verificar la suite completa (`tests/unit` + `tests/integration`) y cobertura combinada con `uv run pytest -v --cov=src --cov=api`.
3. Abrir PR hacia `develop` y asignar revisión a `@JhonatanTC99`.
