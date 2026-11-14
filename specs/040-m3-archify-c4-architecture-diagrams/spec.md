# Especificación Técnica (Spec Kit): SPEC-040 Diagramación Arquitectónica C4 con Archify y Visualización en README

**Identificador:** `SPEC-040`  
**Feature Branch:** `docs/readme-archify-png`  
**Historia / Issue Asociado:** M3 Arquitectura (PR [#36](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/pull/36), PR [#37](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/pull/37))  
**Responsable:** Santiago Correa Campaña (`@vivacius`)  
**Revisor Asignado:** Jhonatan Andrés Tapia Córdoba (`@JhonatanTC99`)  
**Fecha de Implementación de la Unidad:** 2026-11-13 (13/11/2026)  
**Fecha de Documentación SDD (Retrospectiva):** 2026-11-14 (14/11/2026)  
**Trazabilidad Temporal:** Especificación documentada retrospectivamente el 14/11/2026 (no elaborada antes de implementar; la fecha histórica 2026-11-13 corresponde a la implementación de la unidad)  
**Estado:** Completado y verificado en `develop` y `main` (M3)  
**Artefactos Relacionados:** [plan.md](./plan.md) · [tasks.md](./tasks.md)

---

## 1. Propósito y Alcance
Generar y versionar en `docs/architecture/` los artefactos declarativos de arquitectura del sistema elaborados con **Archify** (`docs/architecture/system-architecture.json`, vista interactiva `system-architecture.html`, vectorial `system-architecture.svg` e imagen rasterizada `system-architecture.png`) y embeber el diagrama en la sección 2 del `README.md` para su correcta visualización directa en GitHub.

## 2. Escenarios de Aceptación (Gherkin)

### AC40.1 — Artefactos de arquitectura sincronizados con el código real
- **Dado** los archivos en `docs/architecture/`,
- **Cuando** se inspeccionan las capas y componentes representados,
- **Entonces** reflejan fielmente los módulos de presentación (`ui/desktop_app.py`, `ui/web/static/`, Nginx), servicio REST (`api/main.py`) y núcleo de inferencia (`src/`).

### AC40.2 — Renderizado directo en GitHub mediante PNG
- **Dado** la sección 2 (`Arquitectura del Sistema`) de `README.md`,
- **Cuando** se visualiza el repositorio en GitHub,
- **Entonces** el diagrama `docs/architecture/system-architecture.png` se muestra embebido con enlaces a las vistas `.svg` y `.html`.
