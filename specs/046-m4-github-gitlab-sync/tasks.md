---
description: "Lista de tareas prospectiva para SPEC-046 (Sincronización Unidireccional GitHub -> GitLab)"
---

# Tasks: Sincronización Unidireccional GitHub → GitLab (`SPEC-046`)

**Input**: Design documents from `/specs/046-m4-github-gitlab-sync/`
**Prerequisites**: [spec.md](spec.md), [plan.md](plan.md)

> **Nota de estado (actualizada `2026-11-25`, unidad `M4-DOC-46-50`):** El diseño prospectivo original preveía `.github/workflows/sync-gitlab.yml` y un PrAT con rol `Maintainer`. En la ejecución posterior se integró `.github/workflows/mirror-to-gitlab.yml` (PR `#45`), se configuró `GITLAB_SYNC_TOKEN` con rol `Developer (30)` y se protegió `develop` en GitLab (`id: 352179308`). Permanece pendiente la validación en vivo del próximo *push* sobre `develop` ya protegida y la sincronización hacia `main` protegida.

## Phase 1: Prerrequisitos Humanos y Seguridad en Plataformas (Bloqueante)

**Purpose**: Preparar credenciales mínimas y protección de ramas antes de activar el workflow automático.

- [ ] T001 [Humano/Owner] **[PARCIAL]** Generar Project Access Token (PrAT) en GitLab (`id=89374502`) con rol `Maintainer`, scope único `write_repository` y expiración acotada (60–90 días). *Evidencia/Desviación:* PrAT `GITLAB_SYNC_TOKEN` (`id: 30015655`) creado con scope `write_repository` y vencimiento `2026-12-25`, pero con rol **`Developer (30)`** (decisión posterior en lugar de `Maintainer`), lo que habilita *push* a `develop` pero no a `main` protegida.
- [x] T002 [Humano/Admin GitHub] **[COMPLETA]** Registrar el secreto `GITLAB_SYNC_TOKEN` (y opcionalmente `GITLAB_SYNC_USER`) en GitHub Repository Secrets de `vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades`. *Evidencia:* Secreto cargado por `@vivacius` y validado en GitHub Actions (`#45748907446`, `#45749582913`).
- [ ] T003 [Humano/Owner] **[PARCIAL]** Proteger la rama `develop` en GitLab (`id=89374502`) con `allow_force_push = false` y verificar que `main` mantiene la misma política sin bloquear al PrAT. *Evidencia/Bloqueo:* `develop` protegida (`id: 352179308`, `allow_force_push=false`, `push: Developers + Maintainers (30)`, `merge: Maintainers (40)`); sin embargo, `main` exige `Maintainers (40)` para `push` (bloquea al PrAT `Developer 30`) y falta comprobar en vivo el próximo *push* tras proteger `develop` (Issue `#46`).

**Checkpoint**: Credenciales y protección de ramas listas sin exposición en el repositorio.

---

## Phase 2: User Story 1 & 2 — Implementación del Workflow Seguro (Priority: P1) 🎯 MVP

**Goal**: Replicar automáticamente `develop` y `main` desde GitHub hacia GitLab con Git LFS, sin `--force` y con verificación exacta de SHA.

**Independent Test**: Merge de PR aprobada hacia `develop` en GitHub → job `sync` verde → SHA de `develop` en GitLab igual a `origin/develop`.

- [x] T004 [US1] **[COMPLETA]** Crear rama `feature/m4-spec-046-github-gitlab-sync` desde `develop` (con autorización humana). *Evidencia:* Rama creada, integrada vía PR `#47` (`MERGED`) y limpiada en `M4-MAINT-01`.
- [x] T005 [US1][US2] **[COMPLETA]** Implementar `.github/workflows/sync-gitlab.yml` *(implementado finalmente como **`.github/workflows/mirror-to-gitlab.yml`**)* con triggers `push` (`develop`, `main`) y `workflow_dispatch` restringido, `fetch-depth: 0`, `lfs: true` y `GIT_ASKPASS` temporal sin imprimir tokens. *Evidencia:* PR `#45` (`MERGED`).
- [x] T006 [US1] **[COMPLETA]** Incluir transferencia explícita de objetos Git LFS (`git lfs fetch` / `git lfs push`) y push fast-forward sin `--force`. *Evidencia:* Implementado en `.github/workflows/mirror-to-gitlab.yml` (PR `#45`) y verificado con descarga real de `model.safetensors` en GitLab CI (`#3117068885`).
- [x] T007 [US1] **[COMPLETA]** Incluir verificación de equivalencia exacta de SHA (`git ls-remote` == `github.sha`) con fallo seguro ante divergencia. *Evidencia:* Implementado en `.github/workflows/mirror-to-gitlab.yml` y verificado en runs `#45748907446` (`40af02d8...`) y `#45749582913` (`305f946b...`).
- [x] T008 [US1] **[COMPLETA]** Validar sintaxis del workflow, abrir PR con `.github/PULL_REQUEST_TEMPLATE.md`, obtener revisión de un par y fusionar hacia `develop`. *Evidencia:* PR `#45` y PR `#47` (`MERGED`); la validación del próximo espejo ya con `develop` protegida queda pendiente del siguiente *merge* legítimo.

**Checkpoint**: Sincronización automática operativa tras merge en `develop`.

---

## Phase 3: User Story 3 — Verificación de Pipeline GitLab y Container Registry (Priority: P2)

**Goal**: Confirmar en solo lectura que el primer push sincronizado ejecuta `quality` + `build` y publica imagen en Container Registry.

**Independent Test**: Consultas `glab api` sobre `projects/89374502/pipelines` y `projects/89374502/registry/repositories`.

- [x] T009 [US3] **[COMPLETA]** Verificar con `glab` (y GitLab MCP si está configurado) que el pipeline de `develop` en `89374502` ejecutó `quality` (`lint`, `run_test`) y `build` (`package_wheel`, `build_docker`) en estado `success`. *Evidencia:* Pipelines `#3117043781` (`40af02d8...`) y `#3117068885` (`305f946b...`) en estado `success` (`lint`, `run_test`, `package_wheel`, `build_docker`).
- [x] T010 [US3] **[COMPLETA]** Verificar en `registry.gitlab.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades` la publicación de la imagen Docker con tag trazable por SHA. *Evidencia:* Tags `305f946b7d4b573781754e5acf891f8c8fc1aea9`, `40af02d8e0c22581cb6272cfb8ec7340a6aaf483` y `latest` confirmados vía API.
- [ ] T011 [US3] **[PENDIENTE]** Actualizar `docs/academic-compliance-matrix.md` (`TOOL-05`, `M4-03`, `M4-05`, `M4-06`) registrando evidencia real y dejando pendiente explícito de confirmación normativa para etapas `quality → test → build → deploy` y `deploy` a VPS. *Bloqueo:* Pendiente validar el próximo espejo sobre `develop` protegida y coordinar cierre con `#52`.
