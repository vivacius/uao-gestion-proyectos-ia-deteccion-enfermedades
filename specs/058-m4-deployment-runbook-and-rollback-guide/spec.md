# Feature Specification: Manual Operativo de Despliegue VPS, TLS y Reversión (SPEC-058)

**Feature Branch**: `docs/specs-m4-retrospective-052-065`
**Created**: 2026-11-26
**Status**: Retrospectiva (documenta trabajo ya integrado en PR #45, PR #60 · Issue #49, #51)
**Input**: Trazabilidad SDD retrospectiva sobre artefactos reales ya fusionados en `develop`.

> **Declaración de honestidad temporal:** Esta especificación es **retrospectiva**; documenta implementación ya verificada en PR #45, PR #60 · Issue #49, #51 sin atribuirse carácter de diseño previo.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Trazabilidad verificable de Manual Operativo de Despliegue VPS, TLS y Reversión (Priority: P1)

Como integrante del Grupo 2, quiero documentar de forma trazable en Spec Kit el alcance, criterios de aceptación y evidencia real de **Manual Operativo de Despliegue VPS, TLS y Reversión**, para mantener coherencia entre código, PRs e historial SDD.

**Independent Test**: Verificar la presencia e integridad de `docs/deployment-m4.md` en `develop` y la vigencia de PR #45, PR #60 · Issue #49, #51.

**Acceptance Scenarios**:

1. **Given** la integración previa de PR #45, PR #60 · Issue #49, #51 en `develop`, **When** se auditan los artefactos `docs/deployment-m4.md`, **Then** Documenta aprovisionamiento Ubuntu, firewall UFW (22/80/443), emisión Certbot, verificación E2E y procedimiento de rollback por IMAGE_TAG SHA.

## Requirements *(mandatory)*

- **FR-001**: Documentar con exactitud los artefactos `docs/deployment-m4.md` sin alterar código ni inventar evidencias.
- **FR-002**: Mantener vínculo explícito con PR #45, PR #60 · Issue #49, #51 y requisitos `M4-01, M4-02, M4-07`.

## Success Criteria *(mandatory)*

- **SC-001**: Especificación trazada y verificable frente al estado real de `develop`.

---

<!-- [M1-M4 GOVERNANCE EXTENSION] -->
## M1–M4 Academic Alignment & Protected Capabilities

> **Referencias normativas:** [AGENTS.md](../../AGENTS.md) · [Constitución](../../.specify/memory/constitution.md) · [Matriz Académica M1–M4](../../docs/academic-compliance-matrix.md)

- **ID Estable y Trazabilidad:** `SPEC-058` | **Vínculo:** PR #45, PR #60 · Issue #49, #51 | **Condición temporal:** **Retrospectiva**.
- **Requisitos académicos aplicables:** `M4-01, M4-02, M4-07`.
- **Tecnologías prohibidas:** Streamlit, `pip`, equirements.txt`, `.ipynb`.
- **Capacidades protegidas:** Contratos M1–M4 vigentes y honestidad temporal SDD.
<!-- [/M1-M4 GOVERNANCE EXTENSION] -->
