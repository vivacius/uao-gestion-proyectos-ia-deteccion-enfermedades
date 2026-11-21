# Plan de Implementación (Spec Kit): SPEC-044 Alineación de Plantillas Spec Kit, PR e Issues

**Identificador:** `SPEC-044`  
**Feature Branch:** `feature/gov-03a-agents-constitution-proposal`  
**Spec Asociada:** [spec.md](./spec.md) | **Tasks:** [tasks.md](./tasks.md)  
**Fecha de Elaboración SDD (Prospectiva):** 2026-11-21

---

## Pasos de Implementación y Verificación

1. Confirmar rama actual (`feature/gov-03a-agents-constitution-proposal`), cambios acumulados de `GOV-03A` + `GOV-04` y separar archivos propios de Spec Kit 1.2.2 de plantillas mantenibles por el proyecto.
2. Crear `SPEC-044` (`spec.md`, `plan.md`, `tasks.md`) antes de editar plantillas.
3. Adaptar `.specify/templates/spec-template.md`, `plan-template.md` y `tasks-template.md` manteniendo la estructura esperada por `/speckit.specify`, `/speckit.plan` y `/speckit.tasks`, incorporando requisitos `M1`–`M4`, capacidades protegidas, `Makefile`, skills de `GOV-04` y reglas de autorización Git.
4. Actualizar `.github/PULL_REQUEST_TEMPLATE.md` (`D-09`) eliminando referencias obsoletas de M1 y diferenciando evidencia real vs pendiente.
5. Añadir plantillas mínimas en `.github/ISSUE_TEMPLATE/` (`user-story.md`, `technical-task.md`) orientadas a trazabilidad `Issue ↔ SPEC ↔ PR` sin duplicar specs.
6. Verificar compatibilidad con Spec Kit 1.2.2, coherencia transversal con Constitución / `AGENTS.md` / Matriz / Skills / `Makefile`, enlaces relativos y ausencia de secretos, sin ejecutar `pytest` completo ni Docker.
