# Tasks (Spec Kit): SPEC-036 HU-08 Empaquetado Distribuible Python Wheel y sdist con Hatchling (uv build)

**Feature Branch:** `feature/hu08-wheel-docker-compose` | **Spec:** [spec.md](./spec.md)

- [x] **TSK-036-01:** Configurar `[tool.hatch.build]` en `pyproject.toml` para incluir `src`, `api`, `ui` y `ui/web/static/*`.
- [x] **TSK-036-02:** Verificar generación de `.whl` y `.tar.gz` con `uv build`.
- [x] **TSK-036-03:** Implementar pruebas de verificación en `tests/unit/test_hu08_packaging.py` (commit `f00859c`).
