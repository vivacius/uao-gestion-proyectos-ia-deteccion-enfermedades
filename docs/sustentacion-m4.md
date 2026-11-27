# Guion de Sustentación Final M1–M4 (`28/11/2026`)

**Duración máxima:** `15:00` minutos (sin videos ni diapositivas; demostración 100 % en vivo).  
**URL pública HTTPS:** `https://agroscan-uao.duckdns.org/`  
**Repositorio principal (GitHub):** `vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades`  
**Pipeline CI/CD y Registry (GitLab):** `vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades` (`ID 89374502`)

---

## Reparto de Bloques (14:00 min + 1:00 min margen)

### 1. `00:00–03:30` — Producto y Demo Pública HTTPS (John Restrepo)
- **Qué mostrar en vivo:** `https://agroscan-uao.duckdns.org/` y `https://agroscan-uao.duckdns.org/docs`.
- **Puntos clave:**
  - Problema fitosanitario, modelo `rodynaemad/plant-disease-dinov2-small` (`38` clases, `SafeTensors` en CPU), umbral $\tau=0.60$ y descargo agronómico orientativo.
  - Subir hoja real/de prueba desde la interfaz web HTTPS, mostrar petición `POST /predict` en Network (`200 OK`), ranking Top-3 y prueba de error controlado (`415` con formato no soportado).
  - Mostrar brevemente `docs/model-card.md` (honestidad metodológica: sin métricas inventadas sobre imágenes sintéticas).

### 2. `03:30–07:00` — Pipeline GitLab, Registry y Despliegue VPS (José Silva)
- **Qué mostrar en vivo:** Pipeline de GitLab (`89374502`), Container Registry y verificación HTTPS/puerto `8000`.
- **Puntos clave:**
  - Explicar `Mirror to GitLab` desde GitHub (`develop`/`main`, fast-forward sin `--force`, Git LFS con `model.safetensors`).
  - Mostrar las 4 etapas ejecutadas en verde: `quality` (`lint`), `test` (`run_test`), `build` (`package_wheel`, `build_docker` con SHA en Registry) y `deploy` (`deploy_vps`).
  - Mostrar `GET https://agroscan-uao.duckdns.org/health` (`200 OK`, `device: "cpu"`, `model_path: "/app/modelo_plantas"`), certificado TLS válido y que el puerto `8000` no está expuesto al público.

### 3. `07:00–10:30` — Gobernanza, Kanban, QA y Enmienda Constitucional (Santiago Correa)
- **Qué mostrar en vivo:** GitHub (`main` y `develop` protegidas), `Project #1` (`M3` y `M4 - Sprint activo`), Constitución `v2.0.0` y `pytest` / `ruff`.
- **Puntos clave:**
  - Protección de `main` y `develop` en GitHub (PR, 1 aprobación, CI `Ruff & Unit Tests`, bloqueo de `force push` y borrado).
  - Tablero Kanban (`Backlog`, `In Progress` WIP `4`, `In Review` WIP `2`, `Done`), `docs/kanban-flow-metrics.md` (`35+` PRs fusionados) y `docs/post-mortem-m1-m4.md`.
  - Suite ampliada a **365 pruebas unitarias** (`SPEC-051`) + `6` de integración, **`98 %` cobertura** en `src/` y `api/`, Ruff limpio y Enmienda Constitucional **`v2.0.0`** aprobada por consenso unánime (`PR #54`).

### 4. `10:30–14:00` — Arquitectura Backend, Seguridad y MLflow (Jhonatan Tapia)
- **Qué mostrar en vivo:** `https://agroscan-uao.duckdns.org/docs`, `https://agroscan-uao.duckdns.org/model-info` y MLflow UI local (`http://127.0.0.1:5050`).
- **Puntos clave:**
  - Contratos Pydantic v2, singleton CPU `local_files_only=True`, preprocesamiento `[1, 3, 224, 224]` y manejo de excepciones (`400`/`413`/`415`).
  - Secretos protegidos/enmascarados en GitHub Secrets y GitLab CI/CD Variables (`SPEC-048`), revisión de pares y trazabilidad en `docs/academic-compliance-matrix.md`.
  - MLflow local con 3 runs comparables ($\tau \in \{0.60, 0.80, 0.40\}$) y Model Registry (`dinov2-plant-disease-classifier`).

---

## Checklist Previo al Inicio de la Sustentación
1. Verificar `https://agroscan-uao.duckdns.org/health` = `200 OK`.
2. Tener abierto MLflow UI local en `http://127.0.0.1:5050`.
3. Tener abiertas las pestañas: GitHub (`develop`/`main`), `Project #1` (`M4 - Sprint activo`), GitLab Pipelines (`89374502`) y Container Registry.
