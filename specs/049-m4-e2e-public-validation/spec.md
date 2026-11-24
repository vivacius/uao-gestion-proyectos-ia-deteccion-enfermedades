# Feature Specification: Validación E2E, Despliegue Continuo y Demostración Pública HTTPS

**Feature Branch**: `feature/m4-plan-01-specs-048-050`

**Created**: 2026-11-23

**Status**: Draft (Prospectiva — elaborada antes de ejecutar el despliegue E2E)

**Input**: Issue `#51` (`[M4-E2E]`) — Validación integral de extremo a extremo del despliegue automático desde GitLab hacia la VPS, verificación pública por HTTPS y demostración funcional del sistema.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Despliegue continuo automático tras merge en `develop` (Priority: P1)

Como evaluador y equipo M4, quiero demostrar que un merge aprobado en `develop` en GitHub se sincroniza a GitLab, supera `quality → test → build` y ejecuta `deploy_vps` actualizando la VPS con la imagen etiquetada por `$CI_COMMIT_SHA`, para comprobar despliegue continuo real (15 % de la rúbrica).

**Why this priority**: La rúbrica M4 exige demostración automática y pública; sin evidencia de ejecución real, el estado queda únicamente como implementado localmente.

**Independent Test**: Consultar el job `deploy_vps` en GitLab (`89374502`) y verificar que el contenedor en ejecución en la VPS corresponde al `$CI_COMMIT_SHA` recién fusionado.

**Acceptance Scenarios**:

1. **Given** un push sincronizado a `develop` con variables protegidas de VPS/Registry configuradas, **When** concluye `build_docker`, **Then** `deploy_vps` actualiza los contenedores en la VPS y `GET https://<dominio>/health` responde HTTP `200`.

---

### User Story 2 - Validación pública HTTPS y aislamiento de red (Priority: P1)

Como usuario técnico y auditor de seguridad, quiero verificar públicamente por HTTPS los endpoints `/health`, `/model-info`, `/docs`, `/predict` y el frontend desacoplado, comprobando además que el puerto `8000` de la API y puertos no autorizados están bloqueados desde Internet, para garantizar operación segura en producción.

**Why this priority**: Valida simultáneamente funcionalidad M3 en producción y hardening de firewall/proxy (`M4-01`, `M4-02`, `M4-08`).

**Independent Test**: Ejecutar pruebas `curl` externas sobre `https://<dominio>/*`, `http://<dominio>` (redirección 301/308) y prueba negativa contra `http://<IP>:8000`.

**Acceptance Scenarios**:

1. **Given** la aplicación desplegada detrás de Nginx TLS en la VPS, **When** se consulta `https://<dominio>/health` y `/model-info`, **Then** devuelven HTTP `200` con certificado TLS válido.
2. **Given** una imagen foliar válida y un archivo inválido enviados a `POST https://<dominio>/predict`, **When** responde la API, **Then** la imagen válida retorna predicción con 38 clases/descargo agronómico y el archivo inválido retorna HTTP `400`.
3. **Given** el firewall activo en la VPS (`22/80/443`), **When** se intenta acceder directamente al puerto `8000` desde una red externa, **Then** la conexión es rechazada/filtrada.

### Edge Cases

- **Reversión ante fallo en producción:** Si una versión presenta regresión tras `deploy_vps`, debe poder revertirse apuntando `IMAGE_TAG` al SHA estable anterior sin reconstruir la imagen ni perder certificados TLS.

## Requirements *(mandatory)*

- **FR-001**: El flujo completo `GitHub merge → GitLab sync → quality → test → build → deploy_vps` DEBE completarse con evidencia trazable por SHA.
- **FR-002**: Todos los endpoints públicos (`GET /health`, `GET /model-info`, `GET /docs`, `POST /predict`) y la UI web estática DEBEN responder correctamente vía HTTPS (`443`) con redirección desde HTTP (`80`).
- **FR-003**: El acceso directo al puerto `8000` desde Internet DEBE permanecer bloqueado.

### Key Entities

- **Evidencia E2E (`docs/deployment-m4.md`):** Registro verificable de logs, respuestas HTTP, tags de Registry y pruebas de firewall/TLS sin exponer secretos.

## Success Criteria *(mandatory)*

- **SC-001**: `deploy_vps` en verde en GitLab (`89374502`) y actualización visible tras push autorizado antes del `28/11/2026`.
- **SC-002**: `GET https://<dominio>/health` HTTP `200`, `POST /predict` operativo con imagen real y HTTP `400` con archivo inválido, y puerto `8000` inaccesible externamente.

---

<!-- [M1-M4 GOVERNANCE EXTENSION] -->
## M1–M4 Academic Alignment & Protected Capabilities

> **Referencias normativas:** [AGENTS.md](../../AGENTS.md) · [Constitución](../../.specify/memory/constitution.md) · [Matriz Académica M1–M4](../../docs/academic-compliance-matrix.md)

- **ID Estable y Trazabilidad:** `SPEC-049` | **Issue:** `#51` (`@josesilvacalderon111`) | **Condición temporal:** **Prospectiva**.
- **Requisitos académicos aplicables:** `M4-07`, `M4-08`, `M4-10`.
- **Tecnologías prohibidas:** Streamlit, `pip`, `requirements.txt`, `.ipynb`.
- **Capacidades protegidas:** Modelo DINOv2 (`local_files_only=True`), 38 clases, $\tau=0.60$, descargo agronómico, FastAPI, UI HTTP desacoplada, Docker CPU non-root.
<!-- [/M1-M4 GOVERNANCE EXTENSION] -->
