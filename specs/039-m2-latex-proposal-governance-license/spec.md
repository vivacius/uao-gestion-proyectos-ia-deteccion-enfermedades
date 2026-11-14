# Especificación Técnica (Spec Kit): SPEC-039 Propuesta Formal M2 en LaTeX, Gobernanza AGENTS.md y Licenciamiento Dual

**Identificador:** `SPEC-039`  
**Feature Branch:** `chore/t02-licencia-y-atribuciones`  
**Historia / Issue Asociado:** M2 / T-02 (PR [#13](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/pull/13), PR [#14](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/pull/14), PR [#23](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/pull/23))  
**Responsable:** Santiago Correa Campaña (`@vivacius`)  
**Revisor Asignado:** Jhonatan Andrés Tapia Córdoba (`@JhonatanTC99`)  
**Fecha:** 2026-11-12  
**Estado:** Completado y verificado en `develop`

---

## 1. Propósito y Alcance
Consolidar los artefactos documentales, legales y de gobernanza del proyecto: el documento formal de propuesta del Módulo 2 en LaTeX (`documento/Plantilla.tex` y `Plantilla.pdf`), las reglas operativas para agentes de IA y matriz de responsabilidades (`AGENTS.md`, `.specify/memory/constitution.md`) y el archivo `LICENSE` detallando la licencia MIT del código fuente junto con las atribuciones obligatorias CC BY-SA 4.0 (pesos), Apache 2.0 (DINOv2) y CC BY-SA 3.0 (PlantVillage).

## 2. Escenarios de Aceptación (Gherkin)

### AC39.1 — Licenciamiento transparente y atribuciones de terceros (T-02)
- **Dado** el archivo `LICENSE` y la sección 11 del `README.md`,
- **Cuando** se audita el cumplimiento legal de código, pesos y datos,
- **Entonces** se distingue explícitamente la licencia MIT del código propio respecto de las licencias CC BY-SA 4.0, Apache 2.0 y CC BY-SA 3.0 de los artefactos de terceros.

### AC39.2 — Gobernanza humano-agente y trazabilidad M2-M3
- **Dado** los documentos `AGENTS.md`, `.specify/memory/constitution.md` y `documento/Plantilla.pdf`,
- **Cuando** se revisa la asignación de las 8 historias de usuario (21 SP),
- **Entonces** existe trazabilidad completa entre integrantes, historias HU-01 a HU-08, ramas y Pull Requests.
