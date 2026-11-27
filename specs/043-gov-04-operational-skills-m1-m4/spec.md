# Especificación Técnica (Spec Kit): SPEC-043 Skills Operativas M1–M4 y Coordinación GitHub/GitLab

**Identificador:** `SPEC-043`  
**Feature Branch:** `feature/gov-03a-agents-constitution-proposal`  
**Unidad / Historia Asociada:** `GOV-04` (Operacionalización de Skills M1–M4)  
**Fecha de Elaboración SDD (Prospectiva):** 2026-11-21  
**Trazabilidad Temporal:** **Especificación prospectiva elaborada ANTES de crear las skills en `.agents/skills/`.**  
**Estado:** En progreso (`GOV-04`)  
**Artefactos Relacionados:** [plan.md](./plan.md) · [tasks.md](./tasks.md) · [AGENTS.md](../../AGENTS.md) · [Matriz Académica](../../docs/academic-compliance-matrix.md)

---

## 1. Propósito y Alcance
Crear el conjunto mínimo de 5 skills operativas locales bajo la convención nativa de Antigravity (`.agents/skills/<name>/SKILL.md`), separadas por responsabilidad, para que los agentes ejecuten unidades de trabajo respetando los requisitos acumulativos `M1`–`M4`, las 10 capacidades protegidas, el flujo SDD prospectivo, el `Makefile` y la coordinación segura GitHub/GitLab y CI/CD M4, sin duplicar la matriz ni modificar código funcional, Constitución, `Makefile`, Docker, CI o `archify` (en cuarentena).

---

## 2. Escenarios de Aceptación (Gherkin)

### AC43.1 — Descubrimiento nativo y estructura válida de skills
- **Dado** el directorio `.agents/skills/` en la raíz del repositorio,
- **Cuando** se crean las 5 skills (`academic-compliance`, `sdd-workflow`, `quality-and-make`, `github-gitlab-operations`, `secure-cicd-deployment`),
- **Entonces** cada una reside en `.agents/skills/<name>/SKILL.md` con *frontmatter* YAML válido (`name`, `description`), es descubrible automáticamente por Antigravity sin tocar `.agents/skills/archify/` (ignorada en `.gitignore`) y está referenciada en `AGENTS.md`.

### AC43.2 — Cobertura separada por responsabilidad y alineación M1–M4
- **Dado** los principios innegociables y requisitos `M1`–`M4` + `TOOL-01..TOOL-09`,
- **Cuando** se inspeccionan las 5 skills,
- **Entonces**:
  - `academic-compliance` consulta la matriz M1–M4, aplica precedencia `M4 > M3 > M2 > M1` solo ante incompatibilidad, distingue `REQUISITO` / `MATERIAL` / `DECISIÓN` / `RESULTADO` y bloquea tecnologías prohibidas (Streamlit, `pip`, `requirements.txt`, notebooks).
  - `sdd-workflow` exige spec prospectiva previa (`spec.md`, `plan.md`, `tasks.md`), vinculación a Issue/PR/Given-When-Then, trazabilidad honesta y preservación de `specs/001..040/`.
  - `quality-and-make` usa `Makefile` como interfaz estándar, Python 3.13/`uv`/Ruff/`pytest`, distingue unitarias/integración/cobertura/regresión, verifica GNU Make real antes de invocarlo, evita re-ejecuciones innecesarias, documenta bloqueos y prohíbe comandos destructivos.
  - `github-gitlab-operations` diferencia GitHub (principal) y GitLab (M4 CI/CD/Registry), `gh`/`glab` vs MCPs, lectura vs escritura, exige autorización humana antes de `push`/PR/`merge` y limpieza segura de ramas.
  - `secure-cicd-deployment` cubre `lint → test → build → Registry → deploy`, Docker CPU, pesos reproducibles, tags trazables, VPS/firewall/HTTPS, secretos en variables CI protegidas, `GET /health`, prohibición de afirmar *zero-downtime* o desplegar sin autorización y preservación de la app M3.

### AC43.3 — Preservación de `GOV-03A` y recursos protegidos
- **Dado** los cambios previos de `GOV-03A` en `feature/gov-03a-agents-constitution-proposal`,
- **Cuando** se completa `GOV-04`,
- **Entonces** se preservan íntegros `docs/constitutional-amendment-m1-m4-proposal.md`, `specs/042-gov-03a-agents-constitution-proposal/`, `.specify/memory/constitution.md`, `Makefile`, `Dockerfile`, `.github/workflows/ci.yml`, `src/`, `api/`, `ui/`, `tests/` y `specs/001..041/`.
