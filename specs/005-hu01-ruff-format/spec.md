# Especificación Técnica (Spec Kit): HU-01 Entorno Reproducible y Calidad con Ruff

**Feature Branch:** `feature/hu01-ruff-format`  
**Historia Asociada:** HU-01 (Issue [#4](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/4) · 2 SP)  
**Responsable:** Santiago Correa Campaña (`@vivacius`)  
**Revisor Asignado:** Jhonatan Andrés Tapia Córdoba (`@JhonatanTC99`)  
**Fecha:** 2026-11-12

---

## 1. Propósito y Alcance
Completar el criterio de aceptación **AC1.2** de HU-01 normalizando el formato PEP 8 con Ruff en los 5 archivos pendientes (`src/config.py`, `src/inference.py`, `src/labels.py`, `src/model_loader.py`, `ui/api_client.py`), de modo que tanto `uv run ruff check .` como `uv run ruff format --check .` retornen código `0` y el *Quality Gate* de GitHub Actions pase en verde.

## 2. Escenarios de Aceptación (Gherkin)
- **AC1.1:** **Dado** `pyproject.toml` y `uv.lock`, **cuando** se ejecuta `uv sync --frozen`, **entonces** el entorno Python 3.13 se resuelve de forma determinista.
- **AC1.2:** **Dado** el código en `src/`, `api/`, `ui/` y `tests/`, **cuando** se ejecutan `uv run ruff check .` y `uv run ruff format --check .`, **entonces** ambos retornan código de salida `0` (`47 files already formatted`, `All checks passed!`).
- **AC1.3:** **Dado** el repositorio completo, **cuando** se audita la gestión de dependencias, **entonces** no existen archivos `requirements.txt` ni uso directo de `pip`.
