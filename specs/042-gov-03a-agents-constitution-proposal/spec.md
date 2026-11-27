# Especificación Técnica (Spec Kit): SPEC-042 Operacionalización de Reglas M1–M4 en `AGENTS.md` y Propuesta de Enmienda Constitucional

**Identificador:** `SPEC-042`  
**Feature Branch:** `feature/gov-03a-agents-constitution-proposal`  
**Unidad / Historia Asociada:** `GOV-03A` (Gobernanza M1–M4 / `M4-09`)  
**Fecha de Elaboración SDD (Prospectiva):** 2026-11-21  
**Trazabilidad Temporal:** **Especificación prospectiva elaborada ANTES de actualizar `AGENTS.md` y redactar la propuesta constitucional.**  
**Estado:** En progreso (`GOV-03A`)  
**Artefactos Relacionados:** [plan.md](./plan.md) · [tasks.md](./tasks.md) · [Matriz Académica](../../docs/academic-compliance-matrix.md)

---

## 1. Propósito y Alcance
Hacer operativas dentro de `AGENTS.md` las restricciones académicas, técnicas, de conservación, de procedimiento y de herramientas acumuladas de `M1`–`M4`, estableciendo la jerarquía normativa vigente y corrigiendo afirmaciones obsoletas (`D-02`, `D-09`), sin modificar `.specify/memory/constitution.md` ni implementar infraestructura `M4`. Preparar en un documento separado una propuesta formal de enmienda constitucional para revisión y aprobación unánime del equipo.

---

## 2. Escenarios de Aceptación (Gherkin)

### AC42.1 — Jerarquía normativa y reglas M1–M4 en `AGENTS.md`
- **Dado** el archivo `AGENTS.md` en la raíz del repositorio,
- **Cuando** se actualiza bajo `GOV-03A`,
- **Entonces** declara explícitamente la jerarquía de autoridad (1. Usuario/restricciones oficiales → 2. Reglas académicas vigentes `M4 > M3 > M2 > M1` únicamente ante incompatibilidad → 3. Constitución aprobada → 4. `AGENTS.md` → 5. Matriz académica y specs → 6. Skills/procedimientos), las reglas académicas, de conservación, procedimiento y herramientas, y enlaza a `docs/academic-compliance-matrix.md`, `.specify/memory/constitution.md`, `Makefile` y `specs/`.

### AC42.2 — Eliminación de obsolescencias y precisión de estado vigente
- **Dado** el estado real del repositorio en `develop`,
- **Cuando** se revisa `AGENTS.md`,
- **Entonces** refleja que el empaquetado Wheel y Docker CPU base (`HU-08` base) ya están implementados en M3 (reservando hardening CI/CD, Registry, VPS y TLS para M4), elimina la afirmación de un hook GGA pre-commit activo si no existe en `.git/hooks/`, reconoce el frontend desacoplado (Tkinter + Web HTML/CSS/JS) con prohibición expresa de Streamlit y declara el carácter retrospectivo de `specs/010..040/`.

### AC42.3 — Propuesta de enmienda constitucional separada e integridad de la Constitución vigente
- **Dado** que `.specify/memory/constitution.md` exige consenso unánime de los 4 integrantes para enmendarse,
- **Cuando** se completa `GOV-03A`,
- **Entonces** `.specify/memory/constitution.md` permanece intacta bit a bit y existe un documento separado (`docs/constitutional-amendment-m1-m4-proposal.md`) que identifica texto actual afectado, redacción propuesta, justificación, requisitos académicos relacionados, impactos y requerimiento de aprobación unánime.

### AC42.4 — Registro de pendientes para Skills y Spec Kit sin ampliar alcance
- **Dado** el alcance estricto de `GOV-03A`,
- **Cuando** se entregan los artefactos,
- **Entonces** se documentan qué procedimientos pasarán posteriormente a skills o nuevas specs (sin implementarlos aún) y permanecen intactos `src/`, `api/`, `ui/`, `tests/`, `Dockerfile`, `docker-compose.yml`, `.github/workflows/ci.yml`, `mlflow_tracking.db`, `specs/001..041/` y `.specify/memory/constitution.md`.
