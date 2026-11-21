---
name: Tarea Técnica / Gobernanza / M4
about: Registrar una tarea técnica o de infraestructura acotada y trazable a SPEC y Matriz M1–M4
title: "[TASK] "
labels: chore
---

## Trazabilidad

- **Unidad / Historia padre:** `[#__ / HU-XX / GOV-XX]`
- **Responsable:** `@usuario`
- **GitHub Projects:** Columna `[Backlog / In Progress (máx. 4) / In Review (máx. 2) / Done]`
- **IDs Matriz Académica ([docs/academic-compliance-matrix.md](../../docs/academic-compliance-matrix.md)):** `[M4-XX, TOOL-XX]`
- **Especificación SDD:** `specs/NNN-.../spec.md`
- **PR asociada:** `#__` *(completar al abrir PR usando la plantilla oficial sin modificarla)*
- **Skills aplicables:** [`quality-and-make`](../../.agents/skills/quality-and-make/SKILL.md) · [`github-gitlab-operations`](../../.agents/skills/github-gitlab-operations/SKILL.md) · [`secure-cicd-deployment`](../../.agents/skills/secure-cicd-deployment/SKILL.md)

## Objetivo Técnico

- [Descripción concreta del entregable y alcance acotado]

## Verificación y Evidencia de Aceptación

- [ ] **Evidencia de aceptación:** `[salida de make lint / make coverage / verificación documental o CI]`
- [ ] Cero secretos, rutas locales ni regresiones en capacidades protegidas.
- [ ] PR revisada por par humano y CI en verde antes de fusionar a `develop`.
