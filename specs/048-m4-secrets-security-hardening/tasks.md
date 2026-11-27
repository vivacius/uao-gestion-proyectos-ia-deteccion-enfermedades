---
description: "Lista de tareas prospectiva para SPEC-048 (Seguridad, Secretos y Protección - Issue #50)"
---

# Tasks: Seguridad, Secretos CI/CD y Protección (`SPEC-048` / Issue `#50`)

**Input**: [spec.md](spec.md), [plan.md](plan.md)

## Phase 1: Protección de Ramas y Credenciales (Autorización Humana)

- [x] T001 [Humano/Owner] **[COMPLETA]** Proteger rama `develop` en GitLab (`89374502`) con `allow_force_push = false`. *Evidencia:* Regla `id: 352179308` (`protected=true`, `allow_force_push=false`, `push: Developers + Maintainers (30)`, `merge: Maintainers (40)`). Pendiente: protección de `main`/`develop` en GitHub por `@vivacius` y prueba en vivo del próximo espejo sobre `develop` protegida.
- [ ] T002 [Humano/Owner] **[PARCIAL]** Generar PrAT (`write_repository`, expiración 60–90 días) y Deploy Token (`read_registry`) en GitLab (`89374502`). *Evidencia/Desviación:* Deploy Token `read_registry` creado (`id: 17519681`, `agroscan-vps-registry-read`, expira `2026-12-25`). El PrAT `GITLAB_SYNC_TOKEN` (`id: 30015655`) está activo con scope `write_repository` y expiración `2026-12-25`, pero en rol `Developer (30)` (no permite *push* a `main` protegida).
- [x] T003 [Humano/Admin GitHub] **[COMPLETA]** Cargar `GITLAB_SYNC_TOKEN` en GitHub Secrets (`vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades`). *Evidencia:* Secreto operativo y verificado en GitHub Actions (`#45748907446`, `#45749582913`).
- [ ] T004 [Humano/Owner] **[PARCIAL]** Registrar variables protegidas/enmascaradas en GitLab CI/CD para `deploy_vps` (`DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_PATH`, `SSH_PRIVATE_KEY`, `SSH_KNOWN_HOSTS`, `PUBLIC_HOST`, `LETSENCRYPT_EMAIL`, `DEPLOY_TOKEN_USER`, `DEPLOY_TOKEN`). *Evidencia/Bloqueo:* Configuradas 2/9 (`DEPLOY_TOKEN_USER` `Protected=true/Masked=false` y `DEPLOY_TOKEN` `Protected=true/Masked=true`). Las 7 restantes dependen de VPS/DNS (Issue `#49`).

## Phase 2: Auditoría de Datos Personales y Cierre

- [ ] T005 **[PENDIENTE]** Auditar archivos versionados (`docs/`, `deploy/`, `specs/`, workflows) verificando ausencia de secretos, IPs privadas o datos personales innecesarios. *Bloqueo:* Pendiente de ejecución programada en `#50`.
- [ ] T006 **[PENDIENTE]** Si se detectan datos personales innecesarios en archivos versionados, corregirlos mediante PR limpia sin reescribir historial. *Bloqueo:* Sujeto a resultado de `T005` y decisión humana sobre tratamiento de C.C. en `documento/Plantilla.tex`/PDF.
- [ ] T007 **[PARCIAL]** Verificar en solo lectura con `glab api` que `develop` está protegida y adjuntar evidencia (solo nombres de variables, nunca valores) en Issue `#50`. *Evidencia/Pendiente:* Protección de `develop` y metadatos de las 2 variables ya registrados en `#50` (sin valores); resta completar las 7 variables dependientes de `#49` y el reporte de `T005`.
