---
description: "Lista de tareas prospectiva para SPEC-049 (Validación E2E y Demostración Pública - Issue #51)"
---

# Tasks: Validación E2E y Demostración Pública (`SPEC-049` / Issue `#51`)

**Input**: [spec.md](spec.md), [plan.md](plan.md)

## Phase 1: Prerrequisitos de Ejecución

- [ ] T001 **[PARCIAL]** Confirmar cierre de `#48` (pipeline + Registry), `#49` (VPS + firewall + DNS) y `#50` (variables protegidas). *Evidencia/Pendiente:* Infraestructura VPS/HTTPS (`#49`), pipeline 4 etapas (`#48`) y 9/9 variables protegidas en GitLab (`#50`) operativos; resta cierre formal de las Issues en GitHub.

## Phase 2: Validación del Primer Despliegue y Endpoints HTTPS

- [x] T002 **[COMPLETA]** Verificar ejecución `success` de `deploy_vps` en GitLab (`89374502`) y coincidencia del tag desplegado con `$CI_COMMIT_SHA`. *Evidencia:* Despliegue exitoso sobre `develop` (`33ff9a2caf8220bd5e3b0fee60c77a7066c4219c`) en `https://agroscan-uao.duckdns.org`.
- [x] T003 **[COMPLETA]** Verificar redirección HTTP (`80`) -> HTTPS (`443`) y certificado TLS válido con `curl -i https://agroscan-uao.duckdns.org/health`. *Evidencia:* HTTP `301 Moved Permanently` → HTTPS `200 OK` con Let's Encrypt y cabeceras HSTS/seguridad.
- [x] T004 **[COMPLETA]** Probar `GET /health` (200), `GET /model-info`, `GET /docs`, `POST /predict` (imagen válida + archivo inválido HTTP 400) y UI web estática. *Evidencia:* `GET /` (`200`), `/docs` (`200`), `/health` (`200`), `/model-info` (`200`), `POST /predict` válido (`200`, `175.42 ms`), corrupto (`400`), `.bin` (`415`).
- [x] T005 **[COMPLETA]** Verificar desde red externa que `http://<IP>:8000` no responde y `ufw status` solo expone `22/80/443`. *Evidencia:* `ufw status` activo solo en `22/80/443` y `curl --connect-timeout 5 http://<IP_REDACTADA>:8000/health` → `Connection timed out`.

## Phase 3: Demostración de Actualización Automática y Evidencia

- [ ] T006 **[PENDIENTE]** Ejecutar un cambio acotado aprobado en `develop` y comprobar actualización automática en producción tras el pipeline. *Bloqueo:* Pendiente de aprobación y merge de esta PR hacia `develop` para verificar actualización al nuevo `$CI_COMMIT_SHA`.
- [x] T007 **[COMPLETA]** Documentar evidencias sanitizadas (sin secretos) en `docs/deployment-m4.md` mediante PR revisada. *Evidencia:* Sección 11 y 11.1 actualizadas en `docs/deployment-m4.md` junto con hardening de `.env` en `.gitignore`.
