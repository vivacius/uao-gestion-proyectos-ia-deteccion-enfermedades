---
description: "Lista de tareas prospectiva para SPEC-046 (Sincronización Unidireccional GitHub -> GitLab)"
---

# Tasks: Sincronización Unidireccional GitHub → GitLab (`SPEC-046`)

**Input**: Design documents from `/specs/046-m4-github-gitlab-sync/`
**Prerequisites**: [spec.md](spec.md), [plan.md](plan.md)

> **Nota de estado (actualizada `2026-11-26`, unidad `M4-CLOSE-46-FINAL`):** El diseño prospectivo original preveía `.github/workflows/sync-gitlab.yml` y un PrAT único con rol `Maintainer`. En la ejecución final se integró `.github/workflows/mirror-to-gitlab.yml` (`PR #45`, endurecido en `PR #56` y ampliado en `PR #66`) separando ambos espejos bajo mínimo privilegio: `develop` usa `GITLAB_SYNC_TOKEN` (`id: 30015655`, `Developer 30`) y `main` usa la Deploy Key SSH `github-main-mirror` (`id: 22202767`) desde el Environment protegido `gitlab-main-mirror` (`GITLAB_MAIN_DEPLOY_KEY`). Ambos espejos fueron verificados en vivo tras proteger las ramas en GitLab (`89374502`): `develop` (`573ce21d`, run `#45937181274`) y `main` (`PR #67`, `d3c2aebb7935a72252a6ffb76f2c2cced93dee76`, run `#45937826510`, pipeline `#3121720777` con `deploy_vps` manual).

## Phase 1: Prerrequisitos Humanos y Seguridad en Plataformas (Bloqueante)

**Purpose**: Preparar credenciales mínimas y protección de ramas antes de activar el workflow automático.

- [x] T001 [Humano/Owner] **[COMPLETA]** Generar credencial acotada en GitLab (`id=89374502`) con scope mínimo y expiración/alcance controlado. *Evidencia:* PrAT `GITLAB_SYNC_TOKEN` (`id: 30015655`, `write_repository`, `Developer 30`, vence `2026-12-25`) para `develop` y Deploy Key SSH `github-main-mirror` (`id: 22202767`, `can_push=true`) autorizada exclusivamente sobre `main` protegida (`PR #66`, `MERGED`).
- [x] T002 [Humano/Admin GitHub] **[COMPLETA]** Registrar el secreto `GITLAB_SYNC_TOKEN` (y opcionalmente `GITLAB_SYNC_USER`) en GitHub Repository Secrets de `vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades`. *Evidencia:* Secreto cargado por `@vivacius` y validado en GitHub Actions (`#45748907446`, `#45749582913`, `#45915628026`, `#45923736017`, `#45927337605`, `#45937181274`), junto con `GITLAB_MAIN_DEPLOY_KEY` en el Environment `gitlab-main-mirror` restringido a `main` (`#45937826510`).
- [x] T003 [Humano/Owner] **[COMPLETA]** Proteger la rama `develop` en GitLab (`id=89374502`) con `allow_force_push = false` y verificar que `main` mantiene la misma política sin bloquear la sincronización automática. *Evidencia:* `develop` protegida (`id: 352179308`, `allow_force_push=false`, `push: Developers + Maintainers (30)`, `merge: Maintainers (40)`) verificada en vivo hasta `573ce21d` (run `#45937181274`). En `main` (`id: 351965449`, `allow_force_push=false`, `push: Maintainers 40` + `deploy_key_id: 22202767`, `merge: Maintainers 40`), el espejo automático `mirror_main` fue verificado en vivo tras `PR #67` (`d3c2aebb7935a72252a6ffb76f2c2cced93dee76`, run `#45937826510`, SHA idéntico en GitHub y GitLab).

**Checkpoint**: Credenciales y protección de ramas operativas y verificadas en vivo tanto en `develop` como en `main`.

---

## Phase 2: User Story 1 & 2 — Implementación del Workflow Seguro (Priority: P1) 🎯 MVP

**Goal**: Replicar automáticamente `develop` y `main` desde GitHub hacia GitLab con Git LFS, sin `--force` y con verificación exacta de SHA.

**Independent Test**: Merge de PR aprobada hacia `develop` en GitHub → job `sync` verde → SHA de `develop` en GitLab igual a `origin/develop`.

- [x] T004 [US1] **[COMPLETA]** Crear rama `feature/m4-spec-046-github-gitlab-sync` desde `develop` (con autorización humana). *Evidencia:* Rama creada, integrada vía PR `#47` (`MERGED`) y limpiada en `M4-MAINT-01`.
- [x] T005 [US1][US2] **[COMPLETA]** Implementar `.github/workflows/sync-gitlab.yml` *(implementado finalmente como **`.github/workflows/mirror-to-gitlab.yml`**)* con triggers `push` (`develop`, `main`) y `workflow_dispatch` restringido, `fetch-depth: 0`, `lfs: true` y `GIT_ASKPASS` temporal sin imprimir tokens. *Evidencia:* PR `#45` y PR `#56` (`MERGED`).
- [x] T006 [US1] **[COMPLETA]** Incluir transferencia explícita de objetos Git LFS (`git lfs fetch` / `git lfs push`) y push fast-forward sin `--force`. *Evidencia:* Implementado en `.github/workflows/mirror-to-gitlab.yml` (PR `#45`, PR `#56`) y verificado con materialización real de `model.safetensors` (`88 MB`) en GitLab CI (`#3117068885`, `#3121264383`, `#3121439814`, `#3121517394`).
- [x] T007 [US1] **[COMPLETA]** Incluir verificación de equivalencia exacta de SHA (`git ls-remote` == `github.sha`) con fallo seguro ante divergencia. *Evidencia:* Implementado en `.github/workflows/mirror-to-gitlab.yml` y verificado en runs `#45748907446` (`40af02d8...`), `#45749582913` (`305f946b...`), `#45915628026` (`d5277c89...`), `#45923736017` (`33ff9a2c...`) y `#45927337605` (`218b7fc2c1188b29ea9596ed5e209f228d7a62a8`).
- [x] T008 [US1] **[COMPLETA]** Validar sintaxis del workflow, abrir PR con `.github/PULL_REQUEST_TEMPLATE.md`, obtener revisión de un par y fusionar hacia `develop`. *Evidencia:* PR `#45`, PR `#47` y PR `#56` (`MERGED`), con sincronización posterior verificada sobre `develop` protegida hasta `218b7fc2c1188b29ea9596ed5e209f228d7a62a8` (Run `#45927337605`).

**Checkpoint**: Sincronización automática operativa y verificada tras merges en `develop` protegida.

---

## Phase 3: User Story 3 — Verificación de Pipeline GitLab y Container Registry (Priority: P2)

**Goal**: Confirmar en solo lectura que el primer push sincronizado ejecuta `quality` + `build` y publica imagen en Container Registry.

**Independent Test**: Consultas `glab api` sobre `projects/89374502/pipelines` y `projects/89374502/registry/repositories`.

- [x] T009 [US3] **[COMPLETA]** Verificar con `glab` (y GitLab MCP si está configurado) que el pipeline de `develop` en `89374502` ejecutó `quality` (`lint`, `run_test`) y `build` (`package_wheel`, `build_docker`) en estado `success`. *Evidencia:* Pipelines `#3117043781` (`40af02d8...`), `#3117068885` (`305f946b...`), `#3121264383` (`d5277c89...`), `#3121439814` (`33ff9a2c...`) y `#3121517394` (`218b7fc2...`, incluyendo `lint` `#18416796070`, `run_test` `#18416796071`, `package_wheel` `#18416796072`, `build_docker` `#18416796073` y `deploy_vps` `#18416957665`) en estado `success`.
- [x] T010 [US3] **[COMPLETA]** Verificar en `registry.gitlab.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades` la publicación de la imagen Docker con tag trazable por SHA. *Evidencia:* Tags `40af02d8e0c22581cb6272cfb8ec7340a6aaf483`, `305f946b7d4b573781754e5acf891f8c8fc1aea9`, `d5277c891e879251f03416604e0d0ca400e7562a`, `33ff9a2caf8220bd5e3b0fee60c77a7066c4219c`, `218b7fc2c1188b29ea9596ed5e209f228d7a62a8` y `latest` confirmados vía API (`repository id: 13061143`).
- [x] T011 [US3] **[COMPLETA]** Actualizar `docs/academic-compliance-matrix.md` (`TOOL-05`, `M4-03`, `M4-05`, `M4-06`) registrando evidencia real y dejando constancia de la ejecución completa `quality → test → build → deploy` (`deploy_vps` `#18416957665`) en el proyecto oficial `89374502`. *Evidencia:* Filas `M4-03`, `M4-05`, `M4-06` y `TOOL-05` actualizadas con los IDs verificados de GitHub Actions y GitLab CI/Registry en coordinación con `#52` (PR `#59`).
