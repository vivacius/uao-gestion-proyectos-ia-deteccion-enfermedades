# Feature Specification: CONSTITUTION.md en Raíz, Guion M4, Hardening .gitignore y E2E HTTPS (SPEC-065)

**Feature Branch**: `docs/specs-m4-retrospective-052-065`
**Created**: 2026-11-26
**Status**: Retrospectiva (documenta trabajo ya integrado en PR #59, PR #60 · Issue #51, #52)
**Input**: Trazabilidad SDD retrospectiva sobre artefactos reales ya fusionados en `develop`.

> **Declaración de honestidad temporal:** Esta especificación es **retrospectiva**; documenta implementación ya verificada en PR #59, PR #60 · Issue #51, #52 sin atribuirse carácter de diseño previo.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Trazabilidad verificable de CONSTITUTION.md en Raíz, Guion M4, Hardening .gitignore y E2E HTTPS (Priority: P1)

Como integrante del Grupo 2, quiero documentar de forma trazable en Spec Kit el alcance, criterios de aceptación y evidencia real de **CONSTITUTION.md en Raíz, Guion M4, Hardening .gitignore y E2E HTTPS**, para mantener coherencia entre código, PRs e historial SDD.

**Independent Test**: Verificar la presencia e integridad de `CONSTITUTION.md, README.md, docs/sustentacion-m4.md, docs/academic-compliance-matrix.md, .gitignore` en `develop` y la vigencia de PR #59, PR #60 · Issue #51, #52.

**Acceptance Scenarios**:

1. **Given** la integración previa de PR #59, PR #60 · Issue #51, #52 en `develop`, **When** se auditan los artefactos `CONSTITUTION.md, README.md, docs/sustentacion-m4.md, docs/academic-compliance-matrix.md, .gitignore`, **Then** Incorpora CONSTITUTION.md v2.0.0 en raíz enlazada desde README, alinea guion de sustentación 15 min, excluye .env en .gitignore y verifica HTTPS en vivo.

## Requirements *(mandatory)*

- **FR-001**: Documentar con exactitud los artefactos `CONSTITUTION.md, README.md, docs/sustentacion-m4.md, docs/academic-compliance-matrix.md, .gitignore` sin alterar código ni inventar evidencias.
- **FR-002**: Mantener vínculo explícito con PR #59, PR #60 · Issue #51, #52 y requisitos `M4-06, M4-08, M4-09, M4-11`.

## Success Criteria *(mandatory)*

- **SC-001**: Especificación trazada y verificable frente al estado real de `develop`.

---

<!-- [M1-M4 GOVERNANCE EXTENSION] -->
## M1–M4 Academic Alignment & Protected Capabilities

> **Referencias normativas:** [AGENTS.md](../../AGENTS.md) · [Constitución](../../.specify/memory/constitution.md) · [Matriz Académica M1–M4](../../docs/academic-compliance-matrix.md)

- **ID Estable y Trazabilidad:** `SPEC-065` | **Vínculo:** PR #59, PR #60 · Issue #51, #52 | **Condición temporal:** **Retrospectiva**.
- **Requisitos académicos aplicables:** `M4-06, M4-08, M4-09, M4-11`.
- **Tecnologías prohibidas:** Streamlit, `pip`, equirements.txt`, `.ipynb`.
- **Capacidades protegidas:** Contratos M1–M4 vigentes y honestidad temporal SDD.
<!-- [/M1-M4 GOVERNANCE EXTENSION] -->
