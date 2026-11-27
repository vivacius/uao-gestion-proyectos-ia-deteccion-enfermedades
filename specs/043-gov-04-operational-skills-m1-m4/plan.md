# Plan de Implementación (Spec Kit): SPEC-043 Skills Operativas M1–M4

**Identificador:** `SPEC-043`  
**Feature Branch:** `feature/gov-03a-agents-constitution-proposal`  
**Spec Asociada:** [spec.md](./spec.md) | **Tasks:** [tasks.md](./tasks.md)  
**Fecha de Elaboración SDD (Prospectiva):** 2026-11-21

---

## Pasos de Implementación y Verificación

1. Confirmar rama actual (`feature/gov-03a-agents-constitution-proposal`), cambios locales de `GOV-03A` y mecanismo oficial de descubrimiento de skills en Antigravity (`.agents/skills/<name>/SKILL.md`).
2. Redactar `SPEC-043` (`spec.md`, `plan.md`, `tasks.md`) antes de crear las skills.
3. Implementar las 5 skills concisas y enlazadas a `docs/academic-compliance-matrix.md` en `.agents/skills/`:
   - `academic-compliance`
   - `sdd-workflow`
   - `quality-and-make`
   - `github-gitlab-operations`
   - `secure-cicd-deployment`
4. Actualizar `AGENTS.md` (§ 5 o subsección breve) únicamente para indexar las 5 skills y cuándo activarlas, preservando íntegramente el contenido de `GOV-03A`.
5. Verificar estáticamente frontmatter YAML, enlaces relativos, ausencia de secretos/rutas locales, no interferencia con `.gitignore` (incluyendo cuarentena de `archify`) y preservación de recursos protegidos.
