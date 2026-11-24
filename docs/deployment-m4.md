# Despliegue M4: GitHub → GitLab → VPS con HTTPS

**Unidades:** `SPEC-046` (integración y Registry) · `SPEC-047` (VPS, TLS y deploy)
**Fecha:** 2026-11-24
**Estado:** artefactos locales listos para PR; **sin aprovisionamiento ni despliegue verificado**.

> Este documento no contiene tokens, claves, IPs privadas ni valores de variables. Solo nombres y procedimientos. Cualquier evidencia real se agrega al final, con fecha y responsable.

---

## 1. Arquitectura

```text
GitHub (fuente de verdad)
  vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades
        │ push a develop/main
        ▼
GitHub Actions · .github/workflows/mirror-to-gitlab.yml
        │ git push --force + LFS
        ▼
GitLab · vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades
        │ quality → test → build → deploy
        ▼
registry.gitlab.com/vivacius/...:<sha-completo>
        │ docker compose pull
        ▼
VPS · Nginx 80/443 → api:8000 (red interna) → FastAPI + DINOv2 CPU
```

**Regla:** nadie pushea directamente a GitLab. El espejo sobrescribe `develop`/`main` desde GitHub. Los PRs y la revisión humana siguen en GitHub.

---

## 2. Estado verificado al 2026-11-24

| Elemento | Estado | Evidencia |
| :--- | :--- | :--- |
| Proyecto GitLab definitivo | Existe, público | `vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades`, ID 89374502 |
| Origen | Importado desde GitHub | `import_type: github`, `import_status: finished` |
| Rol de los 4 integrantes | Owner (50) | `GET /projects/:id/members/all` |
| `.gitlab-ci.yml` en `develop` | Presente | `develop` = `589444f` |
| CI lint del archivo local | Válido | `glab ci lint` → `CI/CD YAML is valid` |
| `develop` en GitLab | `589444f` (igual a GitHub) | API de ramas |
| `main` en GitLab | `a4e23dd` | API de ramas |
| Pipelines en GitLab | Ninguno todavía | `workflow:rules` excluía `api`/`schedule`; la importación no genera push |
| Registry del proyecto | Sin imágenes | API de Registry |
| Variables CI/CD | Vacías (accesibles) | API de variables |
| Secreto `GITLAB_TOKEN` en GitHub | No existe | `gh secret list` |
| Permisos GitHub de la cuenta | `push`, sin `admin` | API de repo |
| VPS / dominio | **No aprovisionados** | Cuenta DigitalOcean sin droplets ni claves |

Conclusión: `SPEC-046` tiene la base lista (proyecto, rama y CI válido) pero **falta la primera ejecución real y el espejo automático**. `SPEC-047` está implementada localmente y no verificada. No se declara cumplido `M4-01`, `M4-02`, `M4-05` ni `M4-07` hasta tener evidencia.

---

## 3. Prerrequisitos y responsables

| Prerrequisito | Responsable | Dónde |
| :--- | :--- | :--- |
| Crear secreto `GITLAB_TOKEN` | Administrador del repo GitHub (`vivacius`) | GitHub → Settings → Secrets and variables → Actions |
| Crear variables protegidas de deploy | Cualquier Owner de GitLab | GitLab → Settings → CI/CD → Variables |
| Crear Deploy Token `read_registry` | Cualquier Owner de GitLab | GitLab → Settings → Repository → Deploy tokens |
| Autorizar push del espejo a `main` | Owner de GitLab | Settings → Repository → Protected branches |
| Aprovisionar VPS y DNS | Responsable autorizado del equipo | Proveedor cloud + DNS |
| Autorizar apertura de 80/443 | Responsable del equipo | VPS |

### 3.1 Estado de permisos

- **GitLab:** los cuatro integrantes son Owner, por lo que variables, Deploy Tokens, ramas protegidas y ajustes de CI están disponibles.
- **GitHub:** la cuenta actual tiene `push` pero **no `admin`**, así que el secreto `GITLAB_TOKEN` debe crearlo el propietario del repositorio.
- **Infraestructura:** no hay VPS ni dominio; cualquier aprovisionamiento requiere autorización y costo.

Alternativas para la sincronización automática, en orden de preferencia:

1. **Pull mirroring de GitLab** (si el plan lo permite): el proyecto jala de GitHub cada pocos minutos.
2. **Push desde GitHub Actions** con `GITLAB_TOKEN` (requiere admin de GitHub).
3. **Pipeline programado en GitLab** que hace `git fetch` del repo público de GitHub y actualiza `develop`/`main`; no requiere permisos de GitHub, pero la latencia depende del intervalo del schedule.

---

## 4. Configuración del espejo GitHub → GitLab

1. Crear en GitLab un **Project Access Token** con scope `write_repository` y caducidad corta. Guardar el valor una sola vez.
2. En GitHub, crear el secreto `GITLAB_TOKEN` con ese valor.
3. Verificar que el workflow `Mirror to GitLab` aparece en Actions.
4. Si `main` está protegida en GitLab, permitir que la identidad del token haga push (Protected branches → Allowed to push). Si no se permite, el espejo de `main` fallará de forma visible; `develop` seguirá funcionando.

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
IMAGE_TAG=<sha-anterior-verificado> docker compose up -d --remove-orphans
curl -fsS https://<dominio>/health
```

No borrar `certbot/conf` ni `certbot/www` durante una reversión. Si el fallo es de configuración, restaurar el `docker-compose.yml` y la plantilla Nginx del commit anterior.

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
| Workflow `Mirror to GitLab` en verde | Pendiente | — | — |
| SHA GitHub = SHA GitLab | Pendiente | — | — |
| Pipeline GitLab `quality → build` en verde | Pendiente | — | — |
| Tag `<sha>` en Registry | Pendiente | — | — |
| Job `deploy_vps` en verde | Pendiente | — | — |
| `GET /health` 200 por HTTPS | Pendiente | — | — |
| `POST /predict` 200 con imagen válida | Pendiente | — | — |
| Puerto 8000 cerrado desde Internet | Pendiente | — | — |
| Push autorizado actualiza el servicio | Pendiente | — | — |
