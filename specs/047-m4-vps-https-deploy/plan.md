# Plan de Implementación (Spec Kit): SPEC-047 VPS, Seguridad, HTTPS y Despliegue Continuo

**Identificador:** `SPEC-047`
**Feature Branch:** `feature/m4-gitlab-registry-deploy`
**Issues Relacionadas:** #46 (sincronización canónica) · #48 (CI/Registry/LFS) · #49 (VPS/firewall/TLS) · #50 (secretos) · #51 (E2E público) · #52 (gobernanza, fuera de alcance)
**Spec Técnica:** [spec.md](./spec.md)
**Tasks:** [tasks.md](./tasks.md)
**Fecha SDD (Prospectiva):** 2026-11-24
**Estado:** Implementado y validado localmente; pendiente de validación en GitLab oficial y VPS

---

## 1. Estrategia

1. **Separar producción de desarrollo.** Se crea un Compose y un Nginx exclusivos para la VPS; los artefactos locales de M3 quedan intactos.
2. **Cerrar la superficie de red.** La API no publica puertos; Nginx es el único punto de entrada y termina TLS.
3. **Automatizar el ciclo completo sin secretos en Git.** El job `deploy` se activa solo cuando existen las variables protegidas; usa un Deploy Token de solo lectura para el Registry y una clave SSH dedicada.
4. **Emitir TLS de forma reproducible.** El primer certificado se obtiene con `certbot --standalone`; los siguientes ciclos renuevan con `--webroot` y Nginx sirve el desafío ACME.
5. **Verificar desde fuera.** El job comprueba `/health` por HTTPS público; la validación de `/predict` se hace con una imagen de prueba en la fase de evidencias.

## 2. Flujo de Despliegue

```text
push a develop (GitHub)
  → espejo fast-forward (GIT_ASKPASS efímero, sin token en la URL)
  → GitLab pipeline
    → quality (Ruff)
      → test (pytest + cobertura)
        → build (wheel + image :$CI_COMMIT_SHA)
        → deploy_vps (solo si DEPLOY_HOST existe)
          → SSH a VPS
            → docker login registry (Deploy Token)
            → docker compose pull
            → docker compose up -d
            → curl https://$PUBLIC_HOST/health
```

## 3. Responsabilidades y Topología

| Componente | Puerto | Red | Persistencia |
| :--- | :--- | :--- | :--- |
| `api` (imagen del Registry) | `expose 8000` | `internal` | Ninguna; modelo dentro de la imagen |
| `web` (Nginx TLS) | `80`, `443` | `internal` | `./certbot/conf`, `./certbot/www` |
| `certbot` | — | `internal` | `./certbot/conf`, `./certbot/www` |

## 4. Variables Requeridas (solo nombres)

| Variable | Ámbito | Protegida | Enmascarada | Uso |
| :--- | :--- | :--- | :--- | :--- |
| `DEPLOY_HOST` | GitLab CI/CD | Sí | No | IP o hostname de la VPS |
| `DEPLOY_USER` | GitLab CI/CD | Sí | No | Usuario SSH de despliegue |
| `DEPLOY_PATH` | GitLab CI/CD | Sí | No | Directorio remoto (p. ej. `/opt/agroscan`) |
| `SSH_PRIVATE_KEY` | GitLab CI/CD | Sí | Sí | Clave dedicada sin passphrase |
| `SSH_KNOWN_HOSTS` | GitLab CI/CD | Sí | No | Huella del host para evitar MITM |
| `PUBLIC_HOST` | GitLab CI/CD | Sí | No | Dominio público (sin esquema) |
| `LETSENCRYPT_EMAIL` | GitLab CI/CD | Sí | No | Contacto para Let's Encrypt |
| `DEPLOY_TOKEN_USER` | GitLab CI/CD | Sí | No | Usuario del Deploy Token |
| `DEPLOY_TOKEN` | GitLab CI/CD | Sí | Sí | Token con `read_registry` |
| `GITLAB_SYNC_TOKEN` | GitHub Secrets | — | — | Token con `write_repository` para el espejo (canónico, `SPEC-046`) |

> Ningún valor se versiona. La tabla anterior es la única referencia admitida en documentación. El workflow acepta `GITLAB_TOKEN` como alias de compatibilidad, pero la documentación y `SPEC-046` usan `GITLAB_SYNC_TOKEN`.

## 5. Cambios Implementados

| Archivo | Cambio | Estado |
| :--- | :--- | :--- |
| `deploy/docker-compose.prod.yml` | API sin puerto público, Nginx TLS, certbot y red interna. | Implementado localmente |
| `deploy/nginx.prod.conf.template` | Redirección 80→443, TLS, proxy a `api:8000`, ACME webroot. | Implementado localmente |
| `deploy/.env.production.example` | Variables no secretas de ejemplo. | Implementado localmente |
| `.gitlab-ci.yml` | Stage `deploy` y job `deploy_vps` con reglas por disponibilidad de variables. | Implementado localmente; no ejecutado en GitLab |
| `docs/deployment-m4.md` | Runbook de VPS, DNS, TLS, variables, verificación y reversión. | Implementado localmente |
| `specs/047-.../` | Spec, plan y tareas prospectivas. | Implementado localmente |
| `.github/workflows/mirror-to-gitlab.yml` | Espejo unidireccional fast-forward con credencial efímera. | Implementado localmente; no verificado |

## 6. Procedimiento Operativo (resumen)

1. **VPS:** crear usuario `deploy`, instalar Docker Engine + Compose, añadir su clave pública, desactivar login root por contraseña.
2. **Firewall:** permitir `22/tcp`, `80/tcp`, `443/tcp`; denegar el resto por defecto.
3. **DNS:** registro A del dominio hacia la IP de la VPS; verificar propagación.
4. **Deploy Token:** crear token de proyecto con `read_registry`; guardar usuario y token como variables protegidas.
5. **Clave SSH:** generar par dedicado, guardar la privada como `SSH_PRIVATE_KEY` y la huella como `SSH_KNOWN_HOSTS`.
6. **Primer despliegue:** ejecutar el job; si no hay certificado, el script lo emite con `--standalone` antes de levantar Nginx.
7. **Verificación:** `GET /health` 200 por HTTPS, `/predict` con imagen válida, `http://IP:8000` cerrado.
8. **Renovación:** el contenedor `certbot` renueva cada 12 h; un cron del host recarga Nginx (`docker compose exec -T web nginx -s reload`).

## 7. Validación Local Ejecutada (2026-11-25)

| Comprobación | Comando | Resultado |
| :--- | :--- | :--- |
| Sintaxis YAML y etapas | Parseo con PyYAML + `glab ci lint` | Válido; `quality → test → build → deploy` |
| Compose | `docker compose --env-file deploy/.env.production.example -f deploy/docker-compose.prod.yml config` | Válido; `api.ports` vacío, `api.expose=8000`, `web` publica `80:80` y `443:443` |
| Calidad | `uv run --no-sync ruff check .` / `ruff format --check .` | `All checks passed!`; `196 files already formatted` |
| Pruebas | `uv run --no-sync pytest tests/unit --cov=src --cov=api --cov-fail-under=85` | **180 pruebas** (`179 passed`, `1 skipped` por Tcl/Tk); cobertura **97.86 %** |
| Secretos | Búsqueda de `glpat-`, `BEGIN OPENSSH`, `password=` y credenciales en URLs | Sin valores reales |
| Nginx | Revisión de plantilla y `docker compose config` | Sintaxis y variables consistentes; `nginx -t` en VPS queda pendiente |

### 7.1 Validación remota pendiente

| Comprobación | Estado | Motivo |
| :--- | :--- | :--- |
| Espejo GitHub → GitLab | Pendiente | Falta `GITLAB_SYNC_TOKEN` y una ejecución real |
| Pipeline GitLab `quality → test → build → deploy` | Pendiente | No se ha ejecutado en el proyecto oficial `89374502` |
| Tag de imagen en Registry | Pendiente | Depende del pipeline de GitLab |
| VPS, DNS, TLS y `deploy_vps` | Pendiente | Infraestructura no aprovisionada |
| E2E público `/health` y `/predict` | Pendiente | Depende del despliegue |

> La validación local y cualquier run de GitHub Actions no sustituyen estas comprobaciones remotas.

## 8. Riesgos y Mitigación

| Riesgo | Mitigación |
| :--- | :--- |
| Certificado no emitido y Nginx no arranca. | Bootstrap con `--standalone` antes de `compose up`; mensaje de error explícito. |
| Renovación sin recarga. | Cron documentado + verificación de fecha de expiración. |
| Clave SSH comprometida. | Clave dedicada, rotación, usuario sin sudo amplio y firewall restrictivo. |
| Deploy concurrente. | `resource_group: production`. |
| Push a `develop` sin variables. | El job no se crea si `DEPLOY_HOST` está vacío; el pipeline sigue en verde. |
| Regresión funcional. | Reversión por `IMAGE_TAG` anterior y healthcheck previo. |
| Exposición de IP/dominio en el repo. | El dominio puede documentarse; la IP y credenciales no. |

## 9. Reversión

1. Identificar el SHA/tag anterior verificado.
2. En la VPS: `IMAGE_TAG=<sha-anterior> docker compose up -d --remove-orphans`.
3. Confirmar `/health` 200 y funcionalidad de `/predict`.
4. Si el fallo es de configuración, restaurar el `docker-compose.yml`/plantilla Nginx del commit anterior.
5. No revocar certificados ni borrar volúmenes de certbot durante una reversión.
