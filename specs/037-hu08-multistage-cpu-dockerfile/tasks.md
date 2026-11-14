# Tasks (Spec Kit): SPEC-037 HU-08 Contenerización Docker CPU Multi-Etapa con Usuario No-Root y Healthcheck

**Feature Branch:** `feature/hu08-wheel-docker-compose` | **Spec:** [spec.md](./spec.md)

- [x] **TSK-037-01:** Crear `.dockerignore` optimizado para contexto de construcción ligero.
- [x] **TSK-037-02:** Implementar `Dockerfile` multi-etapa con usuario `appuser` y `HEALTHCHECK` (commit `f00859c`).
- [x] **TSK-037-03:** Validar estructura del `Dockerfile` en `tests/unit/test_hu08_packaging.py`.
