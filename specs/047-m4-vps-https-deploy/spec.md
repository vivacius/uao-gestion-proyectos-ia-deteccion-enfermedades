# Especificación Técnica (Spec Kit): SPEC-047 VPS, Seguridad, HTTPS y Despliegue Continuo

**Identificador:** `SPEC-047`
**Feature Branch:** `feature/m4-gitlab-registry-deploy`
**Issues Relacionadas:** [#46](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/46) (sincronización canónica) · [#48](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/48) (CI/Registry/LFS) · [#49](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/49) (VPS/firewall/TLS) · [#50](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/50) (secretos) · [#51](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/51) (E2E público) · [#52](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/52) (gobernanza, fuera de alcance)
**Unidad / Historia Asociada:** `M4-01`, `M4-02`, `M4-06`, `M4-07`, `M4-08`, `TOOL-03`, `TOOL-07`
**Fecha de Elaboración SDD (Prospectiva):** 2026-11-24
**Trazabilidad Temporal:** **Especificación prospectiva elaborada ANTES de crear el Compose de producción, la configuración TLS y el job de despliegue.**
**Estado:** Implementado y validado localmente; **pendiente de validación en GitLab oficial y VPS**
**Responsable:** Frente B — DevOps (asignación por ratificar por el equipo)
**Artefactos Relacionados:** [plan.md](./plan.md) · [tasks.md](./tasks.md) · [docs/deployment-m4.md](../../docs/deployment-m4.md)

---

## 1. Propósito y Alcance

Definir el despliegue productivo del sistema fitosanitario en una VPS con Docker Engine/Compose, firewall mínimo, usuario de despliegue sin privilegios interactivos, proxy inverso Nginx con TLS válido y una etapa `deploy` en GitLab CI/CD que actualice el servicio a partir de la imagen publicada en el Container Registry.

La unidad cubre:

1. **Aprovisionamiento reproducible** de la VPS (Docker Engine + Compose, usuario `deploy`, firewall SSH/HTTP/HTTPS).
2. **Compose de producción** separado del Compose local: la API no publica el puerto 8000; solo Nginx expone 80/443.
3. **TLS/HTTPS válido** con Let's Encrypt (certbot en modo *webroot* + *standalone* para el primer certificado), renovación y recarga de Nginx.
4. **Job `deploy` automático en `develop`** (manual y con aprobación en `main`), con *resource group* para evitar despliegues concurrentes, verificación de `/health` y reversión documentada.
5. **Gestión de secretos** exclusivamente mediante variables protegidas/enmascaradas de GitLab o `.env` fuera de Git.

**Fuera de alcance:** compra del dominio, aprovisionamiento de la VPS sin autorización humana, cambios en el modelo/API/UI y configuración del espejo GitHub → GitLab (`SPEC-046`, cuya especificación canónica ya vive en `develop` tras la PR #47; esta PR no la duplica).

### 1.1 Estado de implementación y validación

| Componente | Estado | Evidencia / pendiente |
| :--- | :--- | :--- |
| `deploy/docker-compose.prod.yml`, `deploy/nginx.prod.conf.template`, `deploy/.env.production.example` | Implementado localmente | `docker compose config` válido; `api` solo declara `expose: 8000` |
| Job `deploy_vps` y stage `deploy` en `.gitlab-ci.yml` | Implementado localmente | `glab ci lint` válido; **no ejecutado en GitLab oficial** |
| Pipeline `quality → test → build → deploy` | Implementado localmente | Etapas verificadas por parseo; **no ejecutado en GitLab** |
| VPS, firewall, DNS y TLS | **Pendiente** | No hay VPS ni dominio aprovisionados |
| Verificación E2E `/health`, `/predict`, HTTPS | **Pendiente** | Requiere despliegue real |
| Variables y secretos protegidos | Diseñado; no configurado | Solo se documentan nombres; no hay valores |

> **Honestidad de estado:** GitHub Actions en verde no sustituye la validación del pipeline oficial de GitLab ni del despliegue público. La unidad solo se declara verificada con evidencia remota real.

---

## 2. Decisiones de Diseño

| Decisión | Justificación |
| :--- | :--- |
| **Compose productivo separado** (`deploy/docker-compose.prod.yml`). | Preserva el Compose local verificado en M3 y evita arrastrar *bind mounts* de desarrollo a producción. |
| **La API solo usa `expose: 8000`; Nginx publica 80/443.** | Cumple `C6`/`M4-02`: el backend no queda accesible directamente por 8000. |
| **Nginx sirve TLS y hace proxy de todo `/` a `api:8000`.** | La API ya monta el frontend estático en `/` (SPEC-031), manteniendo *same-origin* y el desacoplamiento por HTTP. |
| **Plantilla Nginx con `${DOMAIN}` y `NGINX_ENVSUBST_FILTER=DOMAIN`.** | Evita sustituir variables nativas de Nginx y permite reutilizar la imagen oficial sin builds adicionales. |
| **Certificados en `./certbot/conf` y validación en `./certbot/www`.** | *Bind mounts* simples, inspeccionables y fáciles de respaldar. |
| **Primer certificado con `certbot --standalone`; renovación con `--webroot`.** | Permite emitir TLS antes de que Nginx tenga certificados y renovar sin detener el servicio. |
| **Credenciales de Registry en la VPS mediante Deploy Token (`read_registry`).** | El `CI_JOB_TOKEN` caduca y no debe persistir en la VPS. |
| **Sincronización GitHub → GitLab solo fast-forward y con credencial efímera.** | `SPEC-046` prohíbe reescribir historia; el token se entrega con `GIT_ASKPASS` temporal y nunca se embebe en la URL ni en `.git/config`. |
| **`deploy` automático solo en `develop`; manual en `main`.** | Un push de integración se demuestra en vivo; producción principal conserva aprobación humana. |

### 2.1 Supuestos que deben confirmarse antes de ejecutar

- Existe una VPS accesible por SSH con Docker Engine ≥ 24 y Compose v2.
- Existe un dominio o subdominio con registro DNS A/AAAA apuntando a la VPS.
- El Owner del proyecto GitLab (`vivacius`) crea las variables protegidas y el Deploy Token.
- El equipo autoriza abrir 80/443 y desplegar; nada de esto se ejecutará sin esa autorización.

---

## 3. Escenarios de Aceptación (Gherkin)

### AC47.1 — API no expuesta directamente
- **Dado** el Compose de producción desplegado,
- **Cuando** se inspeccionan los puertos publicados,
- **Entonces** solo `web` publica `80` y `443`; `api` únicamente declara `expose: 8000` en la red interna y `http://IP:8000` no responde desde Internet.

### AC47.2 — HTTPS válido y redirección
- **Dado** el dominio configurado y el certificado emitido,
- **Cuando** se solicita `http://<dominio>/health`,
- **Entonces** responde `301` hacia `https://<dominio>/health`, y la respuesta HTTPS presenta un certificado válido (sin advertencias) y `200`.

### AC47.3 — Endpoints funcionales en producción
- **Dado** el servicio desplegado,
- **Cuando** se ejecutan `GET /health`, `GET /model-info`, `GET /docs` y `POST /predict`,
- **Entonces** responden `200` con el modelo cargado en CPU, 38 clases y Top-3; un archivo inválido responde `400`/`415` según corresponda.

### AC47.4 — Despliegue automático por push
- **Dado** un push autorizado a `develop` que supera `quality` y `build`,
- **Cuando** el job `deploy_vps` se ejecuta,
- **Entonces** la VPS descarga la imagen con el SHA del commit, recrea los contenedores y la verificación de `/health` termina en `200`; el job queda asociado al entorno `production`.

### AC47.5 — Secretos y firewall
- **Dado** el repositorio y la VPS,
- **Cuando** se auditan archivos, logs y reglas de red,
- **Entonces** no hay claves ni tokens versionados, las variables sensibles están protegidas/enmascaradas, y el firewall solo permite SSH, HTTP y HTTPS (más las reglas de egreso necesarias).

### AC47.6 — Reversión documentada
- **Dado** un despliegue con regresión funcional,
- **Cuando** se ejecuta el procedimiento de reversión,
- **Entonces** es posible volver al tag SHA anterior con `IMAGE_TAG=<sha-anterior> docker compose up -d` sin reconstruir la imagen ni perder los certificados.

---

## 4. Requisitos Trazables

| ID | Requisito | Evidencia esperada |
| :--- | :--- | :--- |
| `M4-01` | VPS con Docker y firewall mínimo. | `docker version`, `ufw status` (sin IP ni credenciales en el repo). |
| `M4-02` | Proxy inverso HTTPS válido. | `curl -I https://<dominio>/health` y cadena TLS válida. |
| `M4-06` | Secretos protegidos. | Variables enmascaradas/protegidas; `.env` ignorado. |
| `M4-07` | Despliegue continuo verificable. | Job `deploy_vps` en verde y contenedor actualizado. |
| `M4-08` | Healthcheck operativo. | `GET /health` 200 tras el despliegue. |
| `TOOL-03` | GitLab CI/CD y Registry. | Pipeline y tag SHA consumidos por la VPS. |

---

## 5. Capacidades Protegidas que No Se Modifican

- Modelo DINOv2, pesos SafeTensors, 38 clases, τ = 0.60 y descargo agronómico.
- Endpoints y contratos Pydantic existentes.
- Frontends desacoplados; prohibición de Streamlit.
- `Dockerfile` CPU multi-etapa y usuario no-root.
- Compose local y Nginx local de M3.
- Suite de pruebas, Ruff, cobertura ≥ 85 % y Gitflow.

---

## 6. Criterio de Cierre

La unidad se considera **verificada** solo con evidencia real de: VPS operativa, firewall activo, DNS resolviendo, certificado válido, `/health` 200 por HTTPS, puerto 8000 no accesible desde Internet, job `deploy_vps` ejecutado y una actualización visible tras un push autorizado. Sin VPS ni dominio, el estado máximo es **implementado y validado localmente, no verificado**. Un GitHub Actions en verde no cuenta como evidencia de esta unidad.
