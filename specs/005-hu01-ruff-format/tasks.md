# Tasks (Spec Kit): HU-01 Entorno Reproducible y Calidad con Ruff

**Feature Branch:** `feature/hu01-ruff-format` | **Issue:** #4

- [x] **TSK-HU01-01:** Crear rama `feature/hu01-ruff-format` desde `develop` (`cbe3c0e`).
- [x] **TSK-HU01-02:** Aplicar `uv run ruff format .` en los 5 archivos pendientes y verificar `ruff format --check .` + `ruff check .` con código `0`.
- [x] **TSK-HU01-03:** Verificar ausencia de `requirements*.txt` (AC1.3).
- [x] **TSK-HU01-04:** Suite unitaria verificada tras formateo (`157 passed, 1 skipped en 12.98s` en sandbox por Tcl/Tk, 98 % cobertura); PR hacia `develop` y validación de CI en curso.
