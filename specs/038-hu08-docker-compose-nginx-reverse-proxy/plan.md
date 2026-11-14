# Plan de Implementación (Spec Kit): SPEC-038 HU-08 Orquestación Docker Compose (API + Web Nginx) y Proxy Same-Origin

**Identificador:** `SPEC-038`  
**Feature Branch:** `feature/hu08-wheel-docker-compose`  
**Spec Asociada:** [spec.md](./spec.md)

---

## Pasos de Implementación y Verificación

1. Crear `deploy/nginx.conf` sirviendo `/usr/share/nginx/html` y enrutando endpoints REST/OpenAPI a `http://api:8000`.
2. Definir servicios `api` y `web` en `docker-compose.yml` con volúmenes `:ro` y `depends_on: condition: service_healthy`.
3. Documentar comandos de operación en la sección 8 del `README.md`.
