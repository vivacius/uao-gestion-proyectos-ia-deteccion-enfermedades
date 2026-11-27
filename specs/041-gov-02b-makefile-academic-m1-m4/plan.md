# Plan de Implementación (Spec Kit): SPEC-041 Makefile Académico M1–M4 y Estándar Operativo

**Identificador:** `SPEC-041`  
**Feature Branch:** `feature/docs`  
**Spec Asociada:** [spec.md](./spec.md) | **Tasks:** [tasks.md](./tasks.md)  
**Fecha de Elaboración SDD (Prospectiva):** 2026-11-21  

---

## Pasos de Implementación y Verificación

1. Verificar estado Git en `feature/docs`, disponibilidad de `make`, `uv`, `docker` y comandos reales del proyecto (`pyproject.toml`, `.github/workflows/ci.yml`, `Dockerfile`, `docker-compose.yml`, `scripts/verify_mlflow_server.py`).
2. Implementar `Makefile` en la raíz con `.DEFAULT_GOAL := help`, `.PHONY`, variables parametrizables (`UV`, `DOCKER`, `DOCKER_COMPOSE`, `HOST`, `PORT`, `MLFLOW_PORT`, `IMAGE_TAG`) y los 17 targets requeridos, sin duplicación ni comandos destructivos.
3. Validar compatibilidad Windows 11 / Linux y ejecutar de forma segura los comandos subyacentes de lectura/QA disponibles (`uv run ruff check .`, `uv run ruff format --check .`, `uv run pytest tests/unit`, etc. o `make` si estuviera disponible).
4. Actualizar `docs/academic-compliance-matrix.md` registrando el `Makefile` como recomendación docente + `DECISIÓN` operativa (`TOOL-09`), vinculándolo a `M1`–`M4` y anotando la evidencia real de validación.
5. Actualizar `README.md` únicamente con la sección de uso del `Makefile` y sus requisitos.
6. Confirmar mediante `git status` y `git diff` que ninguna capacidad protegida fue modificada.
