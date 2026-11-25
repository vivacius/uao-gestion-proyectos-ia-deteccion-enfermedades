# Implementation Plan: Validación E2E, Despliegue Continuo y Demostración Pública HTTPS

**Branch**: `feature/m4-plan-01-specs-048-050` | **Date**: 2026-11-23 | **Spec**: [spec.md](spec.md)

**Input**: Issue `#51` — `/specs/049-m4-e2e-public-validation/spec.md`

## Summary

Planificar la ejecución controlada y verificación pública de extremo a extremo del despliegue continuo en VPS (`deploy_vps`), validando certificado TLS/HTTPS, endpoints FastAPI, frontend desacoplado, aislamiento del puerto `8000` y actualización automática tras un push autorizado en `develop`.

## Technical Context

**Language/Version**: `curl`, `docker compose`, `glab 1.131.0`, FastAPI HTTP/HTTPS

**Primary Dependencies**: `#48` (Pipeline + Registry), `#49` (VPS + Firewall + Proxy TLS), `#50` (Variables protegidas)

**Storage**: Certificados Let's Encrypt en volumen persistente en VPS; evidencias sanitizadas en `docs/deployment-m4.md`

**Testing**: Pruebas HTTP/HTTPS funcionales (`/health`, `/model-info`, `/docs`, `/predict` válido e inválido), prueba negativa de puerto `8000` y verificación de SHA en contenedor

**Target Platform**: VPS Linux + Nginx TLS + Docker CPU

**Project Type**: Validación operacional E2E

**Constraints**: No exponer IPs privadas, llaves SSH ni tokens en la documentación de evidencias

## Constitution Check

- **Veracidad (§ IV / AGENTS.md):** Cumplido — no se reportará `VERIFICADO` sin evidencia real de `/health` 200 y push automático.

## Project Structure

```text
specs/049-m4-e2e-public-validation/
├── spec.md
├── plan.md
└── tasks.md
```

**Structure Decision**: Las evidencias sanitizadas se consolidarán en `docs/deployment-m4.md` mediante PR tras completar el despliegue.

---

<!-- [M1-M4 GOVERNANCE EXTENSION] -->
## M1–M4 Governance, Makefile & Security Gate

> **Referencias normativas:** [AGENTS.md](../../AGENTS.md) · [Constitución](../../.specify/memory/constitution.md) · [Matriz Académica M1–M4](../../docs/academic-compliance-matrix.md)

- **Validación:** Confirmar `GET /health` 200 por HTTPS sin alterar contratos M3.
<!-- [/M1-M4 GOVERNANCE EXTENSION] -->
