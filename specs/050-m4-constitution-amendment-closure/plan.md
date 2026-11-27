# Implementation Plan: Enmienda Constitucional M4, Cierre Kanban y Sustentación

**Branch**: `feature/m4-plan-01-specs-048-050` | **Date**: 2026-11-23 | **Spec**: [spec.md](spec.md)

**Input**: Issue `#52` — `/specs/050-m4-constitution-amendment-closure/spec.md`

## Summary

Ejecutar en dos carriles coordinados el cierre de gobernanza M4: (1) redacción y votación unánime de la Enmienda Constitucional M4 (`.specify/memory/constitution.md`, desacoplada de la espera de VPS), y (2) actualización final de `docs/academic-compliance-matrix.md`, cierre de métricas Kanban en Project #1 y preparación de la sustentación del `28/11/2026` tras las evidencias de `#51`.

## Technical Context

**Language/Version**: Markdown / GitHub Projects (`gh 2.105.0`) / `glab 1.131.0`

**Primary Dependencies**: Consenso unánime de los 4 integrantes para enmienda; evidencias de `#51` para cierre final de matriz

**Storage**: `.specify/memory/constitution.md`, `docs/academic-compliance-matrix.md`, GitHub Project #1

**Testing**: `uv run ruff check .`, revisión cruzada de 4 integrantes y verificación de enlaces/evidencias reales

**Target Platform**: GitHub + documentación del repositorio

**Project Type**: Gobernanza académica M4

**Constraints**: Prohibido editar la Constitución sin aprobación unánime; prohibido marcar `VERIFICADO` sin evidencia real

## Constitution Check

- **Gobernanza y Enmiendas (§ final):** Cumplido — requiere consenso unánime de los 4 integrantes del Grupo 2.

## Project Structure

```text
specs/050-m4-constitution-amendment-closure/
├── spec.md
├── plan.md
└── tasks.md
```

**Structure Decision**: Sin cambios de código de aplicación ni CI/CD; cambios exclusivos en gobernanza y documentación.

---

<!-- [M1-M4 GOVERNANCE EXTENSION] -->
## M1–M4 Governance, Makefile & Security Gate

> **Referencias normativas:** [AGENTS.md](../../AGENTS.md) · [Constitución](../../.specify/memory/constitution.md) · [Matriz Académica M1–M4](../../docs/academic-compliance-matrix.md)

- **Validación:** Verificar que los enlaces a evidencias existan y que ningún secreto aparezca en reportes de cierre.
<!-- [/M1-M4 GOVERNANCE EXTENSION] -->
