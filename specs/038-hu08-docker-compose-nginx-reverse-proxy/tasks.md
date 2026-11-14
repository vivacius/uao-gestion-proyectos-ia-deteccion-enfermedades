# Tasks (Spec Kit): SPEC-038 HU-08 Orquestación Docker Compose (API + Web Nginx) y Proxy Same-Origin

**Feature Branch:** `feature/hu08-wheel-docker-compose` | **Spec:** [spec.md](./spec.md)

- [x] **TSK-038-01:** Crear `deploy/nginx.conf` con configuración de proxy inverso same-origin.
- [x] **TSK-038-02:** Crear `docker-compose.yml` orquestando `plant-disease-api` y `plant-disease-web`.
- [x] **TSK-038-03:** Validar contratos de Compose y Nginx en `tests/unit/test_hu08_packaging.py` y fusionar PR #33.
