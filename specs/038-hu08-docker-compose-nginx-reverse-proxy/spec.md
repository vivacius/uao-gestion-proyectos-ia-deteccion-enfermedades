# Especificación Técnica (Spec Kit): SPEC-038 HU-08 Orquestación Docker Compose (API + Web Nginx) y Proxy Same-Origin

**Identificador:** `SPEC-038`  
**Feature Branch:** `feature/hu08-wheel-docker-compose`  
**Historia / Issue Asociado:** HU-08 (Issue [#11](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/11) · 2 SP · PR [#33](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/pull/33))  
**Responsable:** José Isaac Silva Calderón (`@josesilvacalderon111`)  
**Revisor Asignado:** Jhonatan Andrés Tapia Córdoba (`@JhonatanTC99`)  
**Fecha de Implementación de la Unidad:** 2026-11-13 (13/11/2026)  
**Fecha de Documentación SDD (Retrospectiva):** 2026-11-14 (14/11/2026)  
**Trazabilidad Temporal:** Especificación documentada retrospectivamente el 14/11/2026 (no elaborada antes de implementar; la fecha histórica 2026-11-13 corresponde a la implementación de la unidad)  
**Estado:** Completado y verificado en `develop`

---

## 1. Propósito y Alcance
Orquestar en `docker-compose.yml` y `deploy/nginx.conf` el despliegue conjunto de los dos contenedores del sistema: `plant-disease-api` (FastAPI + DINOv2 en CPU en el puerto `8000`) y `plant-disease-web` (`nginx:1.27-alpine` en el puerto `8080`), sincronizando el arranque con `condition: service_healthy` y configurando un proxy inverso *same-origin* hacia `http://api:8000`.

## 2. Escenarios de Aceptación (Gherkin)

### AC38.1 — Arranque sincronizado por salud del modelo (AC8.3)
- **Dado** la definición de servicios en `docker-compose.yml`,
- **Cuando** se ejecuta `docker compose up -d`,
- **Entonces** el contenedor `plant-disease-web` espera a que `plant-disease-api` alcance el estado `healthy` antes de iniciar.

### AC38.2 — Proxy inverso Same-Origin libre de CORS en el puerto 8080
- **Dado** la configuración `deploy/nginx.conf` montada en `plant-disease-web`,
- **Cuando** el usuario accede a `http://localhost:8080` y a `/predict`, `/health`, `/model-info` o `/docs`,
- **Entonces** Nginx sirve el frontend estático en `/` y redirige las rutas de la API a `http://api:8000` con límite de cuerpo de `12m`.
