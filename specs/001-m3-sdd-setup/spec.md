# Feature Specification: M3-G2 — Configuración Compartida de Gobernanza, Spec Kit, Skills y Herramientas

**Feature Branch**: `feature/m3-sdd-setup` (`001-m3-sdd-setup`)
**Created**: 2026-11-12
**Status**: Ready for Review / Validated
**Input**: Requisitos formales del Módulo 3, compromisos aprobados en Plantilla.pdf (M2), 8 Historias de Usuario, 25 Criterios de Aceptación, 21 Story Points y directrices de gobernanza de agentes.

---

## 1. Resumen Ejecutivo y Propósito
El objetivo de esta unidad es dejar preparado el repositorio del Grupo 2 (Universidad Autónoma de Occidente) para que sus cuatro integrantes adopten de forma unificada la metodología Spec-Driven Development (SDD), la Constitución del proyecto, las directrices operativas de agentes (`AGENTS.md`), la diagramación arquitectónica profesional con Archify, el control de seguridad de skills con SkillSpector, la memoria técnica con Engram MCP y el flujo estricto de Gitflow y revisión por PR.

Asimismo, se incorpora formalmente la totalidad del backlog aprobado en el Módulo 2 (8 Historias de Usuario, 25 Criterios de Aceptación Gherkin y 21 Story Points) como línea base viva para la ejecución técnica del Módulo 3 en inferencia CPU, FastAPI, Streamlit y Pytest AAA.

---

## 2. Matriz de Trazabilidad del Backlog Oficial (M2 ➔ M3)

| ID HU | Ticket | Rol / Especialidad | Responsable Humano | SP | Componente / Archivos | Criterio de Éxito Principal |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **HU-01** | #4 | DevOps | Santiago Correa | 2 | `pyproject.toml`, `uv.lock`, `.specify/` | `uv sync` y `ruff check` sin advertencias (código 0). Sin `pip` ni `requirements.txt`. |
| **HU-02** | #5 | ML | José Silva | 3 | `src/preprocessing.py` | Entrada validada; tensor normalizado $[1, 3, 224, 224]$ (`torch.float32`, media/std ImageNet). Excepción `InvalidImageFormatException`. |
| **HU-03** | #6 | ML | Jhonatan Tapia | 3 | `src/model_loader.py`, `src/inference.py` | Carga local de `model.safetensors` sin descargas runtime; inferencia CPU con `torch.no_grad()`; meta inferencia pura $< 300$\,ms ($N=1$). |
| **HU-04** | #7 | Backend | John Restrepo | 2 | `src/postprocessing.py`, `src/labels.py` | Vector Softmax ($1.000 \pm 0.001$), 38 clases en español, Top-3, filtro $\tau=0.60$ ("Muestra con incertidumbre alta") y descargo agronómico no prescriptivo. |
| **HU-05** | #8 | Backend | Jhonatan Tapia | 3 | `api/main.py`, `api/schemas.py` | Endpoints `GET /health` (200), `POST /predict` (meta E2E $p95 < 450$\,ms) y `GET /docs` OpenAPI interactivo. |
| **HU-06** | #9 | Frontend | John Restrepo | 3 | `ui/app.py`, `ui/api_client.py` | Carga interactiva JPG/JPEG/PNG, barra porcentual, gráfico Top-3, alerta si certeza $< 0.60$ y manejo robusto de errores sin colapso de sesión. |
| **HU-07** | #10 | Testing | Santiago Correa | 3 | `tests/unit/`, `tests/integration/` | Suite unitaria en $< 10$\,s con mocks; suite de integración E2E con TestClient; cobertura combinada $\ge 85\%$ en `src/` y `api/`. |
| **HU-08** | #11 | DevOps | José Silva | 2 | `Dockerfile`, `docker-compose.yml` | Construcción de paquete Wheel (`uv build`) y contenedor Docker CPU multi-etapa validado con `GET /health` HTTP 200. *(Nota: Implementación aplazada a M4 según alcance de unidad).* |

**Total Acumulado:** 8 Historias de Usuario, 25 Criterios de Aceptación, 21 Story Points.

---

## 3. Historias de Usuario y Escenarios de Aceptación (Gherkin)

### HU-01: Entorno Industrial y Tooling Base
- **Responsable:** Santiago Correa (DevOps) | **Estimación:** 2 SP | **Ticket:** #4 | **Prioridad:** P1
- **Narrativa:** *Como* Ingeniero MLOps, *quiero* inicializar el repositorio con estructura `src/` layout, `pyproject.toml`, gestor `uv` y linters `ruff`, *para* garantizar un entorno aislado, determinista y auditable desde el primer commit.
- **Escenarios de Aceptación:**
  1. **AC1.1:** **Dado** el archivo `uv.lock`, **cuando** se ejecuta `uv sync`, **entonces** se resuelve e instalan las dependencias completas sin errores.
  2. **AC1.2:** **Dado** el código fuente, **cuando** corren `uv run ruff check .` y `uv run ruff format --check .`, **entonces** salen con código 0.
  3. **AC1.3:** **Dado** el repositorio, **cuando** se audita la gestión de paquetes, **entonces** se prohíben `requirements.txt` e invocaciones directas a `pip`.

---

### HU-02: Preprocesamiento y Contratos de Tensores
- **Responsable:** José Silva (ML) | **Estimación:** 3 SP | **Ticket:** #5 | **Prioridad:** P1
- **Narrativa:** *Como* Desarrollador de Visión Computacional, *quiero* implementar la ingestión y preprocesamiento en `src/preprocessing.py`, *para* validar la entrada y transformarla en tensores normalizados compatibles con DINOv2.
- **Escenarios de Aceptación:**
  1. **AC2.1:** **Dado** un archivo no imagen o corrupto, **cuando** se procesa la entrada, **entonces** arroja la excepción `InvalidImageFormatException` (HTTP 400).
  2. **AC2.2:** **Dada** una imagen RGB válida, **cuando** se procesa, **entonces** se redimensiona bicúbicamente al tensor exacto $[1, 3, 224, 224]$ (`torch.float32`).
  3. **AC2.3:** **Dado** el tensor reescalado, **cuando** se aplica normalización ImageNet, **entonces** usa media $\mu = [0.485, 0.456, 0.406]$ y desviación $\sigma = [0.229, 0.224, 0.225]$.

---

### HU-03: Carga Segura e Inferencia en CPU
- **Responsable:** Jhonatan Tapia (ML) | **Estimación:** 3 SP | **Ticket:** #6 | **Prioridad:** P1
- **Narrativa:** *Como* Ingeniero de Backend/ML, *quiero* implementar la carga SafeTensors e inferencia en `src/model_loader.py` e `src/inference.py`, *para* ejecutar predicciones deterministas en CPU sin descargas en runtime.
- **Escenarios de Aceptación:**
  1. **AC3.1:** **Dado** el archivo local `model.safetensors`, **cuando** inicia el cargador, **entonces** carga exclusivamente pesos locales sin conexión a red en runtime.
  2. **AC3.2:** **Dado** un tensor de entrada validado, **cuando** se ejecuta la inferencia, **entonces** opera con `torch.no_grad()` sin construcción de grafos de autogradiente.
  3. **AC3.3:** **Dado** un lote unitario ($N=1$) en CPU de referencia (2 vCPUs) bajo protocolo de calentamiento y repeticiones a ejecutar, **cuando** se compute la inferencia pura en CPU, **entonces** el criterio se dará por cumplido si la latencia obtenida resulta $< 300$\,ms.

---

### HU-04: Mapeo Taxonómico y Filtro de Incertidumbre
- **Responsable:** John Restrepo (Backend) | **Estimación:** 2 SP | **Ticket:** #7 | **Prioridad:** P2
- **Narrativa:** *Como* Especialista Agrícola, *quiero* un módulo en `src/postprocessing.py` y `src/labels.py` que traduzca las 38 clases a español, filtre baja certeza ($\tau = 0.60$) y adjunte descargo agronómico, *para* dar soporte orientativo no prescriptivo.
- **Escenarios de Aceptación:**
  1. **AC4.1:** **Dado** el vector de logits ($38$ clases), **cuando** se convierte vía Softmax, **entonces** genera probabilidades que suman estrictamente $1.000 \pm 0.001$.
  2. **AC4.2:** **Dadas** las probabilidades, **cuando** opera el mapeo, **entonces** retorna salida estructurada con Top-$3$, nombre común del cultivo, patógeno y agente causal.
  3. **AC4.3:** **Dada** una probabilidad máxima $< 0.60$, **cuando** actúa el filtro, **entonces** el sistema etiqueta la salida *"Muestra con incertidumbre alta / Muestra atípica"*.
  4. **AC4.4:** **Dado** cualquier resultado de cribado, **cuando** se emite la salida, **entonces** incluye obligatoriamente advertencia que prohíbe prescribir agroquímicos.

---

### HU-05: API REST Asíncrona con FastAPI
- **Responsable:** Jhonatan Tapia (Backend) | **Estimación:** 3 SP | **Ticket:** #8 | **Prioridad:** P2
- **Narrativa:** *Como* Integrador de Sistemas, *quiero* exponer un servicio web con FastAPI en `api/main.py`, *para* permitir que clientes consuman el modelo mediante contratos JSON formales y validados.
- **Escenarios de Aceptación:**
  1. **AC5.1:** **Dado** el servicio FastAPI activo, **cuando** se invoca `GET /health`, **entonces** retorna código 200 y JSON con el estado del servicio y modelo cargado.
  2. **AC5.2:** **Dado** un envío *multipart/form-data* bajo protocolo de evaluación ($N=1$, calentamiento y repeticiones a ejecutar), **cuando** se compute la latencia E2E en `POST /predict`, **entonces** el criterio se dará por cumplido si el percentil satisface $p95 < 450$\,ms.
  3. **AC5.3:** **Dado** el servicio FastAPI en ejecución, **cuando** se accede a la ruta `/docs`, **entonces** despliega la documentación OpenAPI/Swagger interactiva y validada.

---

### HU-06: Interfaz Gráfica para Técnicos de Campo
- **Responsable:** John Restrepo (Frontend) | **Estimación:** 3 SP | **Ticket:** #9 | **Prioridad:** P3
- **Narrativa:** *Como* Técnico Agrícola, *quiero* interactuar con una interfaz Streamlit en `ui/app.py`, *para* cargar imágenes foliares, visualizar el cribado fitosanitario y analizar gráficamente las probabilidades.
- **Escenarios de Aceptación:**
  1. **AC6.1:** **Dada** la interfaz en Streamlit, **cuando** se realiza carga interactiva mediante *drag-and-drop*, **entonces** el sistema admite formatos JPG, JPEG y PNG.
  2. **AC6.2:** **Dada** la respuesta JSON, **cuando** se renderiza la vista, **entonces** muestra barra porcentual y gráfico Top-$3$, alertando si la certeza es $< 0.60$ ($\tau = 0.60$).
  3. **AC6.3:** **Dado** un error de red o archivo no válido, **cuando** se maneja la excepción, **entonces** muestra un mensaje descriptivo sin colapsar la sesión web.

---

### HU-07: Suite de Pruebas Automatizadas
- **Responsable:** Santiago Correa (Testing) | **Estimación:** 3 SP | **Ticket:** #10 | **Prioridad:** P1
- **Narrativa:** *Como* Líder de QA, *quiero* una suite integral con `pytest` cubriendo pruebas unitarias e integración de API, *para* blindar la estabilidad del sistema ante regresiones de código.
- **Escenarios de Aceptación:**
  1. **AC7.1:** **Dada** la suite unitaria (`tests/unit/`) aislada mediante mocks, **cuando** se ejecuta `pytest`, **entonces** finaliza en $< 10$\,segundos.
  2. **AC7.2:** **Dada** la suite de integración (`tests/integration/`), **cuando** corre `pytest`, **entonces** valida el pipeline completo con el modelo real y cliente FastAPI.
  3. **AC7.3:** **Dada** la suite completa, **cuando** se mide cobertura combinada (`pytest --cov`), **entonces** resulta igual o superior al $85\%$ en `src/` y `api/`.

---

### HU-08: Contenerización Docker y Paquete Wheel
- **Responsable:** José Silva (DevOps) | **Estimación:** 2 SP | **Ticket:** #11 | **Prioridad:** P3 (Alcance M4)
- **Narrativa:** *Como* Ingeniero de Despliegue, *quiero* construir la imagen Docker multi-etapa y el paquete Wheel con `uv build`, *para* permitir el despliegue desacoplado y reproducible en servidores productivos.
- **Escenarios de Aceptación:**
  1. **AC8.1:** **Dado** `pyproject.toml`, **cuando** se ejecuta `uv build`, **entonces** genera exitosamente los archivos `.whl` y `.tar.gz` en `dist/`.
  2. **AC8.2:** **Dada** la imagen Docker construida y activa, **cuando** se consulta `curl http://localhost:8000/health`, **entonces** responde exitosamente con HTTP 200.
  3. **AC8.3:** **Dado** `docker-compose.yml`, **cuando** se despliegan los contenedores, **entonces** opera la orquestación unificada de API y Streamlit en red interna compartida.
- *Nota de delimitación M3:* La ejecución de HU-08 queda diferida para el Módulo 4 de acuerdo con la planificación académica.

---

## 4. Escenario de Gobernanza SDD y Tooling (M3-G2)
- **Objetivo de Infraestructura:** Dotar al equipo de gobernanza compartida, plantillas, memoria técnica y diagramación verificada sin vulnerabilidades.
- **Escenarios de Validación:**
  1. **AC-G2.1:** **Dado** el repositorio clonado, **cuando** se inspecciona la configuración de Specify, **entonces** se encuentran inicializadas las plantillas y comandos de Gemini sin alterar ramas Git de forma autónoma.
  2. **AC-G2.2:** **Dada** la Constitución en `.specify/memory/constitution.md` y `AGENTS.md`, **cuando** se auditan sus principios, **entonces** reflejan la jerarquía de roles (Santiago, José, Jhonatan, John), límites WIP, cobertura $\ge 85\%$ y prohibición de notebooks o `pip`.
  3. **AC-G2.3:** **Dada** la skill Archify, **cuando** se somete al análisis de SkillSpector, **entonces** no presenta hallazgos CRITICAL ni HIGH antes de su activación en el espacio de trabajo.
  4. **AC-G2.4:** **Dado** el modelo arquitectónico generado, **cuando** se almacena en `docs/architecture/`, **entonces** se dispone tanto de formato HTML interactivo como de imagen visualizable que separa componentes implementados de planificados.
  5. **AC-G2.5:** **Dada** la guía de preparación (`docs/getting-started.md`), **cuando** un compañero de equipo la ejecuta en Windows, **entonces** reproduce el entorno con `uv`, Spec Kit y memoria técnica sin requerir dependencias globales adicionales.
