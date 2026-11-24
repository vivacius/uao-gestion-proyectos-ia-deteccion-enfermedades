---
description: "Lista de tareas prospectiva para SPEC-046 (Sincronización Unidireccional GitHub -> GitLab)"
---

# Tasks: Sincronización Unidireccional GitHub → GitLab (`SPEC-046`)

**Input**: Design documents from `/specs/046-m4-github-gitlab-sync/`
**Prerequisites**: [spec.md](spec.md), [plan.md](plan.md)

> **Nota de estado:** Este listado corresponde a una **propuesta prospectiva**, no a una implementación activa. El mecanismo GitHub Actions es **provisional** hasta confirmar el trabajo del compañero en GitLab (evitando duplicar integraciones ya implementadas), y toda creación de tokens, protecciones y workflows requiere autorización humana posterior.

## Phase 1: Prerrequisitos Humanos y Seguridad en Plataformas (Bloqueante)

**Purpose**: Preparar credenciales mínimas y protección de ramas antes de activar el workflow automático.

- [ ] T001 [Humano/Owner] Generar Project Access Token (PrAT) en GitLab (`id=89374502`) con rol `Maintainer`, scope único `write_repository` y expiración acotada (60–90 días)
- [ ] T002 [Humano/Admin GitHub] Registrar el secreto `GITLAB_SYNC_TOKEN` (y opcionalmente `GITLAB_SYNC_USER`) en GitHub Repository Secrets de `vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades`
- [ ] T003 [Humano/Owner] Proteger la rama `develop` en GitLab (`id=89374502`) con `allow_force_push = false` y verificar que `main` mantiene la misma política sin bloquear al PrAT

**Checkpoint**: Credenciales y protección de ramas listas sin exposición en el repositorio.

---

## Phase 2: User Story 1 & 2 — Implementación del Workflow Seguro (Priority: P1) 🎯 MVP

**Goal**: Replicar automáticamente `develop` y `main` desde GitHub hacia GitLab con Git LFS, sin `--force` y con verificación exacta de SHA.

**Independent Test**: Merge de PR aprobada hacia `develop` en GitHub → job `sync` verde → SHA de `develop` en GitLab igual a `origin/develop`.

- [ ] T004 [US1] Crear rama `feature/m4-spec-046-github-gitlab-sync` desde `develop` (con autorización humana)
- [ ] T005 [US1][US2] Implementar `.github/workflows/sync-gitlab.yml` con triggers `push` (`develop`, `main`) y `workflow_dispatch` restringido, `fetch-depth: 0`, `lfs: true` y `GIT_ASKPASS` temporal sin imprimir tokens
- [ ] T006 [US1] Incluir transferencia explícita de objetos Git LFS (`git lfs fetch` / `git lfs push`) y push fast-forward sin `--force`
- [ ] T007 [US1] Incluir verificación de equivalencia exacta de SHA (`git ls-remote` == `github.sha`) con fallo seguro ante divergencia
- [ ] T008 [US1] Validar sintaxis del workflow, abrir PR con `.github/PULL_REQUEST_TEMPLATE.md`, obtener revisión de un par y fusionar hacia `develop`

**Checkpoint**: Sincronización automática operativa tras merge en `develop`.

---

## Phase 3: User Story 3 — Verificación de Pipeline GitLab y Container Registry (Priority: P2)

**Goal**: Confirmar en solo lectura que el primer push sincronizado ejecuta `quality` + `build` y publica imagen en Container Registry.

**Independent Test**: Consultas `glab api` sobre `projects/89374502/pipelines` y `projects/89374502/registry/repositories`.

- [ ] T009 [US3] Verificar con `glab` (y GitLab MCP si está configurado) que el pipeline de `develop` en `89374502` ejecutó `quality` (`lint`, `run_test`) y `build` (`package_wheel`, `build_docker`) en estado `success`
- [ ] T010 [US3] Verificar en `registry.gitlab.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades` la publicación de la imagen Docker con tag trazable por SHA
- [ ] T011 [US3] Actualizar `docs/academic-compliance-matrix.md` (`TOOL-05`, `M4-03`, `M4-05`, `M4-06`) registrando evidencia real y dejando pendiente explícito de confirmación normativa para etapas `quality → test → build → deploy` y `deploy` a VPS
