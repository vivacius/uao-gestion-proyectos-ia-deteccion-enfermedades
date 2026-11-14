# Especificación Técnica (Spec Kit): SC-02 Validación Integral E2E y Benchmarks en CPU

**Feature Branch:** `feature/sc02-e2e-benchmarks`  
**Issue Asociado:** [#30 — [M3-QA] Validación Integral E2E y Benchmarks de Latencia en CPU](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/30)  
**Responsable:** Santiago Correa Campaña (`@vivacius`)  
**Revisor Asignado:** Jhonatan Andrés Tapia Córdoba (`@JhonatanTC99`)  
**Fecha:** 2026-11-13

---

## 1. Propósito y Alcance
Validar de forma integral y reproducible el sistema completo en `develop` (`c51e3fb`): entorno `uv`, calidad Ruff, suite `pytest` (unitaria e integración), flujo E2E entre el frontend web estático (`ui/web/static/`) y FastAPI (`GET /`, `GET /health`, `GET /model-info`, `GET /docs`, `POST /predict`), manejo de errores HTTP y protocolo de benchmark en CPU midiendo por separado inferencia pura (`< 300 ms`) y latencia HTTP `p95` (`< 450 ms`), junto con consumo de RAM y CPU en Python 3.13.

> **Restricción de no duplicación:** Esta especificación no modifica `SPEC-006`, `SPEC-007`, `scripts/run_mlflow_benchmark.py`, `pyproject.toml`, `uv.lock`, `Dockerfile` ni `ui/web/`.

## 2. Escenarios de Aceptación (Gherkin)

### AC-E2E-01 — Pruebas de Carga y Latencia en CPU
- **Dado** el modelo `rodynaemad/plant-disease-dinov2-small` cargado localmente en CPU y el endpoint `POST /predict`,
- **Cuando** se ejecuta un protocolo reproducible tras calentamiento (inferencia pura directa y peticiones HTTP secuenciales y concurrentes),
- **Entonces** se miden y reportan por separado la latencia media/p95 de inferencia pura en CPU (meta `< 300 ms`) y la latencia HTTP E2E `p95` (meta `< 450 ms`).

### AC-E2E-02 — Integración Frontend-Backend y Manejo de Errores
- **Dado** el servicio FastAPI con el montaje web estático en `/` (`ui/web/static/`),
- **Cuando** se consultan `GET /`, `GET /health`, `GET /model-info`, `GET /docs`, y se envían a `POST /predict` imágenes válidas (JPG/PNG) e inválidas/corruptas,
- **Entonces** se verifica HTTP 200 con Top-3, campo de incertidumbre (`< 0.60`) si aplica o descargo agronómico, y respuestas HTTP 400/415 controladas sin caída del servidor.

### AC-E2E-03 — Reporte Empírico de Benchmarks y QA
- **Dado** el entorno Python 3.13 con `uv`,
- **Cuando** se documentan los resultados en `docs/qa-e2e-benchmarks.md`,
- **Entonces** se incluyen exclusivamente métricas reales observadas de latencia, RAM, CPU, Ruff y `pytest`, diferenciando hechos cumplidos de brechas si alguna meta no se alcanza.
