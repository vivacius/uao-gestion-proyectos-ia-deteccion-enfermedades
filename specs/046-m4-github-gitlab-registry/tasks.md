# Tareas (Spec Kit): SPEC-046 Integración GitHub–GitLab y Container Registry

**Feature Branch:** `feature/m4-github-gitlab-registry` | **Spec:** [spec.md](./spec.md) | **Plan:** [plan.md](./plan.md) | **Estado global:** Lista para PR; verificación remota pendiente

> Convención: `[x]` solo con evidencia directa. `[ ]` pendiente. `[!]` bloqueado por permisos, infraestructura o decisión humana.

## Fase 0 — Diagnóstico

- [x] Verificar que el proyecto definitivo es `vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades` (ID 89374502, público).
- [x] Confirmar que los cuatro integrantes tienen rol Owner (50) en GitLab.
- [x] Confirmar que `develop` de GitLab y GitHub están en `589444f`, y `main` de GitLab en `a4e23dd`.
- [x] Confirmar `.gitlab-ci.yml` presente en `develop`, sin pipelines ni imágenes aún en Registry.
- [x] Confirmar variables CI/CD accesibles y vacías.
- [x] Confirmar que GitHub no permite crear secretos con la cuenta actual (permiso `admin: false`).

## Fase 1 — Artefactos locales

- [x] Crear `.github/workflows/mirror-to-gitlab.yml`.
- [x] Extender `.gitlab-ci.yml` con etapas `quality → test → build → deploy`, LFS explícito, validación de tamaño del modelo y tags OCI.
- [x] Crear `deploy/docker-compose.prod.yml`.
- [x] Crear `deploy/nginx.prod.conf.template`.
- [x] Crear `deploy/.env.production.example`.
- [x] Crear `docs/deployment-m4.md` con runbook y tabla de variables (solo nombres).
- [x] Confirmar que no se modificaron `Dockerfile`, Compose local, Nginx local, `src/`, `api/`, `ui/`, `tests/` ni la plantilla de PR.

## Fase 2 — Validación local

- [x] Parsear `.gitlab-ci.yml`, workflow y Compose con PyYAML.
- [x] Validar `.gitlab-ci.yml` con `glab ci lint` contra el proyecto definitivo.
- [x] Validar contrato de etapas: `lint`/quality, `run_test`/test, `package_wheel` + `build_docker`/build, `deploy_vps`/deploy.
- [x] Validar `docker compose -f deploy/docker-compose.prod.yml config` con `.env.production.example`; `api` no publica puertos y `web` publica 80/443.
- [x] Ejecutar calidad local: Ruff OK; `pytest tests/unit` = 180 passed, cobertura 98 %; integración = 6 passed.
- [x] Auditar ausencia de secretos y retirar artefactos TLS temporales de validación.

## Fase 3 — Habilitación remota (bloqueada)

- [!] Crear `GITLAB_TOKEN` como secreto en GitHub (requiere administrador del repo GitHub).
- [!] Crear variables protegidas de despliegue en GitLab cuando existan VPS, dominio y clave SSH.
- [!] Autorizar la identidad del token para push a `main` protegida, o acordar espejo solo de `develop`.
- [ ] Crear rama, commit y PR hacia `develop` (autorizado; en curso).

## Fase 4 — Verificación remota

- [ ] Confirmar workflow `Mirror to GitLab` en verde tras configurar `GITLAB_TOKEN`.
- [ ] Comparar el SHA de `develop` en GitHub y GitLab después de un push autorizado.
- [ ] Confirmar pipeline de GitLab en verde sobre ese SHA.
- [ ] Confirmar tag `$CI_COMMIT_SHA` y `latest` en el Container Registry.
- [ ] Confirmar que la imagen contiene `model.safetensors` real (> 1 MB) y que `/health` responde 200 al ejecutarla.

## Evidencia a adjuntar en la PR

- Salida de `glab ci lint` y del contrato de cuatro etapas.
- Salida de Ruff y pytest previamente verificada.
- Captura o JSON de `GET /projects/:id/pipelines` y `GET /projects/:id/registry/repositories/:id/tags` cuando exista ejecución remota.
- Confirmación de que no hay secretos, claves ni binarios temporales en el diff.
