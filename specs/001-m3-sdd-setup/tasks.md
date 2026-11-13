# Tasks Breakdown: M3-G2 y Backlog M3 de Detección Fitosanitaria

**Feature**: `001-m3-sdd-setup` | **Fecha**: 2026-11-12 | **Spec**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

---

## Fase 1: Gobernanza, Spec Kit y Configuración Base (M3-G2)

- [x] **TSK-G2-01: Verificación de Precondiciones Git y Creación de Rama**
  - Consultar estado del PR #14 (Confirmado: `MERGED` en `develop`).
  - Validar aprobación explícita de un par distinto del autor (Confirmado: Dictamen de `vivacius`).
  - Actualizar `develop` mediante avance rápido (`fast-forward`) sin alterar `main`.
  - Crear rama de trabajo `feature/m3-sdd-setup`.
- [x] **TSK-G2-02: Inicialización e Infraestructura de Spec Kit (Specify 1.2.2)**
  - Inicializar Specify con `--integration gemini` y scripts de PowerShell.
  - Asegurar versionamiento de infraestructura compartida (`.specify/`, `.gemini/commands/`, plantillas).
  - Excluir archivos temporales y locales de agentes en `.gitignore`.
  - Evitar que los scripts de Spec Kit creen o cambien ramas Git automáticamente.
- [x] **TSK-G2-03: Constitución del Proyecto y Reglas de Agentes**
  - Redactar `.specify/memory/constitution.md` con los 5 principios base, roles (Santiago, José, Jhonatan, John), límites WIP, cobertura $\ge 85\%$ y prohibición de notebooks o `pip`.
  - Redactar `AGENTS.md` con la jerarquía Humano > Asistentes (GPT/Gemini), permisos, matriz de HUs y restricciones estrictas.
- [x] **TSK-G2-04: Incorporación del Backlog Formal y Ciclo SDD**
  - Registrar las 8 HU, 25 AC y 21 SP en `specs/001-m3-sdd-setup/spec.md`.
  - Ejecutar etapas SDD: `Specify` (`spec.md`), `Clarify` (`clarify.md`), `Plan` (`plan.md`), `Checklist` (`checklist.md`), `Tasks` (`tasks.md`) y `Analyze` (`analyze.md`).
- [x] **TSK-G2-05: Auditoría de Seguridad de Archify con SkillSpector**
  - Clonar/descargar repositorio oficial `tt-a1i/archify` registrando versión, commit y licencia.
  - Auditar la totalidad del paquete mediante escaneo estático local con SkillSpector (sin llamadas externas a LLMs).
  - Verificar ausencia de hallazgos CRITICAL o HIGH.
  - Habilitar la skill en el proyecto y comprobar descubrimiento por el agente.
- [x] **TSK-G2-06: Generación y Validación de Diagrama Arquitectónico**
  - Modelar la arquitectura actual en base a `src/`, `api/`, `ui/` y el flujo de inferencia DINOv2.
  - Diferenciar componentes implementados de previstos.
  - Exportar diagrama interactivo HTML y vista legible a `docs/architecture/`.
- [x] **TSK-G2-07: Configuración de Engram MCP, GGA y Guía de Reproducción**
  - Documentar configuración parametrizada de Engram MCP para memoria técnica por HU sin exponer bases locales ni credenciales.
  - Auditar compatibilidad y viabilidad de GGA para control preventivo de commits en Windows.
  - Crear guía de preparación (`docs/getting-started.md`) garantizando reproducibilidad.

---

## Fase 2: Tareas Técnicas del Backlog M3 (Trazabilidad 1:1 con HUs)

### HU-01: Entorno Industrial y Tooling Base (2 SP · Santiago Correa)
- [ ] **TSK-01-01:** Validar resolución limpia de dependencias con `uv sync` a partir de `uv.lock` (AC1.1).
- [ ] **TSK-01-02:** Asegurar salida con código 0 en `uv run ruff check .` y `uv run ruff format --check .` (AC1.2).
- [ ] **TSK-01-03:** Auditar repositorio para prohibir `requirements.txt` y llamadas a `pip` (AC1.3).

### HU-02: Preprocesamiento y Contratos de Tensores (3 SP · José Silva)
- [ ] **TSK-02-01:** Implementar manejo y validación de formatos en `src/preprocessing.py`, lanzando `InvalidImageFormatException` ante errores (AC2.1).
- [ ] **TSK-02-02:** Implementar redimensión bicúbica al tensor exacto $[1, 3, 224, 224]$ en formato `torch.float32` (AC2.2).
- [ ] **TSK-02-03:** Aplicar normalización con parámetros ImageNet ($\mu = [0.485, 0.456, 0.406]$, $\sigma = [0.229, 0.224, 0.225]$) (AC2.3).

### HU-03: Carga Segura e Inferencia en CPU (3 SP · Jhonatan Tapia)
- [ ] **TSK-03-01:** Implementar cargador seguro de SafeTensors en `src/model_loader.py` leyendo exclusivamente `model.safetensors` local sin conexión de red (AC3.1).
- [ ] **TSK-03-02:** Ejecutar inferencia en CPU bajo bloque `torch.no_grad()` sin grafos de autogradiente en `src/inference.py` (AC3.2).
- [ ] **TSK-03-03:** Protocolo de medición de latencia en CPU de referencia demostrando meta $< 300$\,ms para $N=1$ tras calentamiento (AC3.3).

### HU-04: Mapeo Taxonómico y Filtro de Incertidumbre (2 SP · John Restrepo)
- [ ] **TSK-04-01:** Implementar cálculo de probabilidades Softmax sumando estrictamente $1.000 \pm 0.001$ en `src/postprocessing.py` (AC4.1).
- [ ] **TSK-04-02:** Estructurar salida con Top-3, nombres comunes en español, patógeno y agente causal vía `src/labels.py` (AC4.2).
- [ ] **TSK-04-03:** Aplicar filtro de umbral $\tau = 0.60$ etiquetando como "Muestra con incertidumbre alta / Muestra atípica" cuando $P_{max} < 0.60$ (AC4.3).
- [ ] **TSK-04-04:** Incluir descargo de responsabilidad agronómica que prohíbe la prescripción de agroquímicos (AC4.4).

### HU-05: API REST Asíncrona con FastAPI (3 SP · Jhonatan Tapia)
- [ ] **TSK-05-01:** Crear servicio FastAPI con endpoint `GET /health` que devuelva HTTP 200 y JSON descriptivo del estado (AC5.1).
- [ ] **TSK-05-02:** Crear endpoint `POST /predict` para *multipart/form-data* validando esquema Pydantic y meta de latencia $p95 < 450$\,ms (AC5.2).
- [ ] **TSK-05-03:** Habilitar documentación OpenAPI interactiva en `/docs` con esquemas y respuestas tipadas (AC5.3).

### HU-06: Interfaz Gráfica para Técnicos de Campo (3 SP · John Restrepo)
- [ ] **TSK-06-01:** Construir frontend web desacoplado en `ui/web/` y aplicación de escritorio Tkinter en `ui/desktop_app.py`, con carga interactiva de archivos JPG, JPEG y PNG (AC6.1).
- [ ] **TSK-06-02:** Visualizar barra porcentual de confianza y gráfico Top-3, desplegando alerta si la certeza es menor a $0.60$ (AC6.2).
- [ ] **TSK-06-03:** Integrar clientes HTTP desacoplados (`ui/api_client.py` y `ui/web/app.js`) con manejo resiliente de errores sin colapso de la interfaz (AC6.3).

### HU-07: Suite de Pruebas Automatizadas (3 SP · Santiago Correa)
- [ ] **TSK-07-01:** Construir suite unitaria (`tests/unit/`) aislada con mocks y tiempo de corrida inferior a 10 segundos (AC7.1).
- [ ] **TSK-07-02:** Construir suite de integración (`tests/integration/`) con TestClient de FastAPI validando el flujo E2E real (AC7.2).
- [ ] **TSK-07-03:** Configurar medición de cobertura `pytest --cov` garantizando $\ge 85\%$ sobre `src/` y `api/` (AC7.3).

### HU-08: Contenerización y Empaquetado Wheel (2 SP · José Silva — Módulo 4, implementación local)
- [x] **TSK-08-01:** Generar artefactos `.whl` y `.tar.gz` en `dist/` usando `uv build` (AC8.1).
- [x] **TSK-08-02:** Construir imagen Docker multi-etapa para CPU y validar respuesta HTTP 200 en `GET /health` (AC8.2).
- [x] **TSK-08-03:** Orquestar el servicio de API mediante `docker-compose.yml` y validar la app de escritorio y el frontend web contra la API publicada (AC8.3).
