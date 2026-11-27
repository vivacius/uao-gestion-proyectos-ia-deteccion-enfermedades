---
name: Historia de Usuario (SDD M1–M4)
about: Registrar una historia de usuario trazable a GitHub Projects, matriz M1–M4 y SPEC prospectiva
title: "[HU-XX] "
labels: enhancement
---

## Trazabilidad Académica, Kanban y SDD

- **ID Historia / Unidad:** `HU-XX` / `[M4-XX]`
- **Responsable:** `@usuario`
- **GitHub Projects:** Columna `[Backlog / In Progress (máx. 4) / In Review (máx. 2) / Done]`
- **IDs Matriz Académica ([docs/academic-compliance-matrix.md](../../docs/academic-compliance-matrix.md)):** `[M1-XX..M4-XX, TOOL-XX]`
- **Especificación SDD prospectiva:** `specs/NNN-.../spec.md` *(crear antes de implementar)*
- **Estimación (Fibonacci):** `[1 / 2 / 3 / 5 SP]`
- **PR asociada:** `#__` *(completar al abrir PR usando la plantilla oficial sin modificarla)*
- **Skills aplicables:** [`academic-compliance`](../../.agents/skills/academic-compliance/SKILL.md) · [`sdd-workflow`](../../.agents/skills/sdd-workflow/SKILL.md)

## Descripción (Como / Quiero / Para)

- **Como** [rol de usuario o sistema],
- **Quiero** [capacidad requerida],
- **Para** [valor o cumplimiento de hito].

## Criterios de Aceptación (Resumen Given-When-Then)

1. **Given** [contexto], **When** [acción], **Then** [resultado verificable].

## Invariantes, Evidencia y Definición de Terminado (DoD)

- [ ] Especificación prospectiva (`SPEC-NNN`) creada antes de codificar.
- [ ] Capacidades protegidas (Matriz § 2) y prohibiciones (`Streamlit`, `pip`, `.ipynb`) respetadas.
- [ ] **Evidencia de aceptación:** `[salida de pruebas AAA, Ruff, cobertura o verificación documental]`
- [ ] PR revisada por par y CI en verde hacia `develop`.
