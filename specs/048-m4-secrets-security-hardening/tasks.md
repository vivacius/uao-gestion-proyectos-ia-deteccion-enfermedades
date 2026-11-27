---
description: "Lista de tareas prospectiva para SPEC-048 (Seguridad, Secretos y Protección - Issue #50)"
---

# Tasks: Seguridad, Secretos CI/CD y Protección (`SPEC-048` / Issue `#50`)

**Input**: [spec.md](spec.md), [plan.md](plan.md)

## Phase 1: Protección de Ramas y Credenciales (Autorización Humana)

- [x] T001 [Humano/Owner] **[COMPLETA]** Proteger rama `develop` en GitLab (`89374502`) con `allow_force_push = false`. *Evidencia:* Regla `id: 352179308` (`protected=true`, `allow_force_push=false`, `push: Developers + Maintainers (30)`, `merge: Maintainers (40)`), verificada en vivo con el espejo automático hasta `c184d1de8e0a5e8c5debd4b3a940b9b39687e688`. En GitHub, `main` y `develop` cuentan con protección activa y check obligatorio `Ruff & Unit Tests (Python 3.13 + uv)`.
- [x] T002 [Humano/Owner] **[COMPLETA]** Generar PrAT (`write_repository`, expiración 60–90 días) y Deploy Token (`read_registry`) en GitLab (`89374502`). *Evidencia:* Deploy Token `read_registry` activo (`id: 17519681`, `agroscan-vps-registry-read`, expira `2026-12-25`) y PrAT `GITLAB_SYNC_TOKEN` activo (`id: 30015655`, scope `write_repository`, expira `2026-12-25`, rol `Developer 30`; la alineación de *push* hacia `main` protegida se gestiona en `SPEC-046` / Issue `#46`).
- [x] T003 [Humano/Admin GitHub] **[COMPLETA]** Cargar `GITLAB_SYNC_TOKEN` en GitHub Secrets (`vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades`). *Evidencia:* Secreto operativo y verificado en GitHub Actions (`#45748907446`, `#45749582913`, `#45915628026`, `#45923736017`, `#45927337605`, `#45931831355`, `#45931970078`, `#45932673101`).
- [x] T004 [Humano/Owner] **[COMPLETA]** Registrar variables protegidas/enmascaradas en GitLab CI/CD para `deploy_vps` (`DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_PATH`, `SSH_PRIVATE_KEY`, `SSH_KNOWN_HOSTS`, `PUBLIC_HOST`, `LETSENCRYPT_EMAIL`, `DEPLOY_TOKEN_USER`, `DEPLOY_TOKEN`). *Evidencia:* Configuradas y verificadas las `9/9` variables en GitLab `89374502` con `protected=true` (y `masked=true` en `DEPLOY_TOKEN`, `DEPLOY_HOST`, `DEPLOY_PATH`, `PUBLIC_HOST`), validadas en los despliegues productivos `deploy_vps` `#18416957665`, `#18417303297` y `#18417442325` (`success`), junto con la exclusión explícita de `.env` y `.env.*` en `.gitignore` (PR `#60`).

## Phase 2: Auditoría de Datos Personales y Cierre

- [x] T005 **[COMPLETA]** Auditar archivos versionados (`docs/`, `deploy/`, `specs/`, workflows, `documento/`) verificando ausencia de secretos, IPs privadas o datos personales innecesarios. *Evidencia:* Auditoría documentada en Issue `#50` (`#7182964734`): `0` secretos o IPs privadas en el árbol; hallazgo acotado exclusivamente a los 4 números de identificación personal (`C.C.`) en la portada de `documento/Plantilla.tex` (líneas `106`, `108`, `110`, `112`) y `documento/Plantilla.pdf`.
- [x] T006 **[COMPLETA]** Si se detectan datos personales innecesarios en archivos versionados, corregirlos mediante PR limpia sin reescribir historial. *Evidencia:* Retiradas las 4 identificaciones personales y etiquetas `C.C.` de la portada en `documento/Plantilla.tex` y recompilado localmente `documento/Plantilla.pdf` (`17` páginas, `pdfTeX 3.141592653-2.6-1.40.29 / TeX Live 2026` en contenedor efímero `texlive/texlive:latest`), verificando con `pdftotext` `0` ocurrencias de los identificadores y de `C.C.` tanto en el `.tex` como en el `.pdf` vigentes. Conforme a `FR-003` y `AGENTS.md` § 3, no se reescribió el historial Git (los commits históricos previos conservan sus árboles originales).
- [x] T007 **[COMPLETA]** Verificar en solo lectura con `glab api` que `develop` está protegida y adjuntar evidencia (solo nombres de variables, nunca valores) en Issue `#50`. *Evidencia:* Protección de `develop` (`id: 352179308`, `allow_force_push=false`) y listado sanitizado de las `9/9` variables protegidas registrados en Issue `#50` (`#7208856199`).
