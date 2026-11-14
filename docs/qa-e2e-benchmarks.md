# Reporte Empírico de Validación Integral E2E y Benchmarks en CPU (M3)

**Unidad:** `SC-02` | **Spec:** [`specs/008-m3-e2e-benchmarks/spec.md`](../specs/008-m3-e2e-benchmarks/spec.md)  
**Issue:** [#30](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/30)  
**Responsable:** Santiago Correa Campaña (`@vivacius`)  
**Fecha de ejecución:** 2026-11-13  
**Base verificada:** `develop` (`c51e3fb`)

---

## 1. Entorno de Hardware y Software Medido

| Parámetro | Valor Observado |
| :--- | :--- |
| **Sistema Operativo** | `Windows-11-10.0.26200-SP0` |
| **Procesador / CPUs** | `Intel64 Family 6 Model 141 Stepping 1, GenuineIntel` (`12` CPUs lógicas) |
| **Python / Gestor** | `Python 3.13.18` · `uv sync --frozen` (sin `pip`) |
| **Modelo / Arquitectura** | `rodynaemad/plant-disease-dinov2-small` (`Dinov2ForImageClassification`, `38` clases) |
| **Memoria RAM (RSS con modelo cargado)** | **`459.64 MB`** *(meta `< 1.8 GB`)* |

---

## 2. Calidad Estática y Suite de Pruebas (`ruff` y `pytest`)

| Verificación | Comando | Resultado Real |
| :--- | :--- | :--- |
| **Ruff Lint** | `uv run ruff check .` | `All checks passed!` (código `0`) |
| **Ruff Format** | `uv run ruff format --check .` | `67 files already formatted` (código `0`) |
| **Pruebas Unitarias** | `uv run pytest tests/unit -v --cov=src --cov=api --cov-report=term-missing` | **`176 passed, 1 skipped`** (`177` recopiladas en `32.70 s`) *(1 omitida en sandbox por ruta Tcl/Tk)* |
| **Cobertura (`src/` + `api/`)** | `pytest --cov=src --cov=api` | **`98 %`** (`421` sentencias, `9` sin cubrir) |
| **Pruebas de Integración** | `uv run pytest tests/integration -v` | **`6 passed in 12.05 s`** (DINOv2 real en CPU + FastAPI) |

---

## 3. Validación Funcional E2E (Frontend Estático + FastAPI + DINOv2 CPU)

Ejecutado con [`scripts/validate_e2e_and_benchmark.py`](../scripts/validate_e2e_and_benchmark.py) levantando un servidor real `uvicorn api.main:app --host 127.0.0.1 --port 8011`:

| Ruta / Caso | Código HTTP | Verificación Observada |
| :--- | :---: | :--- |
| `GET /` | `200` | Sirve interfaz web HTML (`text/html`, `ui/web/static/`) |
| `GET /health` | `200` | `status="ok"`, `model_available=True`, `device="cpu"`, `num_classes=38` |
| `GET /model-info` | `200` | `model_name="rodynaemad/plant-disease-dinov2-small"`, `Dinov2ForImageClassification` |
| `GET /docs` | `200` | Documentación interactiva Swagger / OpenAPI disponible |
| `POST /predict` (JPEG válida) | `200` | Retorna Top-3 (`top_k_count=3`), `confidence_percentage=32.38`, `disclaimer` agronómico presente |
| `POST /predict` (bytes corruptos) | `400` | Rechazo controlado (`CorruptedImageError`) sin caída del servidor |
| `POST /predict` (formato `.gif`) | `415` | Rechazo controlado (`UnsupportedImageFormatError`) |

---

## 4. Benchmarks de Latencia en CPU vs. HTTP E2E

Protocolo: **3 corridas de calentamiento** seguidas de **$N=20$ mediciones** sobre imagen sintética JPEG ($300 \times 300\text{ px}$).

| Escenario | N | Min (ms) | Media (ms) | p50 (ms) | **p95 (ms)** | Max (ms) | Throughput (req/s) | Meta Contractual |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Inferencia pura CPU (`predict_from_bytes`)** | 20 | 49.33 | 66.10 | 66.19 | **77.33** | 89.29 | 15.13 | `< 300 ms` ✅ |
| **HTTP E2E secuencial (`POST /predict`)** | 20 | 60.64 | 70.01 | 69.21 | **81.39** | 84.95 | 14.28 | `p95 < 450 ms` ✅ |
| **HTTP E2E concurrente (`4 workers`)** | 20 | 76.42 | 264.86 | 285.59 | **314.60** | 317.25 | 14.11 | `p95 < 450 ms` ✅ |

---

## 5. Limitaciones y Observaciones
1. Los tiempos anteriores se midieron sobre una hoja sintética JPEG de $300 \times 300\text{ px}$ en hardware Intel de 12 CPUs lógicas; en CPUs con menos núcleos o bajo concurrencia mayor pueden variar.
2. Las predicciones sobre imágenes sintéticas sirven exclusivamente para validación técnica de latencia, serialización y estabilidad, **no** para medir *accuracy* o *Macro F1* clínico/agronómico.
3. Este script complementa (sin duplicar ni alterar) la experimentación MLflow registrada en `scripts/run_mlflow_benchmark.py` (`SPEC-007`).
