# Tasks (Spec Kit): SPEC-042 Operacionalización M1–M4 en `AGENTS.md` y Propuesta Constitucional

**Feature Branch:** `feature/gov-03a-agents-constitution-proposal` | **Spec:** [spec.md](./spec.md) | **Plan:** [plan.md](./plan.md) | **Fecha SDD (Prospectiva):** 2026-11-21

- [x] **TSK-042-01:** Verificar `develop` limpio y crear rama `feature/gov-03a-agents-constitution-proposal`.
- [x] **TSK-042-02:** Crear especificación prospectiva `SPEC-042` (`spec.md`, `plan.md`, `tasks.md`) antes de modificar `AGENTS.md`.
- [x] **TSK-042-03:** Actualizar `AGENTS.md` incorporando jerarquía M1–M4, reglas académicas, conservación, procedimiento, herramientas (`Makefile`, `gh`, `glab`, MCPs), estado vigente y eliminación de obsolescencias.
- [x] **TSK-042-04:** Crear `docs/constitutional-amendment-m1-m4-proposal.md` con propuesta detallada de enmienda constitucional sin tocar `.specify/memory/constitution.md`.
- [x] **TSK-042-05:** Verificar coherencia, enlaces, ausencia de secretos e integridad de recursos protegidos (`git diff`, `git status`) sin ejecutar `pytest` completo ni Docker.

---

## Pendientes diferidos a unidades posteriores (no implementados en `GOV-03A`)

- **Para Skills futuras:** procedimientos repetibles de verificación pre-PR (`ruff`, cobertura, chequeo de capacidades protegidas), flujo SDD prospectivo paso a paso, y operación/diagnóstico seguro con `gh`, `glab` y MCPs.
- **Para Spec Kit posterior:**
  - Actualización de `.github/PULL_REQUEST_TEMPLATE.md` (`D-09`) para alinear textos M1 a M1–M4 y citar IDs de matriz.
  - Enmienda formal de `.specify/memory/constitution.md` (`M4-09`) tras aprobación unánime del Grupo 2.
  - Especificación y arquitectura de integración GitHub ↔ GitLab (`TOOL-05`), pipeline `.gitlab-ci.yml` (`M4-03`, `M4-05`), provisión VPS/HTTPS/secretos (`M4-01`, `M4-02`, `M4-06`, `M4-07`) y decisión sobre `requires-python` (`D-03`) y cuarentena de Archify (`D-06`).
