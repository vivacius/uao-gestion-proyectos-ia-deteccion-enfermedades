# Feature Specification: Política de Despliegue Exclusivo desde `main` (SPEC-066)

**Feature Branch**: `fix/m4-release-main-only`
**Created**: 2026-11-27
**Status**: Prospectiva (en implementación previa a PR hacia `develop`)
**Input**: Unidad `M4-E2.1-RELEASE-MAIN-ONLY` — diseño aprobado en `M4-E1-RELEASE-POLICY-DESIGN`.

> **Declaración de honestidad temporal:** Esta especificación es **prospectiva**; se redacta antes de modificar `.gitlab-ci.yml`, pruebas contractuales y documentación operativa.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Integración continua en `develop` sin alterar producción (Priority: P1)

Como equipo de desarrollo del Grupo 2, queremos que `develop` ejecute `quality`, `test` y `build` (empaquetado Wheel y construcción/publicación de imagen Docker por `CI_COMMIT_SHA`), sin desplegar a la VPS ni sobrescribir la etiqueta `:latest`, para evitar que cambios en integración modifiquen el servicio público sin promoción aprobada a `main`.

**Independent Test**: Inspección contractual de `.gitlab-ci.yml` mediante `pytest` y `glab ci lint`, más validación posterior en pipeline real de `develop` tras merge de la PR.

**Acceptance Scenarios**:

1. **Given** un push o merge en `develop`, **When** se evalúa `.gitlab-ci.yml`, **Then** se ejecutan `lint`, `run_test`, `package_wheel` y `build_docker` (publicando `:$CI_COMMIT_SHA`), **And** el job `deploy_vps` no se crea y `:latest` no se actualiza.

### User Story 2 - Despliegue automático exclusivo desde `main` (Priority: P1)

Como responsable de liberación, quiero que `main` (`$CI_DEFAULT_BRANCH`) sea la única rama que actualice `:latest` y ejecute `deploy_vps` automáticamente (`when: on_success`) tras una PR revisada y aprobada, conservando `IMAGE_TAG=${CI_COMMIT_SHA}`, `resource_group: production`, `needs` y secretos protegidos.

**Independent Test**: Prueba contractual unitaria en `tests/unit/test_client_scripts_and_m4_contracts.py` y validación posterior en pipeline real de `main` tras promoción autorizada.

**Acceptance Scenarios**:

1. **Given** una PR aprobada e integrada en `main`, **When** el espejo actualiza `main` en GitLab y `build_docker` finaliza con éxito, **Then** se publican `:$CI_COMMIT_SHA` y `:latest` en el Registry y `deploy_vps` se ejecuta automáticamente sin intervención manual usando `IMAGE_TAG=${CI_COMMIT_SHA}`.
2. **Given** una necesidad de reversión en la VPS, **When** se sigue el procedimiento documentado en `docs/deployment-m4.md`, **Then** `.env` persiste el `IMAGE_TAG` del SHA anterior verificado sin eliminar `certbot/conf` ni `certbot/www`.

## Requirements *(mandatory)*

- **FR-001**: `develop` conserva `quality`, `test` y `build` (publicando `:$CI_COMMIT_SHA`) y no crea `deploy_vps` ni actualiza `:latest`.
- **FR-002**: `$CI_DEFAULT_BRANCH` (`main`) publica `:$CI_COMMIT_SHA` y `:latest`, y ejecuta `deploy_vps` con `when: on_success` conservando `resource_group: production`, `needs: [build_docker]`, `environment: production` y variables protegidas.
- **FR-003**: Añadir prueba contractual unitaria en `tests/unit/test_client_scripts_and_m4_contracts.py` que prevenga regresiones sobre `deploy_vps` y `:latest`.
- **FR-004**: Actualizar `docs/deployment-m4.md` (política `main`-only y persistencia de `.env` en rollback) y `docs/sustentacion-m4.md` (demo vía PR `develop → main`, sin afirmar *zero-downtime*).

## Success Criteria *(mandatory)*

- **SC-001**: `uv run ruff check .`, `uv run ruff format --check .`, `uv run pytest tests/unit -q` y `glab ci lint .gitlab-ci.yml` finalizan con código `0`.
- **SC-002**: PR abierta hacia `develop` con plantilla oficial y checks de GitHub en verde, sin merge ni despliegue ejecutados.

---

<!-- [M1-M4 GOVERNANCE EXTENSION] -->
## M1–M4 Academic Alignment & Protected Capabilities

> **Referencias normativas:** [AGENTS.md](../../AGENTS.md) · [Constitución](../../.specify/memory/constitution.md) · [Matriz Académica M1–M4](../../docs/academic-compliance-matrix.md)

- **ID Estable y Trazabilidad:** `SPEC-066` | **Vínculo:** Unidad `M4-E2.1-RELEASE-MAIN-ONLY` | **Condición temporal:** **Prospectiva**.
- **Requisitos académicos aplicables:** `M4-03`, `M4-05`, `M4-06`, `M4-07`, `TOOL-03`, `TOOL-05`.
- **Tecnologías prohibidas:** Streamlit, `pip`, `requirements.txt`, `.ipynb`.
- **Capacidades protegidas:** Contratos M1–M3 (`src/`, `api/`, `ui/`, `Dockerfile`, `deploy/docker-compose.prod.yml`), secretos protegidos en GitLab y flujo de revisión humana en GitHub.
<!-- [/M1-M4 GOVERNANCE EXTENSION] -->
