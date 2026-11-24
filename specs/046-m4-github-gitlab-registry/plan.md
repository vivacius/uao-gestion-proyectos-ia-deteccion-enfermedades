# Plan de Implementación (Spec Kit): SPEC-046 Integración GitHub–GitLab y Container Registry

**Identificador:** `SPEC-046`
**Feature Branch:** `feature/m4-github-gitlab-registry`
**Spec Técnica:** [spec.md](./spec.md)
**Tasks:** [tasks.md](./tasks.md)
**Fecha SDD (Prospectiva):** 2026-11-24

---

## 1. Estrategia y Enfoque

1. **Conservar GitHub como origen único.** No se reescribe historia en GitHub ni se introduce un segundo flujo de PRs. GitLab recibe un espejo de las ramas de integración y ejecuta CI/CD sobre el mismo commit.
2. **Espejo por GitHub Actions.** Un workflow dedicado hace checkout con historial y LFS, añade el remoto de GitLab con un token de proyecto y empuja la rama actual con `--force`. Si el secreto no existe, el workflow termina con advertencia explícita en lugar de un fallo silencioso.
3. **Endurecer el build existente.** Se preservan `lint`, `run_test`, `package_wheel` y `build_docker`; se añade descarga explícita de LFS, una comprobación de tamaño del modelo y etiquetas OCI. El tag pasa de SHA corto a SHA completo.
4. **Preparar el terreno para `SPEC-047`.** La etapa `deploy` se declara en este cambio, pero el job solo se activa cuando existan `DEPLOY_HOST` y las demás variables protegidas; así un push a `develop` no falla por infraestructura aún no aprovisionada.
5. **Documentar sin secretos.** El runbook lista nombres de variables, propietario requerido y comandos de verificación, nunca valores.

## 2. Arquitectura de Repositorios

```text
GitHub (fuente de verdad)
  vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades
        │  push a develop/main
        ▼
GitHub Actions: mirror-to-gitlab.yml
        │  git push --force (token de proyecto)
        ▼
GitLab (CI/CD + Registry)
  vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades
        │  quality → test → build → deploy
        ▼
registry.gitlab.com/vivacius/...:<sha-completo>
```

## 3. Cambios Previstos

| Archivo | Cambio |
| :--- | :--- |
| `.github/workflows/mirror-to-gitlab.yml` | Nuevo workflow de espejo con verificación de secreto, LFS y `workflow_dispatch`. |
| `.gitlab-ci.yml` | Etapa `deploy`; LFS explícito y validación de tamaño en `build_docker`; tags SHA completo + `latest`; etiquetas OCI. |
| `deploy/docker-compose.prod.yml` | Nuevo Compose de producción (API sin puerto publicado, Nginx TLS, certbot). |
| `deploy/nginx.prod.conf.template` | Nuevo proxy inverso TLS con redirección HTTP→HTTPS y *webroot* ACME. |
| `deploy/.env.production.example` | Plantilla sin secretos para el `.env` de la VPS. |
| `docs/deployment-m4.md` | Runbook de integración, Registry, variables, verificación y reversión. |
| `specs/046-.../` | Spec, plan y tareas prospectivas. |

**No se modifican:** `Dockerfile`, `docker-compose.yml` local, `deploy/nginx.conf` local, `src/`, `api/`, `ui/`, `tests/`, plantilla de PR ni Constitución.

## 4. Fases

1. **Fase 0 — Diagnóstico (completada):** verificar proyecto GitLab, rol, ramas, pipelines, Registry y ausencia de variables.
2. **Fase 1 — Artefactos locales:** crear workflow de espejo, extender `.gitlab-ci.yml`, añadir Compose/Nginx de producción y runbook.
3. **Fase 2 — Validación local:** parsear YAML, validar `docker compose config` con variables ficticias, ejecutar Ruff y pytest, revisar que no haya secretos.
4. **Fase 3 — Habilitación remota (requiere Owner):** crear `GITLAB_TOKEN`, elevarlo si se requiere, configurar variables protegidas y permitir el push del espejo a `main`.
5. **Fase 4 — Verificación remota:** push de prueba a `develop`, comparar SHAs, confirmar pipeline y tag en Registry.

## 5. Validación

| Comprobación | Comando | Criterio |
| :--- | :--- | :--- |
| YAML de GitLab | `python -c "import yaml; yaml.safe_load(open('.gitlab-ci.yml'))"` | Sin error |
| YAML del workflow | `python -c "import yaml; yaml.safe_load(open('.github/workflows/mirror-to-gitlab.yml'))"` | Sin error |
| Compose productivo | `docker compose -f deploy/docker-compose.prod.yml config` con `.env.production.example` | Sin error y sin puerto 8000 publicado |
| Calidad | `uv run ruff check .` / `uv run ruff format --check .` | Código 0 |
| Pruebas | `uv run pytest tests/unit --cov=src --cov=api` | ≥ 180 pruebas, cobertura ≥ 85 % |
| Secretos | búsqueda de patrones `glpat-`, `BEGIN OPENSSH`, `password=` | Sin coincidencias reales |

## 6. Riesgos y Mitigación

| Riesgo | Mitigación |
| :--- | :--- |
| `main` protegida rechaza el espejo. | Documentar y configurar la identidad del token como excepción, o espejar solo `develop` y promover `main` por MR. |
| El runner no descarga LFS y publica una imagen inválida. | `git lfs pull` + comprobación de tamaño antes de `docker build`. |
| Divergencia por pushes directos en GitLab. | Regla operativa: nadie pushea a GitLab; el espejo sobrescribe. |
| Token con permisos excesivos. | Token de proyecto con `write_repository` (y `read_registry` si aplica), caducidad corta y rotación documentada. |
| Fuga de secretos en logs. | Sin `set -x`; token por cabecera/URL enmascarada; variables marcadas como *masked*. |

## 7. Reversión

- Revertir el commit de la unidad restaura el `.gitlab-ci.yml` anterior y elimina el workflow.
- Desactivar el workflow desde GitHub Actions si el espejo causa divergencia.
- Las imágenes publicadas permanecen en el Registry; no se borran sin autorización.
