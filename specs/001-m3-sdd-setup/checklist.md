# Quality Checklist: Requisitos y Gobernanza M3 (Checklist)

**Feature**: `001-m3-sdd-setup` | **Fecha**: 2026-11-12 | **Referencia**: [spec.md](./spec.md)

Este checklist valida la completitud, claridad, testeabilidad y consistencia de los requisitos incorporados en el Spec Kit para el Módulo 3.

---

## 1. Completitud de Requisitos y Backlog

- [x] **8 Historias de Usuario (HU-01 a HU-08)** documentadas con su identificador formal, ticket asociado y título exacto de la propuesta M2.
- [x] **25 Criterios de Aceptación (AC1.1 a AC8.3)** redactados en formato Gherkin (Dado/Cuando/Entonces).
- [x] **21 Story Points** preservados en su totalidad, respetando la estimación aprobada por el docente y el equipo.
- [x] **Asignación de roles y responsables intacta:**
  - Santiago Correa: HU-01 (2 SP), HU-07 (3 SP)
  - José Silva: HU-02 (3 SP), HU-08 (2 SP)
  - Jhonatan Tapia: HU-03 (3 SP), HU-05 (3 SP)
  - John Restrepo: HU-04 (2 SP), HU-06 (3 SP)
- [x] **Delimitación explícita M3 vs M4:** HU-08 (Docker multi-etapa y paquete Wheel) marcada como alcance diferido para M4.

---

## 2. Claridad de Contratos y Restricciones Técnicas

- [x] **Entorno y Tooling:** Uso exclusivo de `uv` con Python 3.13. Prohibición de `pip` y `requirements.txt`.
- [x] **Contratos de Tensores:** Entrada RGB redimensionada bicúbicamente a $[1, 3, 224, 224]$, `torch.float32`, con media ImageNet $[0.485, 0.456, 0.406]$ y desviación $[0.229, 0.224, 0.225]$.
- [x] **Excepciones Formales:** `InvalidImageFormatException` (HTTP 400) ante archivos corruptos o extensiones no compatibles.
- [x] **Inferencia CPU Determinista:** Uso estricto de `safetensors.torch` para carga local, sin llamadas de red en runtime y evaluación bajo `torch.no_grad()`.
- [x] **Postprocesamiento y Negocio:** Vector Softmax sumando $1.000 \pm 0.001$, 38 clases en español, filtro de incertidumbre con umbral $\tau = 0.60$ y leyenda de descargo agronómico obligatorio (no prescriptivo).
- [x] **Servicio API:** FastAPI asíncrono con `GET /health` (200), `POST /predict` y `GET /docs` interactivo.
- [x] **Frontend:** frontend web desacoplado y aplicación de escritorio Tkinter con carga de archivos (JPG, JPEG, PNG), gráfico Top-3 y alerta de baja certeza.

---

## 3. Testeabilidad y Calidad de Código

- [x] **Suite de pruebas unitarias (`tests/unit/`):** Estructura AAA, dependencias aisladas mediante mocks y tiempo total $< 10$\,s.
- [x] **Suite de pruebas de integración (`tests/integration/`):** Validación E2E del pipeline con TestClient y modelo local.
- [x] **Umbral de cobertura:** Cobertura acumulada $\ge 85\%$ sobre `src/` y `api/`.
- [x] **Calidad estática:** `ruff check .` y `ruff format --check .` con código de salida 0.

---

## 4. Gobernanza y Seguridad de Herramientas

- [x] **Constitución y AGENTS.md:** Principios de supremacía humana, límites WIP = 1 por desarrollador, revisión obligatoria por un par y prohibición de notebooks.
- [x] **Protección de Datos y Pesos:** Exclusión en `.gitignore` de `model.safetensors`, `.venv/`, `.env`, secretos y bases SQLite locales.
- [x] **Seguridad de Skills:** Verificación estática con SkillSpector previa a la instalación de Archify en el entorno de desarrollo.
- [x] **Memoria Técnica y Control Git:** Configuración de Engram MCP documentada de forma reproducible sin acoplamiento de rutas de usuario ni publicación de bases de datos.
