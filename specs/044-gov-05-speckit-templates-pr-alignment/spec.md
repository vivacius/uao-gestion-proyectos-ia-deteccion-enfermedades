# Especificación Técnica (Spec Kit): SPEC-044 Alineación de Plantillas Spec Kit, PR e Issues con Gobernanza M1–M4

**Identificador:** `SPEC-044`  
**Feature Branch:** `feature/gov-03a-agents-constitution-proposal`  
**Unidad / Historia Asociada:** `GOV-05` (Alineación SDD y revisión Git `M1`–`M4`)  
**Fecha de Elaboración SDD (Prospectiva):** 2026-11-21  
**Trazabilidad Temporal:** **Especificación prospectiva elaborada ANTES de adaptar las plantillas en `.specify/templates/` y `.github/`.**  
**Estado:** En progreso (`GOV-05`)  
**Artefactos Relacionados:** [plan.md](./plan.md) · [tasks.md](./tasks.md) · [AGENTS.md](../../AGENTS.md) · [Matriz Académica](../../docs/academic-compliance-matrix.md)

---

## 1. Propósito y Alcance
Alinear las plantillas mantenibles por el proyecto (`.specify/templates/spec-template.md`, `.specify/templates/plan-template.md`, `.specify/templates/tasks-template.md`, `.github/PULL_REQUEST_TEMPLATE.md` y plantillas mínimas de Issues en `.github/ISSUE_TEMPLATE/`) con la gobernanza acumulada `M1`–`M4`, `AGENTS.md`, las 5 skills de `GOV-04`, el `Makefile` y la matriz académica, preservando intactos los archivos propios de la instalación de Spec Kit 1.2.2 (`.specify/scripts/`, `.specify/workflows/`, `.specify/integration.json`, `.gemini/commands/speckit.*.toml`), `.specify/memory/constitution.md` y `specs/001..043/`.

---

## 2. Escenarios de Aceptación (Gherkin)

### AC44.1 — Plantillas Spec Kit (`spec`, `plan`, `tasks`) alineadas a `M1`–`M4`
- **Dado** las plantillas en `.specify/templates/` (`spec-template.md`, `plan-template.md`, `tasks-template.md`),
- **Cuando** se actualizan bajo `GOV-05`,
- **Entonces** incorporan todos los campos requeridos por `AGENTS.md`, `docs/academic-compliance-matrix.md` (`M1..M4`, `TOOL-XX`, 10 capacidades protegidas), prohibición de Streamlit/`pip`/`.ipynb`, uso de `Makefile`/`uv`/`ruff`/`pytest`, compatibilidad Windows/Linux/CI, separación implementación/validación/publicación/integración, prohibición de operaciones remotas sin autorización, fecha/condición prospectiva y referencias a las 5 skills de `.agents/skills/`.

### AC44.2 — Plantilla de Pull Request (`.github/PULL_REQUEST_TEMPLATE.md`) actualizada
- **Dado** `.github/PULL_REQUEST_TEMPLATE.md` con texto heredado de M1 (`D-09`),
- **Cuando** se actualiza,
- **Entonces** elimina ejemplos genéricos obsoletos de M1, conserva los principios de calidad heredados (cohesión, acoplamiento, Conventional Commits), referencia historia/Issue y `SPEC-NNN`, verifica capacidades protegidas y secretos, requiere CI verde y revisión cruzada, y diferencia pruebas ejecutadas de pruebas pendientes sin marcar casillas sin evidencia.

### AC44.3 — Plantillas mínimas de Issues compatibles con GitHub Projects y SDD
- **Dado** el flujo GitHub Projects + Spec Kit,
- **Cuando** se evalúa `.github/ISSUE_TEMPLATE/`,
- **Entonces** existen únicamente dos plantillas mínimas (`user-story.md` y `technical-task.md`) que enlazan a `SPEC-NNN` y `docs/academic-compliance-matrix.md` sin duplicar especificaciones completas.

### AC44.4 — Preservación de Spec Kit 1.2.2, Constitución y cambios previos
- **Dado** los artefactos protegidos y cambios acumulados de `GOV-03A` + `GOV-04`,
- **Cuando** finaliza `GOV-05`,
- **Entonces** permanecen intactos `.specify/memory/constitution.md`, `.specify/workflows/`, `.specify/scripts/`, `.gemini/commands/speckit.*.toml`, `Makefile`, `Dockerfile`, `.github/workflows/ci.yml`, `src/`, `api/`, `ui/`, `tests/`, `specs/001..043/` y los cambios previos de `GOV-03A` y `GOV-04`.
