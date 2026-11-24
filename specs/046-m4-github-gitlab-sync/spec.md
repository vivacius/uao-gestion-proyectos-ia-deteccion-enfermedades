# Feature Specification: Sincronización Unidireccional GitHub → GitLab (M4)

**Feature Branch**: `feature/m4-spec-046-github-gitlab-sync` *(propuesta; no creada aún en Git)*

**Created**: 2026-11-23

**Status**: Draft (Prospectiva — elaborada antes de implementar)

**Input**: Unidad `M4-046-E1` / `M4-046-E2` — Propuesta prospectiva del mecanismo mínimo, seguro y reproducible para sincronizar automáticamente el repositorio principal de GitHub (`vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades`) con el proyecto GitLab oficial (`vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades`, Project ID `89374502`), preservando GitHub como fuente única de verdad.

> **Alcance y carácter provisional:** Esta especificación describe una **propuesta de diseño**, no una implementación activa. El mecanismo mediante GitHub Actions es **provisional** hasta confirmar el trabajo y alcance de los compañeros en el GitLab oficial (`origin/feature/m4-gitlab-registry-deploy` y pipelines en curso), evitando duplicar cualquier integración ya implementada. La creación de tokens, protecciones de ramas y workflows requiere autorización humana posterior.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Sincronización automática tras merge en GitHub (Priority: P1)

Como integrante del Grupo 2, quiero que cada merge aprobado hacia `develop` o `main` en GitHub se replique automáticamente en el proyecto GitLab oficial (`id=89374502`) con el mismo SHA de commit y objetos Git LFS, para que GitLab ejecute el pipeline CI/CD y publique artefactos sin intervención manual ni historias divergentes.

**Why this priority**: Sin sincronización controlada `GitHub → GitLab`, el proyecto GitLab oficial permanece estático tras la importación inicial y no ejecuta pipelines M4 ni publica imágenes en el Container Registry (`TOOL-03`, `TOOL-05`, `M4-03`).

**Independent Test**: Fusionar una PR aprobada en `develop` en GitHub y verificar que el workflow de sincronización concluye en verde, que `develop` en GitLab (`id=89374502`) apunta exactamente al mismo SHA que `origin/develop` en GitHub, y que `model.safetensors` está íntegro vía Git LFS.

**Acceptance Scenarios**:

1. **Given** una PR aprobada y fusionada en `develop` (o `main`) en GitHub, **When** se dispara el workflow de sincronización por evento `push`, **Then** el workflow sincroniza únicamente esa rama hacia GitLab (`id=89374502`) sin `--force` y verifica que el SHA remoto en GitLab coincide exactamente con `github.sha`.
2. **Given** un repositorio con objetos pesados gestionados por Git LFS (`model.safetensors`), **When** el workflow sincroniza `develop` o `main` hacia GitLab, **Then** los objetos LFS requeridos se transfieren antes del push de la rama y el checkout/build en GitLab dispone del modelo íntegro.
3. **Given** una ejecución manual (`workflow_dispatch`) solicitada para recuperación controlada, **When** se ejecuta sobre `develop` o `main`, **Then** realiza la misma sincronización fast-forward y verificación de SHA sin afectar otras ramas.

---

### User Story 2 - Seguridad de credenciales y protección de ramas (Priority: P1)

Como responsable DevOps/Seguridad, quiero que la sincronización utilice una credencial de GitLab con privilegios mínimos, almacenada exclusivamente en GitHub Secrets y compatible con ramas protegidas en GitLab, para evitar exposición de secretos y bloqueos o sobrescrituras destructivas.

**Why this priority**: El manejo inseguro de tokens o el uso de `push --force` violaría la Constitución (§ IV, § V), `AGENTS.md` (§ 3, § 4) y `TOOL-06`/`TOOL-07`.

**Independent Test**: Inspeccionar el YAML del workflow (sin tokens embebidos ni impresión en logs), verificar que `develop` y `main` en GitLab tienen `force push` deshabilitado y comprobar que el Project Access Token permite el push fast-forward de sincronización.

**Acceptance Scenarios**:

1. **Given** un Project Access Token (PrAT) de GitLab acotado al proyecto `89374502` con alcance mínimo `write_repository` y expiración definida, **When** se almacena como secreto en GitHub (`GITLAB_SYNC_TOKEN`), **Then** ningún archivo del repositorio ni salida de logs expone el valor del token.
2. **Given** las ramas `main` y `develop` protegidas en GitLab con `allow_force_push = false`, **When** el workflow realiza push fast-forward con la identidad del PrAT, **Then** GitLab acepta el push sin requerir permisos globales de usuario ni desactivar la protección de ramas.

---

### User Story 3 - Validación inicial del pipeline GitLab y Container Registry (Priority: P2)

Como equipo M4, quiero verificar mediante `glab` CLI (y GitLab MCP cuando esté configurado) que la primera sincronización dispara el pipeline de `.gitlab-ci.yml` en `develop` y publica la imagen en el Container Registry oficial, para confirmar operatividad end-to-end de CI/CD en GitLab.

**Why this priority**: Permite comprobar en el proyecto oficial (`89374502`) la ejecución real de `quality` y `build` (`M4-03`, `M4-04`, `M4-05`), dejando registradas para una unidad posterior la separación explícita `quality → test → build → deploy` y la etapa `deploy`.

**Independent Test**: Consultar con `glab` en solo lectura los pipelines y tags del Container Registry de `vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades` tras la primera sincronización.

**Acceptance Scenarios**:

1. **Given** la llegada del primer push sincronizado a `develop` en GitLab (`id=89374502`), **When** GitLab evalúa `.gitlab-ci.yml`, **Then** ejecuta las etapas `quality` (`lint`, `run_test`) y `build` (`package_wheel`, `build_docker`) con estado `success`.
2. **Given** el job `build_docker` exitoso en rama protegida `develop`, **When** publica en `registry.gitlab.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades`, **Then** existe al menos una imagen etiquetada de forma trazable con el SHA del commit.

---

### Edge Cases

- **Divergencia de historial en GitLab:** Si alguien realizara un commit directo en GitLab rompiendo el fast-forward desde GitHub, el push sin `--force` debe fallar explícitamente y abortar el job para revisión humana (nunca sobrescribir con `--force`).
- **Ramas `feature/*`:** No deben sincronizarse hacia GitLab para evitar ruido, consumo innecesario de minutos de runner o exposición de trabajo en progreso fuera de GitHub.
- **Expiración del token PrAT:** Si `GITLAB_SYNC_TOKEN` caduca, el workflow fallará con error de autenticación sin reintentos destructivos y notificará la necesidad de rotación manual en GitLab + GitHub Secrets.
- **Diferencia de etapas CI/CD:** `.gitlab-ci.yml` actual define `quality` y `build`; la separación explícita `quality → test → build → deploy` enseñada en clase y la etapa `deploy` quedan registradas como pendientes para confirmación normativa posterior, sin modificar `.gitlab-ci.yml` en esta unidad.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema DEBE sincronizar de forma unidireccional (`GitHub → GitLab`) exclusivamente las ramas `develop` y `main` tras eventos `push` en GitHub (o `workflow_dispatch` sobre esas mismas ramas).
- **FR-002**: El sistema NO DEBE sincronizar ramas `feature/*`, ejecutar sincronización bidireccional (`GitLab → GitHub`) ni utilizar `git push --force`, `git reset --hard` ni borrado de refs remotas.
- **FR-003**: El workflow DEBE utilizar historial completo (`fetch-depth: 0`) y transferir objetos Git LFS (`model.safetensors`) hacia GitLab antes del push de la rama.
- **FR-004**: El workflow DEBE verificar tras el push que el SHA de la rama en GitLab (`git ls-remote`) coincide exactamente con `github.sha`.
- **FR-005**: La autenticación contra GitLab DEBE realizarse mediante un Project Access Token (PrAT) del proyecto `89374502` con alcance mínimo `write_repository`, fecha de expiración acotada y almacenamiento exclusivo en GitHub Secrets (`GITLAB_SYNC_TOKEN`), sin imprimir credenciales ni configurar URLs remotas con tokens embebidos en disco.
- **FR-006**: Las ramas `main` y `develop` en GitLab DEBEN permanecer protegidas (`allow_force_push = false`) permitiendo el push fast-forward únicamente a la identidad del PrAT autorizado.
- **FR-007**: Esta unidad NO DEBE modificar `.gitlab-ci.yml`; la separación explícita `quality → test → build → deploy` y la etapa `deploy` se documentan como pendientes de confirmación normativa posterior.

### Key Entities

- **Repositorio Fuente (GitHub):** `vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades` — fuente única de verdad para código, PRs, Issues, Kanban y revisión humana.
- **Repositorio Destino (GitLab):** `vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades` (`id=89374502`) — plataforma de CI/CD, Container Registry y futuro despliegue M4.
- **Credencial de Sincronización (PrAT):** Token de proyecto GitLab con scope `write_repository` y expiración definida, almacenado en GitHub Secrets (`GITLAB_SYNC_TOKEN`).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% de los merges a `develop` y `main` en GitHub se replican en GitLab (`id=89374502`) en una única ejecución de workflow con equivalencia exacta de SHA (`github.sha == gitlab_ref_sha`).
- **SC-002**: `0` ocurrencias de `--force`, sincronización inversa o credenciales en archivos del repositorio o logs de GitHub Actions.
- **SC-003**: Primer pipeline en `develop` del proyecto GitLab `89374502` completado en estado `success` (etapas `quality` y `build`) con al menos 1 imagen verificada en el Container Registry oficial.

## Assumptions

- El plan vigente de GitLab.com no habilita Pull Mirroring nativo (`HTTP 403` observado en `M4-046-ACC-CIERRE`), por lo que GitHub Actions es el mecanismo estándar sin costo adicional.
- Un administrador del repositorio en GitHub (`vivacius`) cargará el secreto `GITLAB_SYNC_TOKEN` en GitHub Settings tras la generación del PrAT en GitLab.
- El proyecto auxiliar `juanalvear01/copiamodulo2` queda únicamente como referencia histórica de pruebas previas.

---

<!-- [M1-M4 GOVERNANCE EXTENSION] -->
## M1–M4 Academic Alignment & Protected Capabilities

> **Referencias normativas:** [AGENTS.md](../../AGENTS.md) · [Constitución](../../.specify/memory/constitution.md) · [Matriz Académica M1–M4](../../docs/academic-compliance-matrix.md) · Skills: [`academic-compliance`](../../.agents/skills/academic-compliance/SKILL.md), [`sdd-workflow`](../../.agents/skills/sdd-workflow/SKILL.md)

- **ID Estable y Trazabilidad:** `SPEC-046` | **Historia / Issue (GitHub Projects):** `M4 / TOOL-05 (pendiente Issue)` | **Condición temporal:** **Prospectiva** (elaborada ANTES de implementar `.github/workflows/sync-gitlab.yml` y antes de configurar secretos/mirroring).
- **Requisitos académicos aplicables (Matriz § 1):** `TOOL-01`, `TOOL-03`, `TOOL-04`, `TOOL-05`, `TOOL-06`, `TOOL-07`, `M4-03`, `M4-04`, `M4-05`, `M4-06` — Cumplimiento acumulativo `M1`–`M4`.
- **Tecnologías prohibidas:** Streamlit (frontend evaluable M3/M4), `pip`, `requirements.txt`, notebooks `.ipynb`.
- **Capacidades protegidas a conservar (Matriz § 2):** Modelo DINOv2-small / `model.safetensors` (`local_files_only=True`), 38 clases, $\tau=0.60$, descargo agronómico, FastAPI (`/health`, `/model-info`, `/predict`, `/docs`), UI desacoplada HTTP, MLflow (`mlflow_tracking.db`, `mlruns/`), `pytest` AAA ($\ge 120$ pruebas, $\ge 85\%$ cov.), Docker CPU/Nginx, `.gitlab-ci.yml` (sin alterar en esta unidad), `.github/workflows/ci.yml`, Constitución y `specs/001..040/`.
<!-- [/M1-M4 GOVERNANCE EXTENSION] -->
