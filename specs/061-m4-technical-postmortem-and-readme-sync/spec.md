# Feature Specification: Post-Mortem Técnico M1–M4 y Actualización de Flujo en README (SPEC-061)

**Feature Branch**: `docs/specs-m4-retrospective-052-065`
**Created**: 2026-11-26
**Status**: Retrospectiva (documenta trabajo ya integrado en PR #55 · Issue #52)
**Input**: Trazabilidad SDD retrospectiva sobre artefactos reales ya fusionados en `develop`.

> **Declaración de honestidad temporal:** Esta especificación es **retrospectiva**; documenta implementación ya verificada en PR #55 · Issue #52 sin atribuirse carácter de diseño previo.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Trazabilidad verificable de Post-Mortem Técnico M1–M4 y Actualización de Flujo en README (Priority: P1)

Como integrante del Grupo 2, quiero documentar de forma trazable en Spec Kit el alcance, criterios de aceptación y evidencia real de **Post-Mortem Técnico M1–M4 y Actualización de Flujo en README**, para mantener coherencia entre código, PRs e historial SDD.

**Independent Test**: Verificar la presencia e integridad de `docs/post-mortem-m1-m4.md, README.md` en `develop` y la vigencia de PR #55 · Issue #52.

**Acceptance Scenarios**:

1. **Given** la integración previa de PR #55 · Issue #52 en `develop`, **When** se auditan los artefactos `docs/post-mortem-m1-m4.md, README.md`, **Then** Registra 5 incidentes reales (INC-01 a INC-05) con causa raíz y lecciones aprendidas, y actualiza README.md:85 reflejando la UI web ya montada en /.

## Requirements *(mandatory)*

- **FR-001**: Documentar con exactitud los artefactos `docs/post-mortem-m1-m4.md, README.md` sin alterar código ni inventar evidencias.
- **FR-002**: Mantener vínculo explícito con PR #55 · Issue #52 y requisitos `M1-06, M3-08`.

## Success Criteria *(mandatory)*

- **SC-001**: Especificación trazada y verificable frente al estado real de `develop`.

---

<!-- [M1-M4 GOVERNANCE EXTENSION] -->
## M1–M4 Academic Alignment & Protected Capabilities

> **Referencias normativas:** [AGENTS.md](../../AGENTS.md) · [Constitución](../../.specify/memory/constitution.md) · [Matriz Académica M1–M4](../../docs/academic-compliance-matrix.md)

- **ID Estable y Trazabilidad:** `SPEC-061` | **Vínculo:** PR #55 · Issue #52 | **Condición temporal:** **Retrospectiva**.
- **Requisitos académicos aplicables:** `M1-06, M3-08`.
- **Tecnologías prohibidas:** Streamlit, `pip`, `requirements.txt`, `.ipynb`.
- **Capacidades protegidas:** Contratos M1–M4 vigentes y honestidad temporal SDD.
<!-- [/M1-M4 GOVERNANCE EXTENSION] -->
