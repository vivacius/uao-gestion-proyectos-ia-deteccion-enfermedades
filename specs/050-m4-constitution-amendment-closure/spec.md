# Feature Specification: Enmienda Constitucional M4, Cierre Kanban y Sustentación

**Feature Branch**: `feature/m4-plan-01-specs-048-050`

**Created**: 2026-11-23

**Status**: Draft (Prospectiva — elaborada antes de enmendar la Constitución)

**Input**: Issue `#52` (`[M4-GOV]`) — Enmienda Constitucional M4 (`M4-09`), actualización final de `docs/academic-compliance-matrix.md`, cierre de métricas Kanban y paquete de sustentación antes del `28/11/2026`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Enmienda Constitucional M4 por consenso unánime (Priority: P1)

Como Grupo 2, queremos redactar y aprobar por consenso unánime de los 4 integrantes la Enmienda M4 en `.specify/memory/constitution.md` incorporando las reglas de CI/CD GitLab, Container Registry, VPS/HTTPS y seguridad de secretos, para cumplir `M4-09` sin bloquear el trabajo documental por la espera del despliegue.

**Why this priority**: La redacción y votación constitucional pueden avanzar en paralelo desde el inicio sin depender de la VPS; requiere consenso unánime de los 4 integrantes.

**Independent Test**: Verificar en `.specify/memory/constitution.md` el registro de enmienda firmado/aprobado por los 4 integrantes en la PR correspondiente.

**Acceptance Scenarios**:

1. **Given** el borrador de enmienda M4 en `.specify/memory/constitution.md`, **When** los 4 integrantes revisan y aprueban la PR, **Then** la Constitución refleja la versión enmendada con reglas M4 y consenso unánime documentado.

---

### User Story 2 - Actualización de matriz académica, Kanban y sustentación (Priority: P1)

Como coordinador QA/documentación, quiero actualizar `docs/academic-compliance-matrix.md` con las evidencias reales de M4, cerrar el tablero GitHub Project #1 con métricas Kanban (WIP, throughput, cycle time, work item age) y preparar la guía de sustentación, para demostrar trazabilidad integral el `28/11/2026`.

**Why this priority**: Cierra la trazabilidad documental exigida en M1–M4 y evita afirmaciones no verificadas.

**Independent Test**: Auditar `docs/academic-compliance-matrix.md` comprobando que cada ítem `VERIFICADO` enlaza evidencia real ejecutada y revisar el estado final de Project #1.

**Acceptance Scenarios**:

1. **Given** las evidencias reales de `#46`, `#48`–`#51`, **When** se actualiza `docs/academic-compliance-matrix.md`, **Then** cada requisito `M4-01..M4-12` y `TOOL-01..TOOL-09` refleja su estado real (`VERIFICADO` / `PENDIENTE`) con enlaces exactos.

### Edge Cases

- **Desacople temporal:** Si la votación de la enmienda constitucional concluye antes que el despliegue E2E (`#51`), la PR de enmienda puede fusionarse independientemente; la actualización final de estados `VERIFICADO` en la matriz académica espera la evidencia de `#51`.

## Requirements *(mandatory)*

- **FR-001**: La modificación a `.specify/memory/constitution.md` DEBE contar con aprobación explícita de los 4 integrantes del Grupo 2.
- **FR-002**: `docs/academic-compliance-matrix.md` DEBE distinguir estrictamente entre `VERIFICADO`, `PARCIAL` y `PENDIENTE` según evidencia observada.
- **FR-003**: El cierre de Project #1 DEBE registrar métricas WIP, throughput, work item age y cycle time y mantener solo ítems realmente verificados en `Done`.

### Key Entities

- **Constitución (`.specify/memory/constitution.md`):** Documento supremo del repositorio (`v1.0.0` -> enmienda M4).
- **Matriz Académica (`docs/academic-compliance-matrix.md`):** Fuente única de verdad de cumplimiento M1–M4.

## Success Criteria *(mandatory)*

- **SC-001**: Enmienda M4 aprobada por los 4 integrantes antes del `28/11/2026`.
- **SC-002**: 100 % de los requisitos M4 con evidencia trazable en `docs/academic-compliance-matrix.md` y tablero Kanban cerrado.

---

<!-- [M1-M4 GOVERNANCE EXTENSION] -->
## M1–M4 Academic Alignment & Protected Capabilities

> **Referencias normativas:** [AGENTS.md](../../AGENTS.md) · [Constitución](../../.specify/memory/constitution.md) · [Matriz Académica M1–M4](../../docs/academic-compliance-matrix.md)

- **ID Estable y Trazabilidad:** `SPEC-050` | **Issue:** `#52` (`@vivacius`) | **Condición temporal:** **Prospectiva**.
- **Requisitos académicos aplicables:** `M4-09`, `M4-10`, `TOOL-01`, `TOOL-08`.
- **Tecnologías prohibidas:** Streamlit, `pip`, `requirements.txt`, `.ipynb`.
- **Capacidades protegidas:** Consenso unánime para enmiendas constitucionales, plantilla de PR intacta, `specs/001..040/`.
<!-- [/M1-M4 GOVERNANCE EXTENSION] -->
