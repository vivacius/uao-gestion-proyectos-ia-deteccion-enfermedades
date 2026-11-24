# Tareas (Spec Kit): SPEC-047 VPS, Seguridad, HTTPS y Despliegue Continuo

**Feature Branch:** `feature/m4-vps-https-deploy` | **Spec:** [spec.md](./spec.md) | **Plan:** [plan.md](./plan.md) | **Estado global:** Implementación local, sin aprovisionamiento ni despliegue

> Convención: `[x]` solo con evidencia directa. `[ ]` pendiente. `[!]` bloqueado por permisos, credenciales o decisión humana.

## Fase 1 — Artefactos locales

- [ ] Crear `deploy/docker-compose.prod.yml` con `api` sin `ports`, `web` 80/443 y `certbot`.
- [ ] Crear `deploy/nginx.prod.conf.template` con redirección, TLS, HSTS, ACME y proxy a `api:8000`.
- [ ] Crear `deploy/.env.production.example` sin secretos.
- [ ] Añadir `deploy` a `stages` y el job `deploy_vps` en `.gitlab-ci.yml`.
- [ ] Documentar variables, bootstrap TLS, firewall y reversión en `docs/deployment-m4.md`.
- [ ] Verificar que el Compose local y el Nginx local no cambiaron.

## Fase 2 — Validación local

- [ ] Parsear `.gitlab-ci.yml` con PyYAML.
- [ ] Validar `docker compose -f deploy/docker-compose.prod.yml config` con `.env.production.example`.
- [ ] Confirmar que `api` no declara `ports` y que solo `web` publica 80/443.
- [ ] Ejecutar Ruff y pytest unitarias; registrar resultados.
- [ ] Auditar ausencia de secretos, IP privadas y claves en el diff.

## Fase 3 — Aprovisionamiento (bloqueado, requiere autorización)

- [!] Confirmar proveedor, región, tamaño y titularidad de la VPS.
- [!] Crear la VPS y registrar su IP fuera del repositorio.
- [!] Crear usuario `deploy`, instalar Docker Engine + Compose y añadir su clave pública.
- [!] Configurar firewall: 22/80/443 y política de denegación por defecto.
- [!] Configurar DNS del dominio/subdominio hacia la VPS.
- [!] Crear Deploy Token con `read_registry`.
- [!] Crear variables protegidas en GitLab (requiere rol Maintainer/Owner).
- [!] Configurar secreto `GITLAB_TOKEN` en GitHub (requiere admin).

## Fase 4 — Primer despliegue y verificación

- [ ] Ejecutar `deploy_vps` desde `develop` con variables completas.
- [ ] Confirmar emisión del certificado y arranque de Nginx.
- [ ] Verificar `GET /health` 200 por HTTPS y redirección desde HTTP.
- [ ] Verificar `/model-info`, `/docs` y `/predict` con imagen válida.
- [ ] Verificar que `http://<IP>:8000` no responde.
- [ ] Confirmar que el firewall solo expone 22/80/443.
- [ ] Confirmar que el tag desplegado coincide con `$CI_COMMIT_SHA`.
- [ ] Probar un push autorizado y verificar actualización visible.
- [ ] Documentar evidencia E2E y posibles regresiones en `docs/deployment-m4.md`.

## Evidencia a adjuntar en la PR

- Salida de `docker compose config` sin secretos.
- `curl -I` de HTTP y HTTPS.
- JSON de `/health` y `/model-info`.
- Resultado de `/predict` con imagen válida y con archivo inválido.
- Captura del job `deploy_vps` en verde y del tag en el Registry.
- Confirmación de puerto 8000 cerrado desde una red externa.
