# Despliegue M4: GitHub → GitLab → VPS con HTTPS

**Unidades:** `SPEC-046` (sincronización canónica GitHub → GitLab, integrada en `develop` mediante PR #47) · `SPEC-047` (VPS, TLS y deploy)
**Issues M4:** #46 (sincronización) · #48 (CI/Registry/LFS) · #49 (VPS/firewall/TLS) · #50 (secretos) · #51 (E2E público) · #52 (gobernanza, fuera de alcance)
**Fecha:** 2026-11-25
**Estado:** artefactos locales implementados y validados localmente; **sincronización GitLab, pipeline oficial y despliegue VPS pendientes de validación**.

> Este documento no contiene tokens, claves, IPs privadas ni valores de variables. Solo nombres y procedimientos. Cualquier evidencia real se agrega al final, con fecha y responsable.

> **Trazabilidad y honestidad de estado:** esta PR no cierra las Issues #46, #48, #49, #50 ni #51; solo implementa los artefactos locales y deja explícito lo que falta validar en el proyecto GitLab oficial (`89374502`) y en la VPS. Un GitHub Actions en verde **no sustituye** la ejecución del pipeline de GitLab ni el despliegue público.

---

## 0. Alcance implementado y pendiente

| Componente | Issue | Estado en esta PR | Evidencia / pendiente |
| :--- | :--- | :--- | :--- |
| Sincronización unidireccional GitHub → GitLab, solo fast-forward y credenciales efímeras | #46 | Implementado localmente; **no verificado** | Workflow revisado; falta `GITLAB_SYNC_TOKEN` y una ejecución real |
| Pipeline `quality → test → build → deploy`, Git LFS y Registry por SHA | #48 | Implementado localmente; **no ejecutado en GitLab oficial** | `glab ci lint` válido; falta push a GitLab |
| Compose productivo, Nginx TLS y job `deploy_vps` | #49 | Implementado localmente; **no desplegado** | `docker compose config` válido; sin VPS ni dominio |
| Variables y secretos protegidos | #50 | Diseñado; **no configurado** | Solo se documentan nombres; no hay valores |
| Verificación E2E pública `/health`, `/predict` y HTTPS | #51 | **Pendiente** | Requiere VPS, DNS, TLS y ejecución real |
| Gobernanza, matriz y cierre Kanban | #52 | **Fuera de alcance** | Se gestiona en su Issue independiente |

---

## 1. Arquitectura

```text
GitHub (fuente de verdad)
  vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades
        │ push a develop/main
        ▼
GitHub Actions · .github/workflows/mirror-to-gitlab.yml
        │ git push fast-forward + LFS
        │ (credencial efímera, sin token en la URL)
        ▼
GitLab · vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades
        │ quality → test → build → deploy
        ▼
registry.gitlab.com/vivacius/...:<sha-completo>
        │ docker compose pull
        ▼
VPS · Nginx 80/443 → api:8000 (red interna) → FastAPI + DINOv2 CPU
```

**Regla:** nadie pushea directamente a GitLab. El espejo solo avanza `develop`/`main` si la rama de GitLab es ancestro del commit de GitHub; si hay divergencia, el workflow falla y exige intervención humana, sin reescribir el historial. Los PRs y la revisión humana siguen en GitHub.

**Política de liberación:** `develop` ejecuta `quality → test → build` y publica únicamente la imagen etiquetada por `CI_COMMIT_SHA` (sin sobrescribir `:latest` ni ejecutar `deploy_vps`). Únicamente `main` (`$CI_DEFAULT_BRANCH`), tras una PR aprobada, actualiza `:latest` y ejecuta `deploy_vps` automáticamente sobre producción con `IMAGE_TAG=${CI_COMMIT_SHA}`.

---

## 2. Estado verificado al 2026-11-25

| Elemento | Estado | Evidencia |
| :--- | :--- | :--- |
| Proyecto GitLab definitivo | Existe, público | `vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades`, ID 89374502 |
| Origen | Importado desde GitHub | `import_type: github`, `import_status: finished` |
| Rol de los 4 integrantes | Owner (50) | `GET /projects/:id/members/all` |
| `.gitlab-ci.yml` en `develop` | Base anterior a esta PR | `develop` = `589444f` al abrir la PR |
| PR #45 | Abierta; correcciones aplicadas; pendiente re-revisión | `gh pr view 45` |
| CI lint del archivo local | Válido | `glab ci lint` → `CI/CD YAML is valid` |
| Etapas del pipeline | `quality → test → build → deploy` | Parseo PyYAML de `stages` |
| `develop` en GitLab | `589444f` (sin el commit de esta PR) | API de ramas |
| `main` en GitLab | `a4e23dd` | API de ramas |
| Pipelines en GitLab | Ninguno ejecutado todavía | Falta sincronización o push autorizado |
| Pipeline de GitLab sobre esta PR | **No ejecutado** | Requiere `GITLAB_SYNC_TOKEN` o espejo autorizado |
| Registry del proyecto | Sin imágenes | API de Registry |
| Variables CI/CD | Vacías (accesibles) | API de variables |
| Secreto `GITLAB_SYNC_TOKEN` en GitHub | No existe | `gh secret list` |
| Permisos GitHub de la cuenta | `push`, sin `admin` | API de repo |
| VPS / dominio | **No aprovisionados** | Cuenta DigitalOcean sin droplets ni claves |

Conclusión: `SPEC-046` tiene la base lista (proyecto, rama y CI válido) pero **falta la primera ejecución real y el espejo automático**. `SPEC-047` está implementada y validada localmente, pero no verificada en VPS. No se declara cumplido `M4-01`, `M4-02`, `M4-05` ni `M4-07` hasta tener evidencia remota. La validación local y GitHub Actions no sustituyen el pipeline oficial de GitLab ni el despliegue público.

### 2.1 Validación local de esta PR (2026-11-25)

| Comprobación | Resultado |
| :--- | :--- |
| `glab ci lint` | Válido |
| Etapas del pipeline | `quality → test → build → deploy` |
| Ruff | `All checks passed!`; `196 files already formatted` |
| Pytest unitario | **180 pruebas** (`179 passed`, `1 skipped` por Tcl/Tk); cobertura **97.86 %** |
| `docker compose config` | Válido; `api` sin `ports`, `web` publica `80:80` y `443:443` |
| Archivos M1–M3 | Sin cambios en `src/`, `api/`, `ui/`, `tests/`, `Dockerfile`, Compose local ni Nginx local |
| Credenciales | Sin tokens, claves SSH ni URLs con credenciales embebidas |

---

## 3. Prerrequisitos y responsables

| Prerrequisito | Responsable | Dónde |
| :--- | :--- | :--- |
| Crear secreto `GITLAB_SYNC_TOKEN` (alias admitido: `GITLAB_TOKEN`) | Administrador del repo GitHub (`vivacius`) | GitHub → Settings → Secrets and variables → Actions |
| Crear variables protegidas de deploy | Cualquier Owner de GitLab | GitLab → Settings → CI/CD → Variables |
| Crear Deploy Token `read_registry` | Cualquier Owner de GitLab | GitLab → Settings → Repository → Deploy tokens |
| Autorizar push del espejo a `main` | Owner de GitLab | Settings → Repository → Protected branches |
| Aprovisionar VPS y DNS | Responsable autorizado del equipo | Proveedor cloud + DNS |
| Autorizar apertura de 80/443 | Responsable del equipo | VPS |

### 3.1 Estado de permisos

- **GitLab:** los cuatro integrantes son Owner, por lo que variables, Deploy Tokens, ramas protegidas y ajustes de CI están disponibles.
- **GitHub:** la cuenta actual tiene `push` pero **no `admin`**, así que el secreto `GITLAB_SYNC_TOKEN` debe crearlo el propietario del repositorio.
- **Infraestructura:** no hay VPS ni dominio; cualquier aprovisionamiento requiere autorización y costo.

Alternativas para la sincronización automática, en orden de preferencia:

1. **Pull mirroring de GitLab** (si el plan lo permite): el proyecto jala de GitHub cada pocos minutos.
2. **Push desde GitHub Actions** con `GITLAB_SYNC_TOKEN` (requiere admin de GitHub).
3. **Pipeline programado en GitLab** que hace `git fetch` del repo público de GitHub y actualiza `develop`/`main`; no requiere permisos de GitHub, pero la latencia depende del intervalo del schedule.

---

## 4. Configuración del espejo GitHub → GitLab

1. Crear en GitLab un **Project Access Token** con scope `write_repository` y caducidad corta. Guardar el valor una sola vez.
2. En GitHub, crear el secreto `GITLAB_SYNC_TOKEN` con ese valor (canónico, alineado con `SPEC-046`). El workflow también acepta `GITLAB_TOKEN` como alias de compatibilidad; basta con configurar uno.
3. Verificar que el workflow `Mirror to GitLab` aparece en Actions.
4. Si `main` está protegida en GitLab, permitir que la identidad del token haga push (Protected branches → Allowed to push). Si no se permite, el espejo de `main` fallará de forma visible; `develop` seguirá funcionando.
5. El workflow no escribe el token en la URL del remoto ni en `.git/config`: usa un `GIT_ASKPASS` efímero en `$RUNNER_TEMP`, `GIT_TERMINAL_PROMPT=0` y un `credential.helper` vacío durante la ejecución. El archivo temporal se elimina al finalizar.
6. Si falta el secreto, el job falla con un mensaje explícito (`Espejo no configurado`); no simula una sincronización exitosa.
7. El push es estrictamente **fast-forward**. Si la rama de GitLab divergió, el job detecta la condición, falla y no reescribe el historial.

**Verificación:**

```bash
git rev-parse origin/develop                 # GitHub
glab api projects/vivacius%2Fuao-gestion-proyectos-ia-deteccion-enfermedades/repository/branches/develop
```

Ambos SHAs deben coincidir. El pipeline de GitLab debe aparecer sobre ese SHA.

---

## 5. Variables de GitLab (solo nombres)

| Variable | Protegida | Enmascarada | Contenido |
| :--- | :---: | :---: | :--- |
| `DEPLOY_HOST` | Sí | No | IP o hostname de la VPS |
| `DEPLOY_USER` | Sí | No | Usuario SSH de despliegue |
| `DEPLOY_PATH` | Sí | No | Directorio remoto, por ejemplo `/opt/agroscan` |
| `SSH_PRIVATE_KEY` | Sí | Sí | Clave privada dedicada, sin passphrase |
| `SSH_KNOWN_HOSTS` | Sí | No | Línea de `known_hosts` del host |
| `PUBLIC_HOST` | Sí | No | Dominio público, sin `https://` |
| `LETSENCRYPT_EMAIL` | Sí | No | Correo de contacto Let's Encrypt |
| `DEPLOY_TOKEN_USER` | Sí | No | Usuario del Deploy Token |
| `DEPLOY_TOKEN` | Sí | Sí | Token con `read_registry` |

Sin `DEPLOY_HOST`, el job `deploy_vps` no se crea: el pipeline queda en `quality` + `test` + `build` y no falla por infraestructura pendiente.

---

## 6. Aprovisionamiento de la VPS

> Ejecutar solo con autorización. Los comandos son orientativos para Ubuntu 24.04; adaptar al proveedor.

1. Crear la instancia (2 vCPU, 4 GB RAM recomendado para CPU + modelo + Nginx).
2. Crear usuario de despliegue y añadir su clave pública:

```bash
adduser deploy
usermod -aG sudo deploy
install -d -m 700 -o deploy -g deploy /home/deploy/.ssh
# Pegar la clave publica en /home/deploy/.ssh/authorized_keys con permisos 600
```

3. Instalar Docker Engine y Compose (repositorio oficial de Docker), añadir `deploy` al grupo `docker`.
4. Firewall:

```bash
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable
ufw status
```

5. DNS: registro `A` (y `AAAA` si aplica) del dominio hacia la IP. Verificar con `dig +short <dominio>`.
6. Crear el directorio de despliegue: `/opt/agroscan`.

**No** se debe abrir `8000/tcp`: la API solo escucha en la red interna de Docker.

---

## 7. Emisión de TLS y primer despliegue

El job `deploy_vps`:

1. Copia `docker-compose.prod.yml` y `nginx.prod.conf.template` a `DEPLOY_PATH`.
2. Genera un `.env` con `REGISTRY_IMAGE`, `IMAGE_TAG` (SHA completo) y `DOMAIN`.
3. Hace login al Registry con el Deploy Token.
4. Si no existe `certbot/conf/live/<dominio>/fullchain.pem`, ejecuta:

```bash
docker run --rm -p 80:80 \
  -v "$DEPLOY_PATH/certbot/conf:/etc/letsencrypt" \
  certbot/certbot certonly --standalone --non-interactive --agree-tos \
  --email "$LETSENCRYPT_EMAIL" -d "$PUBLIC_HOST"
```

5. `docker compose pull` y `docker compose up -d --remove-orphans`.
6. Verifica `https://<dominio>/health`.

Renovación: el contenedor `certbot` ejecuta `certbot renew --webroot` cada 12 h. Programar en el host una recarga de Nginx:

```bash
# crontab -e (usuario deploy)
0 3 * * * cd /opt/agroscan && docker compose exec -T web nginx -s reload
```

---

## 8. Verificación E2E

```bash
# Redireccion y TLS
curl -I http://<dominio>/health
curl -I https://<dominio>/health

# Endpoints
curl -fsS https://<dominio>/health
curl -fsS https://<dominio>/model-info
curl -fsS -o /dev/null -w "%{http_code}\n" https://<dominio>/docs

# Prediccion valida
curl -fsS -F "file=@hoja.jpg" https://<dominio>/predict

# Errores controlados
curl -s -o /dev/null -w "%{http_code}\n" -F "file=@archivo.bin" https://<dominio>/predict   # 415
curl -s -o /dev/null -w "%{http_code}\n" -F "file=@corrupto.jpg" https://<dominio>/predict  # 400

# Backend no expuesto
curl --connect-timeout 5 http://<IP>:8000/health   # debe fallar
```

Registrar: fecha, commit, salida de `/health`, código de `/predict`, resultado de `curl` a 8000 y captura del job.

---

## 9. Reversión

```bash
cd /opt/agroscan
sed -i 's/^IMAGE_TAG=.*/IMAGE_TAG=<sha-anterior-verificado>/' .env
docker compose pull
docker compose up -d --remove-orphans
curl -fsS https://<dominio>/health
```

Actualizar `.env` persiste el SHA revertido ante futuros `docker compose up -d`. No borrar `certbot/conf` ni `certbot/www` durante una reversión. Si el fallo es de configuración, restaurar el `docker-compose.yml` y la plantilla Nginx del commit anterior.

---

## 10. Diagnóstico rápido

| Síntoma | Causa probable | Acción |
| :--- | :--- | :--- |
| `deploy_vps` no aparece | `DEPLOY_HOST` ausente o no protegida | Crear variable protegida y repetir pipeline |
| Error de host key | `SSH_KNOWN_HOSTS` desactualizado | Regenerar huella y actualizar variable |
| Nginx reinicia en bucle | Certificado ausente o ruta incorrecta | Revisar `certbot/conf/live/<dominio>` y logs |
| `docker pull` 401 | Deploy Token sin `read_registry` | Rotar token y actualizar variables |
| `/health` 502 | API aún cargando el modelo | Esperar `start_period` de 60 s y revisar logs |
| HTTPS inválido | DNS no propagado o cert de otro dominio | Verificar `dig` y `certbot certificates` |

---

## 11. Evidencia de cierre (completar solo con resultados reales)

| Evidencia | Resultado | Fecha | Responsable |
| :--- | :--- | :--- | :--- |
| GitHub Actions Quality Gate en verde | Verificado (`Quality Gate CI (M3)` en verde sobre `develop`) | 2026-11-26 | `@josesilvacalderon111` |
| Workflow `Mirror to GitLab` en verde | Verificado (`#45748907446`, `#45749582913` y sincronización en `develop` protegida) | 2026-11-26 | `@JhonatanTC99` / `@josesilvacalderon111` |
| SHA GitHub = SHA GitLab | Verificado (`develop` sincronizado a `33ff9a2caf8220bd5e3b0fee60c77a7066c4219c`) | 2026-11-26 | `@josesilvacalderon111` |
| Pipeline GitLab `quality → test → build → deploy` en verde | Verificado en proyecto oficial `89374502` (4 etapas en `success`) | 2026-11-26 | `@josesilvacalderon111` |
| Tag `<sha>` en Registry | Verificado (`registry.gitlab.com/...:33ff9a2caf8220bd5e3b0fee60c77a7066c4219c` y `latest`) | 2026-11-26 | `@josesilvacalderon111` |
| Job `deploy_vps` en verde | Verificado en VPS DigitalOcean (Ubuntu 24.04 LTS, Docker `29.10.1`, Compose `v5.8.0`, TLS Let's Encrypt) | 2026-11-26 | `@josesilvacalderon111` |
| `GET /health` 200 por HTTPS | Verificado (`HTTP/1.1 200 OK` en `https://agroscan-uao.duckdns.org/health`, `301` desde HTTP, HSTS y cabeceras de seguridad) | 2026-11-26 | `@josesilvacalderon111` |
| `POST /predict` 200 con imagen válida | Verificado (`HTTP/1.1 200 OK`, Top-3 en español, descargo agronómico, `175.42 ms` en CPU; corrupto `400`, `.bin` `415`) | 2026-11-26 | `@josesilvacalderon111` |
| Puerto 8000 cerrado desde Internet | Verificado (`ufw status` solo `22/80/443`; `curl --connect-timeout 5 http://<IP_REDACTADA>:8000/health` → `Connection timed out`) | 2026-11-26 | `@josesilvacalderon111` |
| Push autorizado actualiza el servicio | Verificado tras promoción `develop → main` (`PR #67`, `PR #69` / `Mirror to GitLab` + `deploy_vps` en verde) | 2026-11-26 | `@josesilvacalderon111` / `@JhonatanTC99` |

### 11.1 Evidencia E2E pública HTTPS verificada (`2026-11-26`, commit `33ff9a2c`)

- **URL pública:** `https://agroscan-uao.duckdns.org` (DNS → VPS DigitalOcean `x86_64`, 2 GB RAM + 2 GB swap, Docker `29.10.1`, Compose `v5.8.0`).
- **Firewall (`ufw status`):** `Status: active` — únicamente `22/tcp`, `80/tcp`, `443/tcp` en `ALLOW`; política entrante por defecto `deny`.
- **Redirección y TLS:**
  - `curl -I http://agroscan-uao.duckdns.org/health` → `HTTP/1.1 301 Moved Permanently` hacia `https://agroscan-uao.duckdns.org/health`.
  - `curl -i https://agroscan-uao.duckdns.org/health` → `HTTP/1.1 200 OK` con certificado Let's Encrypt válido y cabeceras `Strict-Transport-Security`, `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, `Referrer-Policy`.
- **Endpoints verificados:**
  - `GET /` (UI web desacoplada): `HTTP 200`.
  - `GET /docs` (OpenAPI/Swagger): `HTTP 200`.
  - `GET /health`: `HTTP 200` (`status: ok`, `model_available: true`, `device: cpu`, `num_classes: 38`).
  - `GET /model-info`: `HTTP 200` (`rodynaemad/plant-disease-dinov2-small`).
  - `POST /predict` (JPG válida): `HTTP 200`, Top-3 en español, descargo agronómico no prescriptivo, `inference_time_ms: 175.42`.
  - `POST /predict` (JPG corrupta): `HTTP 400 Bad Request` (`CorruptedImageError`).
  - `POST /predict` (archivo `.bin`): `HTTP 415 Unsupported Media Type` (`UnsupportedImageFormatError`).
- **Aislamiento de red:** `curl --connect-timeout 5 http://<IP_REDACTADA>:8000/health` → `curl: (28) Connection timed out after 5003 milliseconds`.

> **No sustitución de evidencias:** un run verde de GitHub Actions no acredita la sincronización, el pipeline de GitLab ni el despliegue. Las filas de esta tabla solo se completan con salida real del proyecto GitLab oficial y de la VPS.
