# Feature Specification: Pruebas Unitarias Exhaustivas de 38 Clases y Postprocesamiento (SPEC-062)

**Feature Branch**: `docs/specs-m4-retrospective-052-065`
**Created**: 2026-11-26
**Status**: Retrospectiva (documenta trabajo ya integrado en PR #58 · SPEC-051)
**Input**: Trazabilidad SDD retrospectiva sobre artefactos reales ya fusionados en `develop`.

> **Declaración de honestidad temporal:** Esta especificación es **retrospectiva**; documenta implementación ya verificada en PR #58 · SPEC-051 sin atribuirse carácter de diseño previo.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Trazabilidad verificable de Pruebas Unitarias Exhaustivas de 38 Clases y Postprocesamiento (Priority: P1)

Como integrante del Grupo 2, quiero documentar de forma trazable en Spec Kit el alcance, criterios de aceptación y evidencia real de **Pruebas Unitarias Exhaustivas de 38 Clases y Postprocesamiento**, para mantener coherencia entre código, PRs e historial SDD.

**Independent Test**: Verificar la presencia e integridad de `tests/unit/test_taxonomy_and_postprocessing_exhaustive.py` en `develop` y la vigencia de PR #58 · SPEC-051.

**Acceptance Scenarios**:

1. **Given** la integración previa de PR #58 · SPEC-051 en `develop`, **When** se auditan los artefactos `tests/unit/test_taxonomy_and_postprocessing_exhaustive.py`, **Then** Valida mediante parametrización AAA las 38 etiquetas reales de config.json, traducción al español, clean_identifier y process_logits (1D/2D/3D y top_k).

## Requirements *(mandatory)*

- **FR-001**: Documentar con exactitud los artefactos `tests/unit/test_taxonomy_and_postprocessing_exhaustive.py` sin alterar código ni inventar evidencias.
- **FR-002**: Mantener vínculo explícito con PR #58 · SPEC-051 y requisitos `M1-03, M3-01`.

## Success Criteria *(mandatory)*

- **SC-001**: Especificación trazada y verificable frente al estado real de `develop`.

---

<!-- [M1-M4 GOVERNANCE EXTENSION] -->
## M1–M4 Academic Alignment & Protected Capabilities

> **Referencias normativas:** [AGENTS.md](../../AGENTS.md) · [Constitución](../../.specify/memory/constitution.md) · [Matriz Académica M1–M4](../../docs/academic-compliance-matrix.md)

- **ID Estable y Trazabilidad:** `SPEC-062` | **Vínculo:** PR #58 · SPEC-051 | **Condición temporal:** **Retrospectiva**.
- **Requisitos académicos aplicables:** `M1-03, M3-01`.
- **Tecnologías prohibidas:** Streamlit, `pip`, equirements.txt`, `.ipynb`.
- **Capacidades protegidas:** Contratos M1–M4 vigentes y honestidad temporal SDD.
<!-- [/M1-M4 GOVERNANCE EXTENSION] -->
