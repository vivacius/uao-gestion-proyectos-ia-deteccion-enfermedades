# Implementation Plan: Sincronización Unidireccional GitHub → GitLab (M4)

**Branch**: `feature/m4-spec-046-github-gitlab-sync` *(propuesta; no creada aún en Git)* | **Date**: 2026-11-23 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/046-m4-github-gitlab-sync/spec.md`

## Summary

Proponer (sin implementar ni activar todavía) un mecanismo mediante workflow de GitHub Actions (`.github/workflows/sync-gitlab.yml`) que sincronice de forma unidireccional, no destructiva y sin `--force` las ramas `develop` y `main` desde GitHub (`vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades`) hacia el proyecto oficial en GitLab (`id=89374502`), incluyendo objetos Git LFS (`model.safetensors`), verificación exacta de SHA y autenticación mediante Project Access Token (PrAT) almacenado en GitHub Secrets (`GITLAB_SYNC_TOKEN`). Este diseño mediante GitHub Actions es **provisional** hasta confirmar el alcance del trabajo de compañeros en GitLab para no duplicar integraciones existentes; toda creación de tokens, protecciones y workflows requiere autorización humana posterior.

## Technical Context

**Language/Version**: GitHub Actions YAML + Git / Git LFS + PowerShell/Bash CLI (`glab 1.131.0`, `gh 2.105.0`)

**Primary Dependencies**: `actions/checkout@v4` (`fetch-depth: 0`, `lfs: true`), `git`, `git-lfs`, GitLab Project Access Token (`write_repository`)

**Storage**: GitHub Secrets (`GITLAB_SYNC_TOKEN`, `GITLAB_SYNC_USER` opcional) fuera del repositorio; sin almacenamiento en disco de credenciales

**Testing**: Verificación en seco/post-merge mediante `git ls-remote` (equivalencia exacta de SHA), `glab api` (estado de pipeline y Container Registry) y `Quality Gate CI (M3)` en GitHub

**Target Platform**: GitHub Actions (`ubuntu-latest`) → GitLab.com (`projects/89374502`)

**Project Type**: Infraestructura CI/CD y sincronización entre plataformas

**Performance Goals**: Sincronización completada en $< 2\text{ min}$ por merge en `develop`/`main`; disparo inmediato del pipeline GitLab

**Constraints**: Cero `--force`, cero sincronización bidireccional, cero exposición de tokens en código o logs, cero modificación de `.gitlab-ci.yml` en esta unidad

**Scale/Scope**: 2 ramas protegidas (`develop`, `main`) y artefacto LFS `model.safetensors`

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Gitflow & Revisión Humana (§ IV):** Cumplido — toda modificación al repositorio pasará por rama `feature/*` y PR con `.github/PULL_REQUEST_TEMPLATE.md` y aprobación de un par; GitHub permanece como única fuente de verdad.
- **Seguridad y Secretos (§ V):** Cumplido — el token PrAT se almacenará exclusivamente en GitHub Secrets, pasándose mediante `GIT_ASKPASS` temporal en memoria o cabecera HTTP sin persistir URLs con token en `.git/config` ni imprimirlo en stdout/stderr.
- **Protección de capacidades M1–M3:** Cumplido — no se modifican `src/`, `api/`, `ui/`, `tests/`, `Dockerfile`, `docker-compose.yml` ni `.gitlab-ci.yml`.

## Project Structure

### Documentation (this feature)

```text
specs/046-m4-github-gitlab-sync/
├── spec.md              # Especificación prospectiva (creada en M4-046-E1)
├── plan.md              # Este plan de implementación (creado en M4-046-E1)
└── tasks.md             # Lista de tareas trazables (creada en M4-046-E1)
```

### Target Repository Artifacts (pendientes de autorización para implementación)

```text
.github/
└── workflows/
    ├── ci.yml                # Existente (protegido; no modificar)
    └── sync-gitlab.yml       # Propuesto (NO creado aún; requiere autorización humana)
```

**Structure Decision**: Mantener la sincronización aislada en un workflow dedicado `.github/workflows/sync-gitlab.yml`, separado de `.github/workflows/ci.yml`, para respetar la separación de responsabilidades y no alterar el Quality Gate M3 existente.

## Technical Design Details

### 1. Mecanismo de Autenticación Recomendado (GitLab PrAT)
- **Tipo:** Project Access Token (PrAT) generado en `vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades` (`id=89374502`).
- **Alcance (Scope):** Únicamente `write_repository`.
- **Rol:** `Maintainer` dentro del proyecto `89374502` (necesario en GitLab Free cuando `main` y `develop` están protegidas con `Allowed to push and merge: Maintainers`).
- **Expiración:** Acotada al ciclo M4 (ej. 60–90 días), con rotación documentada.
- **Almacenamiento y uso seguro:**
  - Guardado en GitHub Repository Secrets como `GITLAB_SYNC_TOKEN` (y opcionalmente `GITLAB_SYNC_USER`, o usando `oauth2` como usuario estándar de GitLab para tokens HTTPS).
  - En el runner de GitHub Actions, configurar un script `GIT_ASKPASS` temporal con permisos `0700` que lea `$GITLAB_SYNC_TOKEN` desde variable de entorno, evitando incluir el token en la URL del remoto o en comandos `git remote add` que puedan quedar en logs ante errores.

### 2. Esquema Propuesto de `.github/workflows/sync-gitlab.yml`
- **Disparadores (`on`):**
  - `push` en `branches: [develop, main]`
  - `workflow_dispatch` (solo ejecutable manualmente sobre `develop` o `main`, validado en el job para rechazar otras refs).
- **Concurrencia:** `concurrency: { group: gitlab-sync-${{ github.ref }}, cancel-in-progress: false }` (evita condiciones de carrera sin cancelar pushes legítimos en curso).
- **Permisos mínimos del token de GitHub:** `permissions: { contents: read }`.
- **Pasos del job `sync` (`runs-on: ubuntu-latest`):**
  1. `actions/checkout@v4` con `fetch-depth: 0` y `lfs: true`.
  2. Validar que `github.ref_name` sea exactamente `develop` o `main`.
  3. Configurar remoto limpio `https://gitlab.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades.git` + `GIT_ASKPASS` en memoria/archivo temporal con `trap` de limpieza.
  4. `git lfs fetch origin "${GITHUB_REF_NAME}"` y `git lfs push gitlab "${GITHUB_REF_NAME}"` (o `--all` de los objetos de la rama).
  5. `git push gitlab "HEAD:refs/heads/${GITHUB_REF_NAME}"` (estrictamente sin `--force`).
  6. Verificar equivalencia exacta de SHA: consultar `git ls-remote gitlab "refs/heads/${GITHUB_REF_NAME}"` y fallar si el SHA remoto `!= ${{ github.sha }}`.

### 3. Protección de Ramas en GitLab (`id=89374502`)
- `main`: mantener `Protected: True`, `allow_force_push: false`, `push_access_level: Maintainers`.
- `develop`: cambiar de `Protected: False` a `Protected: True`, `allow_force_push: false`, `push_access_level: Maintainers` (habilitando tanto el push del PrAT como la política de publicación en Container Registry de `M4-05`).

### 4. Registro de Pendientes Normativos en `.gitlab-ci.yml`
- El archivo `.gitlab-ci.yml` actual define etapas `quality` y `build`.
- La separación explícita en 4 etapas enseñada en clase (`quality → test → build → deploy`) y la etapa `deploy` hacia VPS quedan registradas como pendientes para confirmación normativa y ejecución en una unidad posterior (`M4-03` / `M4-07`), sin modificar `.gitlab-ci.yml` en `SPEC-046`.

---

<!-- [M1-M4 GOVERNANCE EXTENSION] -->
## M1–M4 Governance, Makefile & Security Gate

> **Referencias normativas:** [AGENTS.md](../../AGENTS.md) · [Constitución](../../.specify/memory/constitution.md) · [Matriz Académica M1–M4](../../docs/academic-compliance-matrix.md) · [Makefile](../../Makefile) · Skills: [`quality-and-make`](../../.agents/skills/quality-and-make/SKILL.md), [`github-gitlab-operations`](../../.agents/skills/github-gitlab-operations/SKILL.md), [`secure-cicd-deployment`](../../.agents/skills/secure-cicd-deployment/SKILL.md)

- **Validación sin regresiones:** Al no modificar código Python ni `.gitlab-ci.yml` en esta unidad de diseño, el Quality Gate local (`ruff`, `pytest`) permanece intacto. Cuando se implemente `.github/workflows/sync-gitlab.yml`, se validará sintaxis YAML, ausencia de secretos y ejecución controlada tras PR aprobada.
<!-- [/M1-M4 GOVERNANCE EXTENSION] -->
