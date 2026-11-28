# Guion de Sustentación Final M4 (`28/11/2026`, 15 min en vivo)

**Lugar:** Salón 2103 (A2) · **Formato:** 100 % en vivo (sin videos ni diapositivas).  
**URL pública HTTPS:** `https://agroscan-uao.duckdns.org/`  
**GitHub:** `vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades`  
**GitLab (`ID 89374502`):** `vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades`

---

## 1. Entorno Abierto Antes de Entrar (Checklist 5.4)
- [ ] **VS Code** abierto en la raíz del repositorio con terminal integrada (`uv`, `pytest`, `ruff`, `docker` disponibles).
- [ ] **GitHub:** repositorio, PRs, reglas de protección (`main` / `develop`) y **Projects (Kanban `M4 - Sprint activo`)** abiertos.
- [ ] **GitLab:** proyecto `89374502`, **Pipelines** y **Container Registry** abiertos.
- [ ] **GitLab CLI (`glab`):** `glab auth status` y `glab pipeline status` funcionando en terminal.
- [ ] **GitLab MCP:** conectado en el cliente/agente de demostración.
- [ ] **Navegador:** `https://agroscan-uao.duckdns.org/`, `https://agroscan-uao.duckdns.org/docs`, `https://agroscan-uao.duckdns.org/health` y **MLflow UI** (`http://127.0.0.1:5050`) abiertos.
- [ ] **Variables CI:** pestaña de variables enmascaradas/protegidas lista (cero `.env` ni llaves en el repo).

---

## 2. Guion Cronometrado por Bloques Oficiales (5.3)

### `0:00 – 2:00` · Contexto y Repositorio — **John Restrepo**
- Presenta el problema fitosanitario, el modelo `DINOv2-small` (`38` clases, `SafeTensors` en CPU) y la app web en `https://agroscan-uao.duckdns.org/` (`POST /predict` + Top-3 + $\tau=0.60$).
- Muestra en VS Code/GitHub: `README.md` (badges + diagrama Archify), `CONSTITUTION.md`, `LICENSE`, `.gitignore`, `docs/model-card.md` y trazabilidad de PRs.

### `2:00 – 5:00` · Calidad y Docker — **Santiago Correa**
- En terminal ejecuta en vivo:
  - `uv sync --frozen` (o verifica entorno `uv`, cero `pip` / `requirements.txt`).
  - `uv run ruff check .` y `uv run pytest tests/unit -q` (**365 unitarias + 6 integración, 98 % cobertura**).
- Muestra `Dockerfile` multi-etapa CPU, `.dockerignore`, `docker-compose.yml` y la imagen con tag SHA en el **Container Registry** de GitLab (o `docker build`/`docker run` local).
- Muestra el Kanban (`Project #1` con WIP `4/2`) y `CONSTITUTION.md` (`v2.0.0`).

### `5:00 – 10:00` · Pipeline y Deploy en Vivo — **José Silva**
- Explica `.gitlab-ci.yml` (`quality: lint` → `test: run_test` → `build: package_wheel, build_docker` → `deploy: deploy_vps`) y `Mirror to GitLab`.
- **Cambio mínimo en vivo:** aplica un cambio mínimo controlado (vía PR de promoción `develop → main` aprobado por un par), muestra el disparo de `Mirror to GitLab` → pipeline de GitLab → actualización de imagen en Registry (`<sha>` y `latest`) → `deploy_vps` automático → `https://agroscan-uao.duckdns.org/` actualizada y `GET /health` `200 OK`.

### `10:00 – 13:00` · Infraestructura, Secretos y Herramientas — **Jhonatan Tapia**
- Muestra el Droplet/VPS activo, firewall (`22/80/443`, puerto `8000` cerrado al público), Nginx + TLS/HTTPS válido en `https://agroscan-uao.duckdns.org/`.
- Muestra variables CI protegidas y enmascaradas en GitLab (`DEPLOY_HOST`, llaves SSH, `DEPLOY_TOKEN`), **GitLab MCP conectado** y `glab auth status` / `glab pipeline status` en terminal.
- Cierra mostrando `/docs`, `/model-info` y **MLflow UI** (`http://127.0.0.1:5050` con los 3 runs y Model Registry).

### `13:00 – 15:00` · Preguntas Individuales — **Todos (4 integrantes)**
- Cada integrante explica su parte, una decisión de diseño clave y qué haría si falla el deploy:
  - **Santiago:** separación mocks (`tests/unit`, 365 pruebas rápidas) vs. modelo real (`tests/integration`); rollback verificando logs de `run_test` / `lint` o revirtiendo al SHA previo en Registry.
  - **José:** imagen CPU multi-etapa sin `uv`/dev deps y puerto `8000` interno; reversión con `IMAGE_TAG=<sha-anterior>` en `/opt/agroscan` (`docs/deployment-m4.md` § 9).
  - **Jhonatan:** carga local `SafeTensors` singleton en CPU + secretos mínimos en CI; diagnóstico en `deploy_vps` / logs Nginx / `docker compose ps` en VPS.
  - **John:** frontend desacoplado vía HTTP sin `torch` en UI + umbral $\tau=0.60$; diagnóstico en Network / `/health` / validación de errores `400`/`415`.
