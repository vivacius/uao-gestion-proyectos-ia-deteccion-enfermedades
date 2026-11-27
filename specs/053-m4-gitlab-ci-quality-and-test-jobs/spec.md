# Feature Specification: Jobs lint y run_test en Pipeline GitLab M4 (SPEC-053)

**Feature Branch**: `docs/specs-m4-retrospective-052-065`
**Created**: 2026-11-26
**Status**: Retrospectiva (documenta trabajo ya integrado en PR #44, PR #45 · Issue #48)
**Input**: Trazabilidad SDD retrospectiva sobre artefactos reales ya fusionados en `develop`.

> **Declaración de honestidad temporal:** Esta especificación es **retrospectiva**; documenta implementación ya verificada en PR #44, PR #45 · Issue #48 sin atribuirse carácter de diseño previo.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Trazabilidad verificable de Jobs lint y run_test en Pipeline GitLab M4 (Priority: P1)

Como integrante del Grupo 2, quiero documentar de forma trazable en Spec Kit el alcance, criterios de aceptación y evidencia real de **Jobs lint y run_test en Pipeline GitLab M4**, para mantener coherencia entre código, PRs e historial SDD.

**Independent Test**: Verificar la presencia e integridad de `.gitlab-ci.yml (etapas quality y test)` en `develop` y la vigencia de PR #44, PR #45 · Issue #48.

**Acceptance Scenarios**:

1. **Given** la integración previa de PR #44, PR #45 · Issue #48 en `develop`, **When** se auditan los artefactos `.gitlab-ci.yml (etapas quality y test)`, **Then** Ejecuta Ruff check/format y pytest unitario con --cov-fail-under=85 y reportes JUnit/cobertura como puerta bloqueante previa al build.

## Requirements *(mandatory)*

- **FR-001**: Documentar con exactitud los artefactos `.gitlab-ci.yml (etapas quality y test)` sin alterar código ni inventar evidencias.
- **FR-002**: Mantener vínculo explícito con PR #44, PR #45 · Issue #48 y requisitos `M1-03, M1-04, M4-04`.

## Success Criteria *(mandatory)*

- **SC-001**: Especificación trazada y verificable frente al estado real de `develop`.

---

<!-- [M1-M4 GOVERNANCE EXTENSION] -->
## M1–M4 Academic Alignment & Protected Capabilities

> **Referencias normativas:** [AGENTS.md](../../AGENTS.md) · [Constitución](../../.specify/memory/constitution.md) · [Matriz Académica M1–M4](../../docs/academic-compliance-matrix.md)

- **ID Estable y Trazabilidad:** `SPEC-053` | **Vínculo:** PR #44, PR #45 · Issue #48 | **Condición temporal:** **Retrospectiva**.
- **Requisitos académicos aplicables:** `M1-03, M1-04, M4-04`.
- **Tecnologías prohibidas:** Streamlit, `pip`, `requirements.txt`, `.ipynb`.
- **Capacidades protegidas:** Contratos M1–M4 vigentes y honestidad temporal SDD.
<!-- [/M1-M4 GOVERNANCE EXTENSION] -->
