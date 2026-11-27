# Feature Specification: Job Condicional deploy_vps vía SSH hacia Producción (SPEC-055)

**Feature Branch**: `docs/specs-m4-retrospective-052-065`
**Created**: 2026-11-26
**Status**: Retrospectiva (documenta trabajo ya integrado en PR #45 · Issue #51)
**Input**: Trazabilidad SDD retrospectiva sobre artefactos reales ya fusionados en `develop`.

> **Declaración de honestidad temporal:** Esta especificación es **retrospectiva**; documenta implementación ya verificada en PR #45 · Issue #51 sin atribuirse carácter de diseño previo.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Trazabilidad verificable de Job Condicional deploy_vps vía SSH hacia Producción (Priority: P1)

Como integrante del Grupo 2, quiero documentar de forma trazable en Spec Kit el alcance, criterios de aceptación y evidencia real de **Job Condicional deploy_vps vía SSH hacia Producción**, para mantener coherencia entre código, PRs e historial SDD.

**Independent Test**: Verificar la presencia e integridad de `.gitlab-ci.yml (etapa deploy)` en `develop` y la vigencia de PR #45 · Issue #51.

**Acceptance Scenarios**:

1. **Given** la integración previa de PR #45 · Issue #51 en `develop`, **When** se auditan los artefactos `.gitlab-ci.yml (etapa deploy)`, **Then** Despliega en la VPS por SSH solo cuando DEPLOY_HOST está definido como variable protegida, haciendo pull por SHA y levantando servicios sin caída.

## Requirements *(mandatory)*

- **FR-001**: Documentar con exactitud los artefactos `.gitlab-ci.yml (etapa deploy)` sin alterar código ni inventar evidencias.
- **FR-002**: Mantener vínculo explícito con PR #45 · Issue #51 y requisitos `M4-03, M4-06, M4-07`.

## Success Criteria *(mandatory)*

- **SC-001**: Especificación trazada y verificable frente al estado real de `develop`.

---

<!-- [M1-M4 GOVERNANCE EXTENSION] -->
## M1–M4 Academic Alignment & Protected Capabilities

> **Referencias normativas:** [AGENTS.md](../../AGENTS.md) · [Constitución](../../.specify/memory/constitution.md) · [Matriz Académica M1–M4](../../docs/academic-compliance-matrix.md)

- **ID Estable y Trazabilidad:** `SPEC-055` | **Vínculo:** PR #45 · Issue #51 | **Condición temporal:** **Retrospectiva**.
- **Requisitos académicos aplicables:** `M4-03, M4-06, M4-07`.
- **Tecnologías prohibidas:** Streamlit, `pip`, equirements.txt`, `.ipynb`.
- **Capacidades protegidas:** Contratos M1–M4 vigentes y honestidad temporal SDD.
<!-- [/M1-M4 GOVERNANCE EXTENSION] -->
