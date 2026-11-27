# Feature Specification: Orquestación Docker Compose de Producción y Plantilla .env (SPEC-056)

**Feature Branch**: `docs/specs-m4-retrospective-052-065`
**Created**: 2026-11-26
**Status**: Retrospectiva (documenta trabajo ya integrado en PR #45 · Issue #49)
**Input**: Trazabilidad SDD retrospectiva sobre artefactos reales ya fusionados en `develop`.

> **Declaración de honestidad temporal:** Esta especificación es **retrospectiva**; documenta implementación ya verificada en PR #45 · Issue #49 sin atribuirse carácter de diseño previo.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Trazabilidad verificable de Orquestación Docker Compose de Producción y Plantilla .env (Priority: P1)

Como integrante del Grupo 2, quiero documentar de forma trazable en Spec Kit el alcance, criterios de aceptación y evidencia real de **Orquestación Docker Compose de Producción y Plantilla .env**, para mantener coherencia entre código, PRs e historial SDD.

**Independent Test**: Verificar la presencia e integridad de `deploy/docker-compose.prod.yml, deploy/.env.production.example` en `develop` y la vigencia de PR #45 · Issue #49.

**Acceptance Scenarios**:

1. **Given** la integración previa de PR #45 · Issue #49 en `develop`, **When** se auditan los artefactos `deploy/docker-compose.prod.yml, deploy/.env.production.example`, **Then** Define servicios api, web y certbot en red interna Docker manteniendo el puerto 8000 cerrado al host y documenta variables requeridas sin secretos reales.

## Requirements *(mandatory)*

- **FR-001**: Documentar con exactitud los artefactos `deploy/docker-compose.prod.yml, deploy/.env.production.example` sin alterar código ni inventar evidencias.
- **FR-002**: Mantener vínculo explícito con PR #45 · Issue #49 y requisitos `M4-01, M4-06`.

## Success Criteria *(mandatory)*

- **SC-001**: Especificación trazada y verificable frente al estado real de `develop`.

---

<!-- [M1-M4 GOVERNANCE EXTENSION] -->
## M1–M4 Academic Alignment & Protected Capabilities

> **Referencias normativas:** [AGENTS.md](../../AGENTS.md) · [Constitución](../../.specify/memory/constitution.md) · [Matriz Académica M1–M4](../../docs/academic-compliance-matrix.md)

- **ID Estable y Trazabilidad:** `SPEC-056` | **Vínculo:** PR #45 · Issue #49 | **Condición temporal:** **Retrospectiva**.
- **Requisitos académicos aplicables:** `M4-01, M4-06`.
- **Tecnologías prohibidas:** Streamlit, `pip`, equirements.txt`, `.ipynb`.
- **Capacidades protegidas:** Contratos M1–M4 vigentes y honestidad temporal SDD.
<!-- [/M1-M4 GOVERNANCE EXTENSION] -->
