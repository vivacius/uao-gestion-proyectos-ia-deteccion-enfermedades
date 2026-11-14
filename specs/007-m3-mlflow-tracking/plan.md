# Plan de Implementación (Spec Kit): SPEC-007 Integración de MLflow Tracking y Model Registry

**Identificador:** `SPEC-007`  
**Feature Branch:** `feature/m3-mlflow-tracking`  
**Issue Asociado:** Issue [#28](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/28)  
**Spec Asociada:** [spec.md](./spec.md)  
**Fecha:** 2026-11-13

---

## 1. Arquitectura y Enfoque Técnico

El objetivo es incorporar **MLflow** para la sustentación del Módulo 3 sin modificar la lógica interna de producción de FastAPI (`api/main.py`) ni los módulos nucleares de inferencia (`src/inference.py`, `src/model_loader.py`), manteniéndolos limpios de dependencias innecesarias de tracking durante el servicio en vivo.

```
┌────────────────────────────────────────────────────────┐
│             Arquitectura de Experimentación            │
└────────────────────────────────────────────────────────┘
                    │
                    ▼
     scripts/run_mlflow_benchmark.py
                    │
         ┌──────────┴──────────┐
         │                     │
         ▼                     ▼
   src.inference         MLflow Tracking Client
  (DINOv2 CPU Real)            │
         │                     ├── Parámetros (tau, top_k, CPU)
         │                     ├── Métricas (latencia, p95, throughput)
         │                     ├── Artefactos (csv, json, report)
         │                     └── Tags (git commit, versión, licencia)
         │                     │
         └─────────────────────┼─────────► Model Registry
                               ▼           ("dinov2-plant-disease-classifier")
                         MLflow Server
                      (http://127.0.0.1:5050)
                      backend: sqlite:///mlruns.db
```

### Componentes a Crear / Modificar:
1. **`pyproject.toml` / `uv.lock`:** Incorporar `mlflow` mediante `uv add mlflow` asegurando compatibilidad con Python 3.13.
2. **`.gitignore`:** Reforzar exclusión de directorios locales de MLflow (`mlruns/`, `mlartifacts/`, `*.db`).
3. **`scripts/run_mlflow_benchmark.py`:**
   - Script de orquestación autónomo que inicializa el experimento `dinov2-plant-disease-screening`.
   - Carga el conjunto fijo de imágenes de prueba (sintéticas reproducibles y de catálogo).
   - Ejecuta los 3 runs comparables:
     - Run 1: Baseline ($\tau = 0.60$, $k = 3$)
     - Run 2: Strict Agronomic ($\tau = 0.80$, $k = 3$)
     - Run 3: Exploratory Permissive ($\tau = 0.40$, $k = 5$)
   - Mide latencia individual con `time.perf_counter_ns()`, calcula p50, p95, media y throughput.
   - Genera artefactos: `predictions.json`, `predictions_summary.csv` y `benchmark_report.json`.
   - Empaqueta el modelo con wrapper `mlflow.pyfunc.PythonModel` conectado a `src.inference.predict_from_bytes` y lo registra en el *Model Registry* como `dinov2-plant-disease-classifier`.
4. **`tests/unit/test_mlflow_benchmark.py`:** Pruebas unitarias de aislamiento para validar la lógica del script de benchmark sin requerir levantar el servidor HTTP de MLflow en la suite continua.
5. **Documentación e Instrucciones:** Instrucciones paso a paso para arranque de UI en puerto 5050 e inspección de runs.

---

## 2. Gestión de Riesgos y Control de Conflictos

| Riesgo Identificado | Estrategia de Mitigación |
| :--- | :--- |
| **Conflicto con PR #26 en `pyproject.toml`** | PR #26 retira Streamlit y agrega herramientas de Docker/Wheel. Nuestra rama añade `mlflow` al `pyproject.toml` base de `origin/develop`. Se documenta el diff puntual para facilitar un rebase limpio posterior si PR #26 es fusionado primero por el equipo humano. |
| **Descarga indebida durante tests** | Pruebas de MLflow usarán mocks o el modelo local ya existente con `local_files_only=True`. Ningún test requerirá conexión a internet. |
| **Inyección de métricas falsas** | Al no haber ground-truth de validación en el repo, se explicita `is_labeled: False` y no se calculan Accuracy ni F1 ficticios. |
| **Fugas de base SQLite o pesos** | Validación de `.gitignore` previo al commit. Verificación de `git status` antes de cualquier entrega. |

---

## 3. Plan de Verificación

1. `uv run ruff check .` y `uv run ruff format --check .` (0 errores).
2. `uv run pytest tests/unit/` (162 passed, 2 skipped intactos + nuevas pruebas unitarias pasando).
3. Ejecución controlada de `scripts/run_mlflow_benchmark.py` apuntando a `sqlite:///mlflow_tracking.db`.
4. Levantamiento y verificación de UI en `http://127.0.0.1:5050`.
5. Inspección visual y programática de los 3 runs y del modelo registrado en el Registry.
