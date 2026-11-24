---
description: "Lista de tareas prospectiva para SPEC-048 (Seguridad, Secretos y Protección - Issue #50)"
---

# Tasks: Seguridad, Secretos CI/CD y Protección (`SPEC-048` / Issue `#50`)

**Input**: [spec.md](spec.md), [plan.md](plan.md)

## Phase 1: Protección de Ramas y Credenciales (Autorización Humana)

- [ ] T001 [Humano/Owner] Proteger rama `develop` en GitLab (`89374502`) con `allow_force_push = false`
- [ ] T002 [Humano/Owner] Generar PrAT (`write_repository`, expiración 60–90 días) y Deploy Token (`read_registry`) en GitLab (`89374502`)
- [ ] T003 [Humano/Admin GitHub] Cargar `GITLAB_SYNC_TOKEN` en GitHub Secrets (`vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades`)
- [ ] T004 [Humano/Owner] Registrar variables protegidas/enmascaradas en GitLab CI/CD para `deploy_vps` (`DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_PATH`, `SSH_PRIVATE_KEY`, `SSH_KNOWN_HOSTS`, `PUBLIC_HOST`, `LETSENCRYPT_EMAIL`, `DEPLOY_TOKEN_USER`, `DEPLOY_TOKEN`)

## Phase 2: Auditoría de Datos Personales y Cierre

- [ ] T005 Auditar archivos versionados (`docs/`, `deploy/`, `specs/`, workflows) verificando ausencia de secretos, IPs privadas o datos personales innecesarios
- [ ] T006 Si se detectan datos personales innecesarios en archivos versionados, corregirlos mediante PR limpia sin reescribir historial
- [ ] T007 Verificar en solo lectura con `glab api` que `develop` está protegida y adjuntar evidencia (solo nombres de variables, nunca valores) en Issue `#50`
