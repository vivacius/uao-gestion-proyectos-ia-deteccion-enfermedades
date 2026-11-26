# Constitución del Proyecto: Detección Fitosanitaria con DINOv2
<!-- Grupo 2 — Maestría en IA y Ciencia de Datos | Universidad Autónoma de Occidente (UAO) -->

## Preámbulo y Propósito
Esta Constitución define los principios de gobernanza técnica, arquitectura, aseguramiento de la calidad y dinámica de colaboración para el desarrollo del sistema de cribado y detección de patologías vegetales basado en visión artificial (DINOv2) en CPU. Es de cumplimiento obligatorio para los cuatro integrantes del Grupo 2 y para todos los asistentes de IA que operen sobre el repositorio.

Esta Constitución rige de forma subordinada a las instrucciones del usuario y a las reglas académicas oficiales del curso, las cuales son acumulativas (`M1`–`M4`). Únicamente ante incompatibilidad explícita entre reglas oficiales prevalece la posterior (`M4 > M3 > M2 > M1`).

---

## Principios Fundamentales

### I. Arquitectura Modular, Alta Cohesión y Bajo Acoplamiento
- **Estructura src/ layout:** Todo el código del dominio reside en `src/`, servicios en `api/`, interfaz en `ui/` y pruebas en `tests/`.
- **Separación de responsabilidades:**
  - `src/preprocessing.py`: Validación de imágenes y generación de tensores normalizados $[1, 3, 224, 224]$ (`torch.float32`, media y desviación ImageNet). Lanza `ImageValidationError` (`CorruptedImageError`, `UnsupportedImageFormatError`, `ImageSizeExceededError`, definidos en `src/exceptions.py`) ante archivos inválidos.
  - `src/model_loader.py` e `src/inference.py`: Carga determinista y segura de pesos locales mediante `safetensors` en CPU sin descargas en runtime, ejecutando inferencia bajo `torch.no_grad()`.
  - `src/postprocessing.py` e `src/labels.py`: Mapeo taxonómico a 38 clases en español, Softmax probabilístico ($1.000 \pm 0.001$), filtro de incertidumbre ($\tau = 0.60$) y descargo de responsabilidad agronómica obligatoria (soporte orientativo, prohibición explícita de prescribir agroquímicos).
  - `api/main.py` y `api/schemas.py`: Capa de servicio FastAPI con contratos Pydantic estrictos, endpoints `GET /health`, `GET /model-info`, `POST /predict` y `GET /docs`.
  - `ui/desktop_app.py`, `ui/api_client.py` y `ui/web/static/`: Interfaces desacopladas (escritorio Tkinter y web HTML/CSS/JS) que consumen la API exclusivamente vía HTTP. Queda expresamente prohibido el uso de Streamlit como interfaz evaluable en M3 y M4.
- **Prohibición de acoplamientos circulares y notebooks:** Queda estrictamente prohibida la presencia o ejecución de `.ipynb`, scripts monolíticos o dependencias directas de la API hacia la UI.

### II. Gestión Determinista del Entorno con uv (Python 3.13)
- **Gestor único:** Se utiliza `uv` con Python 3.13 como versión objetivo de ejecución y CI (`.python-version` = `3.13`, `pyproject.toml` `requires-python` = `">=3.12,<3.14"`). Se prohíbe taxativamente el uso directo de `pip`, `pipenv`, `conda` o la creación de archivos `requirements.txt`.
- **Sincronización:** Cada cambio de dependencias debe actualizar simultáneamente `pyproject.toml` y `uv.lock` en el mismo commit (`uv sync`).
- **Aislamiento:** El entorno `.venv/` es local y nunca se versiona.

### III. Desarrollo Guiado por Pruebas (Test-First & pytest AAA)
- **Patrón AAA:** Todas las pruebas unitarias e integradas deben estructurarse bajo el patrón Arrange-Act-Assert. Mínimo académico de 120 pruebas AAA sin reducir las capacidades vigentes.
- **Cobertura combinada $\ge 85\%$:** La cobertura acumulada sobre `src/` y `api/` debe ser $\ge 85\%$, verificada mediante `pytest --cov`.
- **Velocidad y aislamiento:** La suite de pruebas unitarias (`tests/unit/`) debe ejecutarse en menos de 10 segundos, aislando dependencias externas mediante dobles de prueba (mocks).
- **Pruebas de integración:** `tests/integration/` valida el flujo end-to-end con el modelo real y el cliente de pruebas de FastAPI (`TestClient`).

### IV. Gobernanza Gitflow, Kanban y Revisión por PR
- **Flujo de ramas:**
  - `main`: Reservada exclusivamente para versiones de cierre de hito etiquetadas y validadas.
  - `develop`: Rama base de integración continua donde convergen las funcionalidades aprobadas.
  - `feature/*`: Ramas de trabajo individuales para historias de usuario específicas (`feature/HU-XX-...` o `feature/m3-...`).
  - Prohibido hacer commit o push directo a `develop` o `main`.
- **Límites WIP en Kanban (GitHub Projects):**
  - Límite WIP estricto de máximo 1 tarea activa por desarrollador simultáneamente (límite global del equipo = 4 tareas activas).
  - Regla rectora: *"Stop starting, start finishing"*.
- **Plantilla y Revisión Obligatoria de Pull Requests:**
  - Todo cambio hacia `develop` debe tramitarse mediante un Pull Request que utilice íntegramente `.github/PULL_REQUEST_TEMPLATE.md`.
  - Ninguna PR puede fusionarse sin la aprobación formal de al menos un compañero de equipo distinto del autor (Jhonatan Tapia actúa como Code Reviewer general, con revisiones cruzadas entre pares).
  - El autor de la PR es el único responsable de ejecutar la fusión hacia `develop` tras recibir el dictamen de aprobación.

### V. Calidad Estática, Seguridad y Clean Code
- **Linters y formateo:** Cero advertencias con `uv run ruff check .` y `uv run ruff format --check .` (código de salida 0).
- **Control de artefactos pesados y secretos:** Prohibido subir pesos binarios directamente al historial Git estándar; `model.safetensors` se gestiona exclusivamente mediante Git LFS (`.gitattributes`), prohibiendo binarios sin LFS, secretos, credenciales, bases de datos locales no autorizadas (`*.sqlite`, `*.db`, `engram.db`) o logs de ejecución.
- **Conventional Commits:** Mensajes de commit en imperativo, descriptivos, con tipo (`feat:`, `fix:`, `test:`, `refactor:`, `chore:`, `docs:`) y longitud $\le 72$ caracteres en el asunto.

---

## Roles y Responsabilidades del Equipo

| Integrante | Rol Principal | Historias de Usuario Asignadas | Responsabilidad Principal |
| :--- | :--- | :--- | :--- |
| **Santiago Correa** | DevOps / Testing | **HU-01** (Tooling Base, 2 SP)<br>**HU-07** (Suite Pruebas pytest, 3 SP) | Gestión del entorno `uv`, linters `ruff`, arquitectura de pruebas automatizadas y cobertura $\ge 85\%$. |
| **José Silva** | ML / MLOps | **HU-02** (Preprocesamiento Tensores, 3 SP)<br>**HU-08** (Docker & Wheel, 2 SP) | Pipeline de ingestión y normalización de tensores, empaquetado Wheel y contenerización CPU base (M3) e infraestructura CI/CD/VPS (M4). |
| **Jhonatan Tapia** | ML / Backend & Code Reviewer | **HU-03** (Carga SafeTensors e Inferencia, 3 SP)<br>**HU-05** (API REST FastAPI, 3 SP) | Inferencia determinista CPU, servicio asíncrono FastAPI y revisión cruzada de código. |
| **John Restrepo** | Backend / Frontend | **HU-04** (Postproceso e Incertidumbre, 2 SP)<br>**HU-06** (UI de escritorio y Web, 3 SP) | Mapeo fitosanitario en español, filtro $\tau=0.60$, descargo legal e interfaces desacopladas (Tkinter y Web HTML/CSS/JS). |

Total: **8 Historias de Usuario**, **25 Criterios de Aceptación**, **21 Story Points**.

---

## Puertas de Calidad (Quality Gates) para M3 y M4

### Gates base (M3)
1. **Gate 1: Especificación y Contratos (SDD):** Cada HU o unidad M4 debe contar con su especificación prospectiva, criterios de aceptación Gherkin y tareas trazadas en Spec Kit antes de codificar.
2. **Gate 2: Verificación de Código y Tipado:** Cohesión estricta en contratos de datos con type hints y docstrings en todas las funciones públicas.
3. **Gate 3: Calidad Estática:** `uv run ruff check .` y `uv run ruff format --check .` sin observaciones.
4. **Gate 4: Verificación Funcional:** `uv run pytest -v` con $\ge 120$ pruebas AAA, cobertura $\ge 85\%$ y sin advertencias bloqueantes.
5. **Gate 5: Revisión Cruzada:** Checklist de revisor completo en el PR y aprobación explícita de un par distinto del autor.

### Gates adicionales de Despliegue y CI/CD (M4)
6. **Gate 6: Pipeline GitLab (`lint → test → build → deploy`):** Ejecución bloqueante de Ruff y `pytest` (`--cov-fail-under=85`), empaquetado Wheel y construcción Docker CPU multi-etapa con Git LFS íntegro.
7. **Gate 7: Container Registry y Secretos:** Imagen Docker publicada en Registry con tag trazable por SHA de commit; cero secretos en código, logs o historial Git (exclusivamente variables protegidas y enmascaradas).
8. **Gate 8: Producción VPS y TLS/HTTPS:** Proxy inverso con certificado HTTPS válido, puerto `8000` cerrado al exterior, despliegue continuo reproducible y `GET /health` respondiendo `200 OK` sobre HTTPS.

---

## Gobernanza, Fuentes SSOT y Enmiendas
- Esta Constitución rige de forma subordinada a las instrucciones del usuario y a las reglas académicas oficiales acumulativas (`M1`–`M4`).
- Se designa a `docs/academic-compliance-matrix.md` como fuente única de trazabilidad (SSOT) de requisitos `M1`–`M4` y capacidades protegidas, y a `Makefile` como interfaz operativa estándar.
- **GitHub** actúa como repositorio principal de código, Issues, PRs y Kanban; **GitLab** actúa como plataforma de CI/CD, Container Registry y despliegue M4, sujeto a sincronización unidireccional segura (`SPEC-046`) y uso autorizado de `gh`, `glab` y MCPs.
- Cualquier modificación a los principios, responsabilidades, criterios de aceptación o umbrales de cobertura requiere consenso unánime de los cuatro integrantes del Grupo 2 y su debido registro en el historial de enmiendas.

**Versión**: 2.0.0 | **Ratificado**: 2026-11-12 | **Última Enmienda**: 2026-11-25 (`SPEC-050`, Enmienda M4 `ENM-01`–`ENM-07`)
