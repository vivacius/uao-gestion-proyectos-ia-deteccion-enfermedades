# Tareas (Spec Kit): SPEC-047 VPS, Seguridad, HTTPS y Despliegue Continuo

**Feature Branch:** `feature/m4-gitlab-registry-deploy` | **Spec:** [spec.md](./spec.md) | **Plan:** [plan.md](./plan.md)
**Issues Relacionadas:** #46 (sincronización canónica) · #48 (CI/Registry/LFS) · #49 (VPS/firewall/TLS) · #50 (secretos) · #51 (E2E público) · #52 (gobernanza, fuera de alcance)
**Estado global:** Implementación y validación local completas; **validación en GitLab oficial y VPS pendiente**

> Convención: `[x]` solo con evidencia directa. `[ ]` pendiente. `[!]` bloqueado por permisos, credenciales o decisión humana.
>
> **Trazabilidad:** esta PR no cierra las Issues #46, #48, #49, #50 ni #51. Un GitHub Actions en verde no sustituye el pipeline oficial de GitLab ni el despliegue público.

## Fase 1 — Artefactos locales

- [x] Crear `deploy/docker-compose.prod.yml` con `api` sin `ports`, `web` 80/443 y `certbot`.
- [x] Crear `deploy/nginx.prod.conf.template` con redirección, TLS, HSTS, ACME y proxy a `api:8000`.
- [x] Crear `deploy/.env.production.example` sin secretos.
- [x] Añadir `deploy` a `stages` y el job `deploy_vps` en `.gitlab-ci.yml`.
- [x] Documentar variables, bootstrap TLS, firewall y reversión en `docs/deployment-m4.md`.
- [x] Verificar que el Compose local y el Nginx local no cambiaron.

## Fase 2 — Validación local

- [x] Parsear `.gitlab-ci.yml` con PyYAML: etapas `quality → test → build → deploy`.
- [x] Validar `docker compose --env-file deploy/.env.production.example -f deploy/docker-compose.prod.yml config`.
- [x] Confirmar que `api` no declara `ports` (`expose: 8000`) y que solo `web` publica `80:80` y `443:443`.
- [x] Ejecutar Ruff (`196` archivos) y pytest unitarias: **180 pruebas** (`179 passed`, `1 skipped` por Tcl/Tk) y cobertura **97.86 %**.
- [x] Auditar ausencia de secretos, IP privadas y claves en el diff.

## Fase 3 — Aprovisionamiento (bloqueado, requiere autorización)

- [!] Confirmar proveedor, región, tamaño y titularidad de la VPS.
- [!] Crear la VPS y registrar su IP fuera del repositorio.
- [!] Crear usuario `deploy`, instalar Docker Engine + Compose y añadir su clave pública.
- [!] Configurar firewall: 22/80/443 y política de denegación por defecto.
- [!] Configurar DNS del dominio/subdominio hacia la VPS.
- [!] Crear Deploy Token con `read_registry`.
- [!] Crear variables protegidas en GitLab (requiere rol Maintainer/Owner).
- [!] Configurar secreto `GITLAB_SYNC_TOKEN` en GitHub (requiere admin; alias admitido `GITLAB_TOKEN`).

## Fase 4 — Primer despliegue y verificación remota (pendiente)

- [ ] Ejecutar `deploy_vps` desde `develop` con variables completas.
- [ ] Confirmar emisión del certificado y arranque de Nginx.
- [ ] Verificar `GET /health` 200 por HTTPS y redirección desde HTTP.
- [ ] Verificar `/model-info`, `/docs` y `/predict` con imagen válida.
- [ ] Verificar que `http://<IP>:8000` no responde.
- [ ] Confirmar que el firewall solo expone 22/80/443.
- [ ] Confirmar que el tag desplegado coincide con `$CI_COMMIT_SHA`.
- [ ] Probar un push autorizado y verificar actualización visible.
- [ ] Documentar evidencia E2E y posibles regresiones en `docs/deployment-m4.md`.

## Evidencia local (adjunta en la PR)

- `glab ci lint`: CI/CD YAML válido; etapas `quality → test → build → deploy`.
- `docker compose config`: válido; `api.ports` vacío, `api.expose=8000`, `web` publica `80:80` y `443:443`.
- Ruff: `All checks passed!`; `196 files already formatted`.
- Pytest: `180` pruebas (`179 passed`, `1 skipped` por Tcl/Tk); cobertura `97.86 %`.
- Auditoría: sin tokens, claves SSH ni URLs con credenciales embebidas.
- Sin cambios en `src/`, `api/`, `ui/`, `tests/`, `Dockerfile`, Compose local ni Nginx local.

## Evidencia remota pendiente (no inventar)

- Workflow `Mirror to GitLab` en verde y SHA GitHub = SHA GitLab.
- Pipeline de GitLab (`89374502`) en verde con las cuatro etapas.
- Tag `<sha>` visible en el Container Registry.
- Job `deploy_vps` en verde y servicio actualizado en la VPS.
- `curl -I` de HTTP y HTTPS, JSON de `/health` y `/model-info`.
- Resultado de `/predict` con imagen válida y con archivo inválido.
- Confirmación de puerto 8000 cerrado desde una red externa.
