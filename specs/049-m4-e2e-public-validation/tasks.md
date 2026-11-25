---
description: "Lista de tareas prospectiva para SPEC-049 (Validación E2E y Demostración Pública - Issue #51)"
---

# Tasks: Validación E2E y Demostración Pública (`SPEC-049` / Issue `#51`)

**Input**: [spec.md](spec.md), [plan.md](plan.md)

## Phase 1: Prerrequisitos de Ejecución

- [ ] T001 Confirmar cierre de `#48` (pipeline + Registry), `#49` (VPS + firewall + DNS) y `#50` (variables protegidas)

## Phase 2: Validación del Primer Despliegue y Endpoints HTTPS

- [ ] T002 Verificar ejecución `success` de `deploy_vps` en GitLab (`89374502`) y coincidencia del tag desplegado con `$CI_COMMIT_SHA`
- [ ] T003 Verificar redirección HTTP (`80`) -> HTTPS (`443`) y certificado TLS válido con `curl -I https://<dominio>/health`
- [ ] T004 Probar `GET /health` (200), `GET /model-info`, `GET /docs`, `POST /predict` (imagen válida + archivo inválido HTTP 400) y UI web estática
- [ ] T005 Verificar desde red externa que `http://<IP>:8000` no responde y `ufw status` solo expone `22/80/443`

## Phase 3: Demostración de Actualización Automática y Evidencia

- [ ] T006 Ejecutar un cambio acotado aprobado en `develop` y comprobar actualización automática en producción tras el pipeline
- [ ] T007 Documentar evidencias sanitizadas (sin secretos) en `docs/deployment-m4.md` mediante PR revisada
