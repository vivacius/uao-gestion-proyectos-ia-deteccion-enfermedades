# Plan de Implementación (Spec Kit): SPEC-009 Model Card Fitosanitaria

**Feature Branch:** `feature/m3-model-card`  
**Issue:** #29 | **Spec:** [spec.md](./spec.md)  
**Responsable:** John Restrepo Aparicio (`@JohnRestrepo-coder`)

---

## Fases de Ejecución

### Fase A: Preparación y Validación de Línea Base
1. Confirmar sincronización de `develop` en HEAD `734fbdf` y conmutar a la rama de trabajo `feature/m3-model-card`.
2. Verificar no alteración de archivos de código ni de especificaciones previas (`specs/001` a `008`).
3. Auditar fuentes empíricas: `docs/qa-e2e-benchmarks.md`, `scripts/run_mlflow_benchmark.py`, `src/labels.py`, `LICENSE` y `config.json`.

### Fase B: Redacción de la Model Card Oficial (`docs/model-card.md`)
1. Estructurar el documento conforme a las 9 secciones canónicas de Mitchell et al. (2019):
   - **Sección 1 — Detalles del Modelo:** Arquitectura, formato SafeTensors, autores, fecha y licencias.
   - **Sección 2 — Uso Previsto y Alcance:** Casos de uso válidos (cribado de apoyo) y casos explícitamente fuera de alcance / prohibidos (prescripción química automática).
   - **Sección 3 — Factores de Evaluación:** Variaciones fenotípicas, factores lumínicos y condiciones ambientales.
   - **Sección 4 — Métricas y Honestidad Científica:** Métricas de latencia computacional real en CPU (min, media, p50, p95, throughput), RAM y justificación estricta de ausencia de accuracy/F1 por evaluación sobre muestras sintéticas sin ground truth.
   - **Sección 5 — Datos de Evaluación:** Características del conjunto sintético de 10 muestras y pruebas de estrés HTTP.
   - **Sección 6 — Datos de Entrenamiento:** PlantVillage (54,306 imágenes, 14 cultivos, 38 condiciones) y sesgo de laboratorio.
   - **Sección 7 — Análisis Cuantitativos:** Tablas consolidadas de rendimiento en CPU pura, HTTP secuencial y HTTP concurrente (4 workers).
   - **Sección 8 — Consideraciones Éticas y Mitigación de Sesgos:** Análisis de 4 ejes críticos (iluminación, ángulo/enfoque, síntomas cruzados, brecha de laboratorio vs. campo) e impacto socioeconómico en pequeños productores.
   - **Sección 9 — Advertencias y Recomendaciones:** Protocolo operativo de campo, rol del umbral $\tau=0.60$ y validación humana obligatoria.

### Fase C: Integración Documental y Quality Gate
1. Enlazar `docs/model-card.md` en [README.md](../../README.md) en la sección de arquitectura / documentación técnica sin generar conflictos.
2. Ejecutar validaciones estáticas y suite de pruebas:
   - `uv run ruff check .`
   - `uv run ruff format --check .`
   - `uv run pytest tests/unit`

### Fase D: Entrega y Pull Request
1. Crear commit bajo Conventional Commits: `docs(model-card): elaborar Model Card fitosanitaria en docs/model-card.md (Issue #29, SPEC-009)`.
2. Publicar rama `feature/m3-model-card` a `origin`.
3. Abrir Pull Request hacia `develop` usando `.github/PULL_REQUEST_TEMPLATE.md` asignando a `@JhonatanTC99` y `@vivacius`.
