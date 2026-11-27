# Feature Specification: Protección de Ramas main/develop y Quality Gate en PR a main (SPEC-059)

**Feature Branch**: `docs/specs-m4-retrospective-052-065`
**Created**: 2026-11-26
**Status**: Retrospectiva (documenta trabajo ya integrado en PR #57 · Issue #52)
**Input**: Trazabilidad SDD retrospectiva sobre artefactos reales ya fusionados en `develop`.

> **Declaración de honestidad temporal:** Esta especificación es **retrospectiva**; documenta implementación ya verificada en PR #57 · Issue #52 sin atribuirse carácter de diseño previo.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Trazabilidad verificable de Protección de Ramas main/develop y Quality Gate en PR a main (Priority: P1)

Como integrante del Grupo 2, quiero documentar de forma trazable en Spec Kit el alcance, criterios de aceptación y evidencia real de **Protección de Ramas main/develop y Quality Gate en PR a main**, para mantener coherencia entre código, PRs e historial SDD.

**Independent Test**: Verificar la presencia e integridad de `.github/workflows/ci.yml y reglas de protección GitHub` en `develop` y la vigencia de PR #57 · Issue #52.

**Acceptance Scenarios**:

1. **Given** la integración previa de PR #57 · Issue #52 en `develop`, **When** se auditan los artefactos `.github/workflows/ci.yml y reglas de protección GitHub`, **Then** Activa Quality Gate CI en PR hacia main y configura protección estricta en main y develop (PR, 1 aprobación, CI verde, sin force push ni borrado).

## Requirements *(mandatory)*

- **FR-001**: Documentar con exactitud los artefactos `.github/workflows/ci.yml y reglas de protección GitHub` sin alterar código ni inventar evidencias.
- **FR-002**: Mantener vínculo explícito con PR #57 · Issue #52 y requisitos `M1-07, TOOL-01, TOOL-06`.

## Success Criteria *(mandatory)*

- **SC-001**: Especificación trazada y verificable frente al estado real de `develop`.

---

<!-- [M1-M4 GOVERNANCE EXTENSION] -->
## M1–M4 Academic Alignment & Protected Capabilities

> **Referencias normativas:** [AGENTS.md](../../AGENTS.md) · [Constitución](../../.specify/memory/constitution.md) · [Matriz Académica M1–M4](../../docs/academic-compliance-matrix.md)

- **ID Estable y Trazabilidad:** `SPEC-059` | **Vínculo:** PR #57 · Issue #52 | **Condición temporal:** **Retrospectiva**.
- **Requisitos académicos aplicables:** `M1-07, TOOL-01, TOOL-06`.
- **Tecnologías prohibidas:** Streamlit, `pip`, `requirements.txt`, `.ipynb`.
- **Capacidades protegidas:** Contratos M1–M4 vigentes y honestidad temporal SDD.
<!-- [/M1-M4 GOVERNANCE EXTENSION] -->
