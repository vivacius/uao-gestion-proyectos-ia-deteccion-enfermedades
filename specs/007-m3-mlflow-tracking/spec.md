# Especificación Técnica (Spec Kit): SPEC-007 Integración de MLflow Tracking y Model Registry

**Identificador:** `SPEC-007`  
**Feature Branch:** `feature/m3-mlflow-tracking`  
**Unidad de Trabajo:** `M3-IMP-MLF-01`  
**Issue Asociado:** Issue [#28](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/28)  
**Responsable Principal:** Grupo 2 — MLOps / ML  
**Revisor de Código:** Jhonatan Andrés Tapia Córdoba (Code Reviewer)  
**Fecha:** 2026-11-13  
**Estado:** Implementado y Verificado (Listo para Revisión)

---

## 1. Propósito y Contexto del Negocio

El **Anuncio 007** del curso asigna un **20% de la calificación del Módulo 3 (M3)** a la integración y demostración de **MLflow** en el ciclo de vida del modelo de aprendizaje profundo para detección fitosanitaria.

Esta especificación formaliza la integración mínima verificable y reproducible de MLflow para el modelo **DINOv2-small** (`rodynaemad/plant-disease-dinov2-small`) operando localmente en CPU con pesos SafeTensors, asegurando:
1. Servidor de tracking y UI activo en `http://127.0.0.1:5050`.
2. Tres ejecuciones (*runs*) comparables y genuinamente distintas sobre un conjunto fijo de evaluación.
3. Registro riguroso de parámetros, métricas reales de latencia/rendimiento CPU, artefactos estructurados y tags de trazabilidad.
4. Registro del modelo en el *Model Registry* local de MLflow con versión trazable al modelo servido por FastAPI.
5. Preservación estricta de las puertas de calidad: suite unitaria intacta (162 passed, 2 skipped), cero advertencias en Ruff, y ausencia de regresiones o conflictos con los PRs abiertos (#25, #26, #27).

---

## 2. Delimitación y Restricciones Técnicas

1. **Gestor de Dependencias:** Uso exclusivo de `uv` (`uv add`) bajo Python 3.13. Se prohíbe taxativamente `pip` directo o la creación de `requirements.txt`.
2. **Código Separado:** El script de orquestación y evaluación de MLflow reside en `scripts/` o `src/evaluation/`, completamente desacoplado del código productivo de la API (`api/main.py`) para evitar impactos de latencia en runtime.
3. **No Invención de Métricas:** Al no existir un dataset de prueba con etiquetas verdaderas (*ground-truth labels*) dentro del repositorio, no se inventarán métricas de exactitud (*accuracy*) ni F1-score. Se registrará explícitamente `is_labeled = False` y se reportarán métricas empíricas de desempeño computacional: latencia media, mediana, p95, throughput (imágenes/segundo), distribución de confianza y tasa de incertidumbre fitosanitaria.
4. **Protección Git:** Ninguna base de datos SQLite (`mlflow.db`), directorio de artefactos (`mlruns/`, `mlartifacts/`) ni pesos pesados será comiteada al repositorio. Se refuerza `.gitignore`.

---

## 3. Escenarios de Aceptación (Gherkin)

### Escenario 1: Servidor de Tracking y UI Activo en Puerto 5050
- **Dado** el entorno virtual gestionado por `uv` con la dependencia de `mlflow`,
- **Cuando** se levanta el servidor de tracking local con `uv run mlflow server --port 5050`,
- **Entonces** el servidor responde exitosamente en `http://127.0.0.1:5050`, con backend SQLite local y directorio de artefactos reproducible.

### Escenario 2: Tres Runs Experimentales Comparables y Genuinos
- **Dado** el modelo DINOv2-small local en CPU y un conjunto fijo de imágenes de evaluación,
- **Cuando** se ejecuta el script de experimentación y evaluación con MLflow,
- **Entonces** se registran exactamente 3 runs en el experimento `dinov2-plant-disease-screening`:
  1. *Run 1 (Baseline Screening)*: Umbral de confianza $\tau = 0.60$, $k = 3$.
  2. *Run 2 (Strict Agronomic)*: Umbral de confianza $\tau = 0.80$, $k = 3$.
  3. *Run 3 (Exploratory Permissive)*: Umbral de confianza $\tau = 0.40$, $k = 5$.

### Escenario 3: Parámetros, Métricas y Tags Fidedignos
- **Dado** cada uno de los 3 runs ejecutados,
- **Cuando** se inspeccionan sus metadatos registrados en MLflow,
- **Entonces** se constata que:
  - **Parámetros**: `model_name`, `device` (cpu), `confidence_threshold` ($\tau$), `top_k`, `image_size` (224x224), `interpolation`, `is_labeled` (False), `eval_samples_count`.
  - **Métricas**: `latency_mean_ms`, `latency_p50_ms`, `latency_p95_ms`, `throughput_img_per_sec`, `uncertainty_rate`, `mean_top1_confidence`.
  - **Tags**: `version`, `environment` (local-cpu), `license` (MIT), `git_commit`, `architecture`, `unit` (M3-IMP-MLF-01).

### Escenario 4: Artefactos Registrados y Verificables
- **Dado** la culminación de cada run experimental,
- **Cuando** se consulta la pestaña de artefactos en la UI de MLflow,
- **Entonces** existen archivos descargables e inspeccionables:
  - `predictions.json` (resumen estructurado de predicciones por imagen).
  - `predictions_summary.csv` (tabla exportable con clases predichas, probabilidad y bandera de incertidumbre).
  - `run_report.json` (resumen ejecutivo con metadatos del hardware y entorno de ejecución).

### Escenario 5: Registro del Modelo en Model Registry
- **Dado** el modelo base validado de DINOv2-small,
- **Cuando** concluye la evaluación del run de referencia (Baseline),
- **Entonces** el modelo se registra en el *Model Registry* bajo el nombre `dinov2-plant-disease-classifier`, generando una versión formal (Version 1) con descripción, etiquetas y esquema de inferencia PyFunc trazable al modelo consumido por FastAPI.

### Escenario 6: Ausencia de Regresiones y Puertas de Calidad
- **Dado** el repositorio con la integración de MLflow,
- **Cuando** se ejecutan `uv run pytest tests/unit/`, `uv run ruff check .` y `uv run ruff format --check .`,
- **Entonces** todas las pruebas unitarias pasan sin fallas (162 passed, 2 skipped), el formateo y linteo retornan código de salida 0, y no se generan conflictos con PR #25, #26 ni #27.
