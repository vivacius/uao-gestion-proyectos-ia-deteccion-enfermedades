# Implementation Plan: Política de Despliegue Exclusivo desde `main` (SPEC-066)

**Branch**: `fix/m4-release-main-only` | **Date**: 2026-11-27 | **Spec**: [spec.md](./spec.md)

## Summary

Ajustar `.gitlab-ci.yml` para que `main` (`$CI_DEFAULT_BRANCH`) sea la única rama que publique `:latest` y ejecute `deploy_vps` automáticamente (`when: on_success`), mientras `develop` mantiene `quality`, `test` y `build` con etiqueta inmutable `:$CI_COMMIT_SHA`. Incorporar prueba contractual en `tests/unit/test_client_scripts_and_m4_contracts.py` y alinear `docs/deployment-m4.md` y `docs/sustentacion-m4.md`.

## Technical Context

- **CI/CD**: GitLab CI (`.gitlab-ci.yml`) en proyecto oficial `89374502`.
- **Testing**: `pytest` (AAA) con `PyYAML` ya disponible en `tests/unit/test_client_scripts_and_m4_contracts.py`.
- **Linting**: `uv run ruff check .` y `uv run ruff format --check .`.
- **CI Syntax**: `glab ci lint .gitlab-ci.yml`.

## Architecture & Invariants Check

- Sin cambios en `src/`, `api/`, `ui/`, `Dockerfile`, `deploy/docker-compose.prod.yml`, `deploy/nginx.prod.conf.template` ni `.github/workflows/mirror-to-gitlab.yml`.
- Se conservan `resource_group: production`, `needs: [build_docker]`, `interruptible: false`, `environment: production` y `IMAGE_TAG=${CI_COMMIT_SHA}`.
- Sin infraestructura adicional ni modificación de variables/protecciones remotas.
