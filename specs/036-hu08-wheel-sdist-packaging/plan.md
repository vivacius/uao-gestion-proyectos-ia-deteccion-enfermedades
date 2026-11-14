# Plan de Implementación (Spec Kit): SPEC-036 HU-08 Empaquetado Distribuible Python Wheel y sdist con Hatchling (uv build)

**Identificador:** `SPEC-036`  
**Feature Branch:** `feature/hu08-wheel-docker-compose`  
**Spec Asociada:** [spec.md](./spec.md)

---

## Pasos de Implementación y Verificación

1. Configurar `packages = ["src", "api", "ui"]` y `artifacts = ["ui/web/static/*"]` en `pyproject.toml`.
2. Configurar exclusiones en `.dockerignore` y `.gitignore` (`dist/`).
3. Crear pruebas automatizadas de empaquetado en `tests/unit/test_hu08_packaging.py`.
