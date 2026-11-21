# Plan de Implementación (Spec Kit): SPEC-042 Operacionalización M1–M4 en `AGENTS.md` y Propuesta Constitucional

**Identificador:** `SPEC-042`  
**Feature Branch:** `feature/gov-03a-agents-constitution-proposal`  
**Spec Asociada:** [spec.md](./spec.md) | **Tasks:** [tasks.md](./tasks.md)  
**Fecha de Elaboración SDD (Prospectiva):** 2026-11-21

---

## Pasos de Implementación y Verificación

1. Confirmar estado limpio en `develop`, crear la rama `feature/gov-03a-agents-constitution-proposal` y redactar `SPEC-042` (`spec.md`, `plan.md`, `tasks.md`) antes de editar `AGENTS.md`.
2. Analizar `AGENTS.md` y `.specify/memory/constitution.md` identificando reglas compatibles a preservar, obsolescencias (`D-02`, `D-09`, menciones a GGA inexistente o HU-08 diferida) y reglas M1–M4 a operacionalizar.
3. Actualizar `AGENTS.md` de forma concisa y estructurada sin duplicar las tablas extensas de `docs/academic-compliance-matrix.md`.
4. Redactar `docs/constitutional-amendment-m1-m4-proposal.md` con las enmiendas propuestas (académicas, excepciones/contratos `D-05`, frontend desacoplado sin Streamlit `D-04`, HU-08 base vs M4 `D-02`, rango Python `D-03`, herramientas GitHub/GitLab/Makefile y matriz SSOT `M4-09`), dejando constancia de que requiere aprobación unánime.
5. Registrar explícitamente en `SPEC-042` (`tasks.md`) y en el informe qué reglas se delegarán posteriormente a skills y Spec Kit.
6. Verificar con `git diff`, `git status` y comprobación rápida de Markdown/enlaces/secretos que `.specify/memory/constitution.md`, código funcional, Docker, CI, MLflow y specs históricas permanecen intactos.
