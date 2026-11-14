# Plan de Implementación (Spec Kit): SPEC-037 HU-08 Contenerización Docker CPU Multi-Etapa con Usuario No-Root y Healthcheck

**Identificador:** `SPEC-037`  
**Feature Branch:** `feature/hu08-wheel-docker-compose`  
**Spec Asociada:** [spec.md](./spec.md)

---

## Pasos de Implementación y Verificación

1. Redactar `.dockerignore` excluyendo `.git`, `.venv`, `tests`, `docs`, `documento` y cachés.
2. Implementar las 3 etapas en `Dockerfile` (`ghcr.io/astral-sh/uv:0.13.1`, `builder` y `runtime`).
3. Configurar usuario `appuser`, variables de entorno, `HEALTHCHECK` y `CMD ["uvicorn", ...]`.
