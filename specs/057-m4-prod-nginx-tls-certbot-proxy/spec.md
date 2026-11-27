# Feature Specification: Proxy Inverso Nginx con TLS/HTTPS y Renovación Certbot (SPEC-057)

**Feature Branch**: `docs/specs-m4-retrospective-052-065`
**Created**: 2026-11-26
**Status**: Retrospectiva (documenta trabajo ya integrado en PR #45 · Issue #49)
**Input**: Trazabilidad SDD retrospectiva sobre artefactos reales ya fusionados en `develop`.

> **Declaración de honestidad temporal:** Esta especificación es **retrospectiva**; documenta implementación ya verificada en PR #45 · Issue #49 sin atribuirse carácter de diseño previo.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Trazabilidad verificable de Proxy Inverso Nginx con TLS/HTTPS y Renovación Certbot (Priority: P1)

Como integrante del Grupo 2, quiero documentar de forma trazable en Spec Kit el alcance, criterios de aceptación y evidencia real de **Proxy Inverso Nginx con TLS/HTTPS y Renovación Certbot**, para mantener coherencia entre código, PRs e historial SDD.

**Independent Test**: Verificar la presencia e integridad de `deploy/nginx.prod.conf.template` en `develop` y la vigencia de PR #45 · Issue #49.

**Acceptance Scenarios**:

1. **Given** la integración previa de PR #45 · Issue #49 en `develop`, **When** se auditan los artefactos `deploy/nginx.prod.conf.template`, **Then** Enruta tráfico HTTPS (443) hacia el frontend estático y FastAPI con proxy same-origin, redirección HTTP->HTTPS y desafío ACME de Certbot.

## Requirements *(mandatory)*

- **FR-001**: Documentar con exactitud los artefactos `deploy/nginx.prod.conf.template` sin alterar código ni inventar evidencias.
- **FR-002**: Mantener vínculo explícito con PR #45 · Issue #49 y requisitos `M4-02, M4-08`.

## Success Criteria *(mandatory)*

- **SC-001**: Especificación trazada y verificable frente al estado real de `develop`.

---

<!-- [M1-M4 GOVERNANCE EXTENSION] -->
## M1–M4 Academic Alignment & Protected Capabilities

> **Referencias normativas:** [AGENTS.md](../../AGENTS.md) · [Constitución](../../.specify/memory/constitution.md) · [Matriz Académica M1–M4](../../docs/academic-compliance-matrix.md)

- **ID Estable y Trazabilidad:** `SPEC-057` | **Vínculo:** PR #45 · Issue #49 | **Condición temporal:** **Retrospectiva**.
- **Requisitos académicos aplicables:** `M4-02, M4-08`.
- **Tecnologías prohibidas:** Streamlit, `pip`, equirements.txt`, `.ipynb`.
- **Capacidades protegidas:** Contratos M1–M4 vigentes y honestidad temporal SDD.
<!-- [/M1-M4 GOVERNANCE EXTENSION] -->
