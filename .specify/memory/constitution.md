# Constitución del Proyecto: Detección Fitosanitaria con DINOv2
<!-- Grupo 2 — Maestría en IA y Ciencia de Datos | Universidad Autónoma de Occidente (UAO) -->

## Preámbulo y Propósito
Esta Constitución define los principios de gobernanza técnica, arquitectura, aseguramiento de la calidad y dinámica de colaboración para el desarrollo del sistema de cribado y detección de patologías vegetales basado en visión artificial (DINOv2) en CPU. Es de cumplimiento obligatorio para los cuatro integrantes del Grupo 2 y para todos los asistentes de IA que operen sobre el repositorio.

---

## Principios Fundamentales

### I. Arquitectura Modular, Alta Cohesión y Bajo Acoplamiento
- **Estructura src/ layout:** Todo el código del dominio reside en `src/`, servicios en `api/`, interfaz en `ui/` y pruebas en `tests/`.
- **Separación de responsabilidades:**
  - `src/preprocessing.py`: Validación de imágenes y generación de tensores normalizados $[1, 3, 224, 224]$ (`torch.float32`, media y desviación ImageNet). Lanza `InvalidImageFormatException` ante archivos corruptos o formatos inválidos.
  - `src/model_loader.py` e `src/inference.py`: Carga determinista y segura de pesos locales mediante `safetensors` en CPU sin descargas en runtime, ejecutando inferencia bajo `torch.no_grad()`.
  - `src/postprocessing.py` e `src/labels.py`: Mapeo taxonómico a 38 clases en español, Softmax probabilístico ($1.000 \pm 0.001$), filtro de incertidumbre ($\tau = 0.60$) y descargo de responsabilidad agronómica obligatoria (soporte orientativo, prohibición explícita de prescribir agroquímicos).
  - `api/main.py` y `api/schemas.py`: Capa de servicio FastAPI con contratos Pydantic estrictos, endpoints `GET /health`, `POST /predict` y `GET /docs`.
  - `ui/desktop_app.py` y `ui/api_client.py`: Interfaz de usuario de escritorio desacoplada para técnicos de campo, consumiendo la API vía cliente HTTP.
- **Prohibición de acoplamientos circulares y notebooks:** Queda estrictamente prohibida la presencia o ejecución de `.ipynb`, scripts monolíticos o dependencias directas de la API hacia la UI.

### II. Gestión Determinista del Entorno con uv (Python 3.13)
- **Gestor único:** Se utiliza exclusivamente `uv` sobre Python 3.13. Se prohíbe taxativamente el uso directo de `pip`, `pipenv`, `conda` o la creación de archivos `requirements.txt`.
- **Sincronización:** Cada cambio de dependencias debe actualizar simultáneamente `pyproject.toml` y `uv.lock` en el mismo commit (`uv sync`).
- **Aislamiento:** El entorno `.venv/` es local y nunca se versiona.

### III. Desarrollo Guiado por Pruebas (Test-First & pytest AAA)
- **Patrón AAA:** Todas las pruebas unitarias e integradas deben estructurarse bajo el patrón Arrange-Act-Assert.
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
- **Control de artefactos pesados y secretos:** Prohibido subir al repositorio pesos del modelo (`*.safetensors`, `*.bin`, `*.pt`, `*.onnx`), secretos, credenciales, bases de datos locales (`*.sqlite`, `*.db`, `engram.db`) o logs de ejecución.
- **Conventional Commits:** Mensajes de commit en imperativo, descriptivos, con tipo (`feat:`, `fix:`, `test:`, `refactor:`, `chore:`, `docs:`) y longitud $\le 72$ caracteres en el asunto.

---

## Roles y Responsabilidades del Equipo

| Integrante | Rol Principal | Historias de Usuario Asignadas | Responsabilidad Principal |
| :--- | :--- | :--- | :--- |
| **Santiago Correa** | DevOps / Testing | **HU-01** (Tooling Base, 2 SP)<br>**HU-07** (Suite Pruebas pytest, 3 SP) | Gestión del entorno `uv`, linters `ruff`, arquitectura de pruebas automatizadas y cobertura $\ge 85\%$. |
| **José Silva** | ML / MLOps | **HU-02** (Preprocesamiento Tensores, 3 SP)<br>**HU-08** (Docker & Wheel, 2 SP) | Pipeline de ingestión y normalización de tensores, empaquetado Wheel y contenerización en CPU. |
| **Jhonatan Tapia** | ML / Backend & Code Reviewer | **HU-03** (Carga SafeTensors e Inferencia, 3 SP)<br>**HU-05** (API REST FastAPI, 3 SP) | Inferencia determinista CPU, servicio asíncrono FastAPI y revisión cruzada de código. |
| **John Restrepo** | Backend / Frontend | **HU-04** (Postproceso e Incertidumbre, 2 SP)<br>**HU-06** (UI de escritorio, 3 SP) | Mapeo fitosanitario en español, filtro $\tau=0.60$, descargo legal e interfaz gráfica para campo. |

Total: **8 Historias de Usuario**, **25 Criterios de Aceptación**, **21 Story Points**.

---

## Puertas de Calidad (Quality Gates) para M3

1. **Gate 1: Especificación y Contratos (SDD):** Cada HU debe contar con su especificación, criterios de aceptación Gherkin y tareas trazadas en Spec Kit antes de codificar.
2. **Gate 2: Verificación de Código y Tipado:** Cohesión estricta en contratos de datos con type hints y docstrings en todas las funciones públicas.
3. **Gate 3: Calidad Estática:** `uv run ruff check .` y `uv run ruff format --check .` sin observaciones.
4. **Gate 4: Verificación Funcional:** `uv run pytest -v` con 100% de pruebas pasando sin advertencias.
5. **Gate 5: Revisión Cruzada:** Checklist de revisor completo en el PR y aprobación explícita de un par.

---

## Gobernanza y Enmiendas
- La presente Constitución tiene rango supremo sobre cualquier convención no documentada.
- Cualquier modificación a los principios, responsabilidades, criterios de aceptación o umbrales de cobertura requiere consenso unánime de los cuatro integrantes del Grupo 2 y su debido registro en el historial de enmiendas.

**Versión**: 1.0.0 | **Ratificado**: 2026-11-12 | **Última Enmienda**: 2026-11-12
