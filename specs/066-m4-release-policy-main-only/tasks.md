# Tasks: Política de Despliegue Exclusivo desde `main` (SPEC-066)

**Input**: [spec.md](./spec.md) · [plan.md](./plan.md)

## Phase 1: Especificación y Rama

- [x] T001 Crear rama `fix/m4-release-main-only` desde `develop` (`501c1ec3`)
- [x] T002 Crear `specs/066-m4-release-policy-main-only/` (`spec.md`, `plan.md`, `tasks.md`) sin reutilizar IDs previos

## Phase 2: Implementación Mínima

- [x] T003 Actualizar `.gitlab-ci.yml`: restringir `:latest` y `deploy_vps` (`when: on_success`) a `$CI_DEFAULT_BRANCH` (`main`)
- [x] T004 Añadir prueba contractual en `tests/unit/test_client_scripts_and_m4_contracts.py` para `deploy_vps` y `:latest`
- [x] T005 Actualizar `docs/deployment-m4.md` (política `main`-only y persistencia `.env` en rollback) y `docs/sustentacion-m4.md` (demo vía `main`, sin afirmar *zero-downtime*)

## Phase 3: Validación Local y PR

- [x] T006 Ejecutar `uv run ruff check .`, `uv run ruff format --check .`, `uv run pytest tests/unit -q` y `glab ci lint .gitlab-ci.yml`
- [ ] T007 Revisar `git diff` y ausencia de secretos; commit Conventional Commits y push a `origin`
- [ ] T008 Abrir PR hacia `develop` con `.github/PULL_REQUEST_TEMPLATE.md` y verificar checks de GitHub (sin merge)
