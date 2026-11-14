# Tasks (Spec Kit): SPEC-010 HU-01 Inicialización Determinista con uv y Python 3.13

**Feature Branch:** `feature/hu01-uv-bootstrap` | **Spec:** [spec.md](./spec.md)

- [x] **TSK-010-01:** Configurar `.python-version` y `pyproject.toml` con dependencias de CPU y desarrollo.
- [x] **TSK-010-02:** Generar y versionar `uv.lock` verificando resolución determinista con `uv sync --frozen`.
- [x] **TSK-010-03:** Configurar secciones `[tool.ruff]` y `[tool.pytest.ini_options]` en `pyproject.toml`.
- [x] **TSK-010-04:** Documentar comandos de instalación reproducible en `docs/getting-started.md` y `README.md`.
