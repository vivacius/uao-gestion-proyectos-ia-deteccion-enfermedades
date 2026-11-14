# Especificación Técnica (Spec Kit): SPEC-037 HU-08 Contenerización Docker CPU Multi-Etapa con Usuario No-Root y Healthcheck

**Identificador:** `SPEC-037`  
**Feature Branch:** `feature/hu08-wheel-docker-compose`  
**Historia / Issue Asociado:** HU-08 (Issue [#11](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/11) · 2 SP · PR [#33](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/pull/33))  
**Responsable:** José Isaac Silva Calderón (`@josesilvacalderon111`)  
**Revisor Asignado:** Jhonatan Andrés Tapia Córdoba (`@JhonatanTC99`)  
**Fecha:** 2026-11-13  
**Estado:** Completado y verificado en `develop`

---

## 1. Propósito y Alcance
Diseñar e implementar un `Dockerfile` multi-etapa en 3 fases (`uv` $\rightarrow$ `builder` $\rightarrow$ `runtime`) basado en `python:3.13-slim` que instale exclusivamente dependencias de producción sobre CPU desde `uv.lock` (`--frozen --no-dev`), ejecute bajo un usuario sin privilegios (`appuser`, UID 10001), incorpore los pesos locales en `/app/modelo_plantas/` y configure un `HEALTHCHECK` nativo contra `GET /health`.

## 2. Escenarios de Aceptación (Gherkin)

### AC37.1 — Imagen runtime limpia sin uv ni herramientas de desarrollo (AC8.2)
- **Dado** el `Dockerfile` de 3 etapas,
- **Cuando** se construye la etapa final `runtime`,
- **Entonces** solo contiene `/opt/venv` de producción, `src/`, `api/`, `ui/web/static` y `/app/modelo_plantas/`, sin el binario `uv` ni paquetes de `dev`.

### AC37.2 — Ejecución segura no-root y sonda de salud integrada
- **Dado** un contenedor iniciado desde `plant-disease-classifier:1.0.0`,
- **Cuando** se inspecciona su proceso y estado en Docker,
- **Entonces** corre bajo el usuario `appuser` (UID 10001), expone el puerto `8000` y reporta estado `healthy` al responder `/health`.
