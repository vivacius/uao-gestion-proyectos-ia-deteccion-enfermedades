# Reglas Operativas para Agentes de IA (`AGENTS.md`)
<!-- Grupo 2 — Maestría en IA y Ciencia de Datos | UAO -->

Este documento es el **punto de entrada normativo y operativo** para cualquier agente de inteligencia artificial que opere sobre el repositorio. Define jerarquía de autoridad, reglas inamovibles, flujo de trabajo, protección contra regresiones y uso autorizado de herramientas, sin duplicar el inventario detallado de [docs/academic-compliance-matrix.md](docs/academic-compliance-matrix.md).

---

## 1. Autoridad, Precedencia y Gobernanza

En caso de conflicto, rige estrictamente el siguiente orden de precedencia (de mayor a menor autoridad):

1. **Instrucciones del usuario y restricciones oficiales aplicables.**
2. **Reglas académicas vigentes del curso:** los requisitos `M1`–`M4` son **acumulativos**. Únicamente ante incompatibilidad explícita prevalece la regla oficial posterior (`M4 > M3 > M2 > M1`); toda regla anterior no sustituida continúa vigente.
3. **Constitución aprobada:** [.specify/memory/constitution.md](.specify/memory/constitution.md) (su reforma exige consenso unánime de los 4 integrantes).
4. **`AGENTS.md`** (este documento).
5. **Matriz académica y especificaciones SDD:** [docs/academic-compliance-matrix.md](docs/academic-compliance-matrix.md) y `specs/`.
6. **Skills y procedimientos operativos.**

- **Primacía humana:** Ningún agente puede tomar decisiones unilaterales ni técnicas que contradigan requisitos oficiales o decisiones humanas aprobadas.
- **Estado vigente de capacidades (`HU-01`–`HU-08`):** `HU-01`–`HU-07` y la base de `HU-08` (empaquetado Wheel, `Dockerfile` CPU multi-etapa y `docker-compose.yml` + Nginx) ya están implementadas en M3. Quedan para M4 el pipeline CI/CD completo en GitLab, Container Registry, VPS, TLS/HTTPS, observabilidad de despliegue y enmienda constitucional (`M4-09`).

| Historia | Responsable Humano | Rol | Alcance Técnico Vigente |
| :--- | :--- | :--- | :--- |
| **HU-01** | Santiago Correa | DevOps | Tooling base, `uv`, Ruff, Python 3.13. |
| **HU-02** | José Silva | ML | Preprocesamiento `[1, 3, 224, 224]` `float32`. |
| **HU-03** | Jhonatan Tapia | ML | Carga SafeTensors local e inferencia CPU $< 300\text{ ms}$. |
| **HU-04** | John Restrepo | Backend | Postproceso, 38 clases en español, $\tau=0.60$ y descargo agronómico. |
| **HU-05** | Jhonatan Tapia | Backend | API REST FastAPI, OpenAPI y contratos Pydantic v2. |
| **HU-06** | John Restrepo | Frontend | Interfaz de escritorio Tkinter y web estática desacoplada vía HTTP. |
| **HU-07** | Santiago Correa | Testing | Suite `pytest` AAA (mín. 120 pruebas; cobertura $\ge 85\%$). |
| **HU-08** | José Silva | DevOps | Base Wheel/Docker CPU lista en M3; hardening CI/CD, Registry, VPS y TLS en M4. |

- **Code Reviewer general:** Jhonatan Tapia (toda PR requiere revisión aprobada de un par distinto del autor).

---

## 2. Reglas Inamovibles (Académicas y de Conservación)

### A. Obligaciones Académicas Acumuladas (`M1`–`M4`)
- **Arquitectura y calidad:** `src/` layout modular (`src/`, `api/`, `ui/`, `tests/`), tipado (`type hints`), docstrings en API pública y separación estricta inferencia/servicio/API/UI. Cero notebooks (`.ipynb`) o código muerto.
- **Entorno y verificación:** Python 3.13, gestor único `uv` (`pyproject.toml` + `uv.lock`), Ruff (`ruff check .`, `ruff format --check .`) y `pytest` bajo patrón Arrange-Act-Assert (AAA), con mínimo académico de 120 pruebas y cobertura $\ge 85\%$ en `src/` y `api/`, sin reducir capacidades actuales.
- **Planeación y trazabilidad:** Propuesta M2 (`documento/Plantilla.*`), alcance, criterios Given-When-Then, tablero Kanban, MLflow (3 runs comparables, tracking y Model Registry), Model Card (`docs/model-card.md`), Spec Kit (`specs/`) y PRs verificables.
- **Frontend desacoplado:** Consumo exclusivo de la API vía HTTP (Tkinter y Web HTML/CSS/JS). **Streamlit está expresamente prohibido** como interfaz evaluable en M3/M4.
- **Alcance M4:** CI/CD (`lint → test → build → deploy`), Container Registry, VPS, Docker CPU, HTTPS/TLS, gestión segura de secretos y despliegue demostrable.
- **Honestidad SDD:** No atribuir validez prospectiva a las **31 especificaciones retrospectivas** (`specs/010..040/`). Toda nueva implementación requiere especificación prospectiva previa.

### B. Protección contra Regresiones
Queda prohibido alterar sin autorización expresa y verificación previa las 10 capacidades protegidas en [docs/academic-compliance-matrix.md § 2](docs/academic-compliance-matrix.md):
- Modelo `rodynaemad/plant-disease-dinov2-small`, pesos `model.safetensors` (`local_files_only=True`), `config.json`, 38 clases en español y contratos de inferencia (`[1, 3, 224, 224]`, `torch.no_grad()`, Softmax, $\tau=0.60$, descargo agronómico no prescriptivo).
- Endpoints FastAPI (`GET /health`, `GET /model-info`, `POST /predict`, `GET /docs`) y frontends desacoplados (`ui/desktop_app.py`, `ui/web/static/`, `ui/api_client.py`).
- Artefactos MLflow (`mlflow_tracking.db`, `mlruns/`, `mlflow_data/`), suite `tests/`, `Dockerfile`, `docker-compose.yml`, `deploy/nginx.conf`, `.github/workflows/ci.yml` y documentación vigente.
- No modificar recursos locales ignorados (`.venv/`, `.env`, etc.). Todo cambio arquitectónico requiere autorización humana expresa.
- **Protección de artefactos institucionales y contratos nativos:** Prohibido sustituir o modificar plantillas oficiales del curso (incluyendo `.github/PULL_REQUEST_TEMPLATE.md`), rúbricas, fuentes oficiales o contratos nativos de herramientas (ej. estructura esperada por Spec Kit 1.2.2) sin autorización expresa. Ante desactualizaciones aparentes, documentar la discrepancia y solicitar decisión humana; los agentes deben adaptar sus flujos a los artefactos oficiales (ej. agregando trazabilidad M3/M4 adicional en la descripción de la PR sin editar la plantilla oficial).

---

## 3. Flujo de Trabajo, Kanban y Restricciones Git

### Flujo Obligatorio (SDD + GitHub Projects)
`Historia → Issue/Project → SPEC prospectiva → tareas → implementación → pruebas → PR revisada → merge → Done`
- **Tablero Kanban (GitHub Projects):** Columnas `Backlog`, `In Progress` (máximo integrantes del equipo = 4; 1 por desarrollador), `In Review` (máximo 2) y `Done`. Mantener seguimiento de métricas **WIP**, **throughput**, **work item age** y **cycle time**.
- **SDD primero:** Redactar especificación prospectiva (`specs/NNN-.../`) antes de codificar o modificar normativa.
- **Alcance acotado:** Ejecutar una unidad controlable por vez, identificando requisitos (`M1`–`M4`, `TOOL-XX`), criterios de aceptación, impactos y riesgos de regresión.
- **Veracidad de estado:** Distinguir explícitamente entre *implementado*, *verificado*, *listo para PR* e *integrado*. Nunca inventar resultados ni ocultar limitaciones.

### Restricciones Git Estrictas
- **Prohibido** hacer commit o push directo a `main` o `develop`.
- **Prohibido** ejecutar `git merge`, `git rebase`, `git push --force`, `git reset --hard`, `git clean` o borrar ramas/worktrees sin autorización explícita.
- **Prohibido** crear commits, hacer `push`, abrir PRs, conmutar ramas, aprobar/fusionar PRs o permitir que scripts de Spec Kit creen o conmuten ramas salvo autorización explícita en la unidad de trabajo.
- Todo cambio hacia `develop` requiere PR con [.github/PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md), Conventional Commits, revisión aprobada de un par humano y CI en verde.
- *Nota sobre hooks locales:* `.git/hooks/` contiene únicamente hooks de Git LFS; no existe un hook pre-commit GGA instalado localmente.

---

## 4. Herramientas y Seguridad Operativa

- **`Makefile` ([Makefile](Makefile)):** Interfaz operativa estándar de 17 targets con comandos reales y seguros (`uv`, `ruff`, `pytest`, `uvicorn`, `mlflow`, `docker`). Diferenciar siempre la disponibilidad local de GNU Make frente a la ejecución en CI.
- **GitHub y GitLab:** **GitHub** es el repositorio principal (código, Issues, PRs, Kanban, revisión humana) operado mediante **`gh` CLI** y **GitHub MCP** autorizados. **GitLab** actuará en M4 para CI/CD, Container Registry y despliegue VPS sujeto a arquitectura aprobada, mediante **`glab` CLI** y **GitLab MCP** cuando estén configurados.
- **Reglas de entorno y seguridad:**
  - Prohibido usar `pip` o crear `requirements.txt` (gestor único `uv`, § 2A).
  - No afirmar instalación o conexión de herramientas/servicios (`make`, `docker`, `glab`, MCPs) sin evidencia directa. MCP y CLI no sustituyen controles de autorización humana.
  - No instalar herramientas, modificar `PATH` global ni aprovisionar servicios sin autorización expresa.
  - **Secretos nunca en código, Git, prompts, logs ni documentación pública.**

---

## 5. Skills Operativas Locales (`.agents/skills/`)

Antigravity descubre automáticamente las skills del proyecto en `.agents/skills/<nombre>/SKILL.md` (carga progresiva por nombre y descripción):

- [`academic-compliance`](.agents/skills/academic-compliance/SKILL.md): Activar al iniciar cualquier unidad para validar requisitos `M1`–`M4`, precedencia, prohibiciones (Streamlit, `pip`, `.ipynb`) y capacidades protegidas.
- [`sdd-workflow`](.agents/skills/sdd-workflow/SKILL.md): Activar antes de diseñar o codificar para crear specs prospectivas (`spec.md`, `plan.md`, `tasks.md`) preservando `specs/001..040/`.
- [`quality-and-make`](.agents/skills/quality-and-make/SKILL.md): Activar al ejecutar o validar `Makefile`, `uv`, Ruff y `pytest` AAA según alcance real del cambio.
- [`github-gitlab-operations`](.agents/skills/github-gitlab-operations/SKILL.md): Activar para consultas o acciones autorizadas en GitHub (`gh`/MCP) y GitLab (`glab`/MCP), Gitflow y limpieza de ramas.
- [`secure-cicd-deployment`](.agents/skills/secure-cicd-deployment/SKILL.md): Activar en unidades M4 de CI/CD, Docker CPU, Registry, VPS, HTTPS y secretos protegidos.
- *Nota de seguridad:* `.agents/skills/archify/` permanece en cuarentena (`.gitignore`) y no debe ejecutarse ni reutilizarse.

---

## 6. Referencias Oficiales del Repositorio

- **Constitución vigente:** [.specify/memory/constitution.md](.specify/memory/constitution.md)
- **Matriz académica M1–M4 (SSOT):** [docs/academic-compliance-matrix.md](docs/academic-compliance-matrix.md)
- **Interfaz operativa:** [Makefile](Makefile)
- **Especificaciones SDD:** `specs/` y `.specify/`
- **Plantilla de PR:** [.github/PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md)
