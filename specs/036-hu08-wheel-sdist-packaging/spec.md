# Especificación Técnica (Spec Kit): SPEC-036 HU-08 Empaquetado Distribuible Python Wheel y sdist con Hatchling (uv build)

**Identificador:** `SPEC-036`  
**Feature Branch:** `feature/hu08-wheel-docker-compose`  
**Historia / Issue Asociado:** HU-08 (Issue [#11](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/11) · 2 SP · PR [#33](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/pull/33))  
**Responsable:** José Isaac Silva Calderón (`@josesilvacalderon111`)  
**Revisor Asignado:** Jhonatan Andrés Tapia Córdoba (`@JhonatanTC99`)  
**Fecha:** 2026-11-13  
**Estado:** Completado y verificado en `develop`

---

## 1. Propósito y Alcance
Configurar el sistema de construcción **Hatchling** en `pyproject.toml` (`[build-system]` y `[tool.hatch.build.targets.wheel]`) para que `uv build` genere artefactos estándar de distribución Python (`plant_disease_classifier-1.0.0-py3-none-any.whl` y `.tar.gz`) incluyendo los paquetes `src`, `api`, `ui` y los activos estáticos `ui/web/static/*`.

## 2. Escenarios de Aceptación (Gherkin)

### AC36.1 — Construcción limpia de Wheel y sdist (AC8.1)
- **Dado** la configuración de `hatchling` en `pyproject.toml`,
- **Cuando** se ejecuta `uv build`,
- **Entonces** se generan en `dist/` los archivos `.whl` y `.tar.gz` sin errores.

### AC36.2 — Inclusión verificada de módulos y activos web en el Wheel
- **Dado** el archivo `.whl` generado,
- **Cuando** se inspecciona su contenido interno (`zipfile`),
- **Entonces** contiene `src/`, `api/`, `ui/` y `ui/web/static/index.html`, y excluye artefactos obsoletos como `streamlit_app.py`.
