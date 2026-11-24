# Plan de Implementación (Spec Kit): SPEC-047 VPS, Seguridad, HTTPS y Despliegue Continuo

**Identificador:** `SPEC-047`
**Feature Branch:** `feature/m4-vps-https-deploy`
**Spec Técnica:** [spec.md](./spec.md)
**Tasks:** [tasks.md](./tasks.md)
**Fecha SDD (Prospectiva):** 2026-11-24

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
  → espejo → GitLab pipeline
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
| `GITLAB_TOKEN` | GitHub Secrets | — | — | Token con `write_repository` para el espejo |

> Ningún valor se versiona. La tabla anterior es la única referencia admitida en documentación.

## 5. Cambios Previstos

| Archivo | Cambio |
| :--- | :--- |
| `deploy/docker-compose.prod.yml` | Nuevo: API sin puerto público, Nginx TLS, certbot y red interna. |
| `deploy/nginx.prod.conf.template` | Nuevo: redirección 80→443, TLS, proxy a `api:8000`, ACME webroot. |
| `deploy/.env.production.example` | Nuevo: variables no secretas de ejemplo. |
| `.gitlab-ci.yml` | Nuevo stage `deploy` y job `deploy_vps` con reglas por disponibilidad de variables. |
| `docs/deployment-m4.md` | Nuevo: runbook de VPS, DNS, TLS, variables, verificación y reversión. |
| `specs/047-.../` | Spec, plan y tareas prospectivas. |

## 6. Procedimiento Operativo (resumen)

1. **VPS:** crear usuario `deploy`, instalar Docker Engine + Compose, añadir su clave pública, desactivar login root por contraseña.
2. **Firewall:** permitir `22/tcp`, `80/tcp`, `443/tcp`; denegar el resto por defecto.
3. **DNS:** registro A del dominio hacia la IP de la VPS; verificar propagación.
4. **Deploy Token:** crear token de proyecto con `read_registry`; guardar usuario y token como variables protegidas.
5. **Clave SSH:** generar par dedicado, guardar la privada como `SSH_PRIVATE_KEY` y la huella como `SSH_KNOWN_HOSTS`.
6. **Primer despliegue:** ejecutar el job; si no hay certificado, el script lo emite con `--standalone` antes de levantar Nginx.
7. **Verificación:** `GET /health` 200 por HTTPS, `/predict` con imagen válida, `http://IP:8000` cerrado.
8. **Renovación:** el contenedor `certbot` renueva cada 12 h; un cron del host recarga Nginx (`docker compose exec -T web nginx -s reload`).

## 7. Validación Local

| Comprobación | Comando | Criterio |
| :--- | :--- | :--- |
| Sintaxis YAML | Parseo con PyYAML | Sin error |
| Compose | `docker compose -f deploy/docker-compose.prod.yml config` | Sin error; `api` sin `ports` |
| Calidad | `uv run ruff check .` / `ruff format --check .` | Código 0 |
| Pruebas | `uv run pytest tests/unit --cov=src --cov=api` | ≥ 180 pruebas, cobertura ≥ 85 % |
| Secretos | Búsqueda de `glpat-`, `BEGIN OPENSSH`, `password=` | Sin valores reales |
| Nginx | Revisión de `nginx -t` en contenedor (si Docker está disponible) | Sintaxis válida |

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
