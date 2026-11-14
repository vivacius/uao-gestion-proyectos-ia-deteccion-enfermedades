# Especificación Técnica (Spec Kit): SPEC-010 HU-01 Inicialización Determinista con uv y Python 3.13

**Identificador:** `SPEC-010`  
**Feature Branch:** `feature/hu01-uv-bootstrap`  
**Historia / Issue Asociado:** HU-01 (Issue [#4](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/4) · 2 SP)  
**Responsable:** Santiago Correa Campaña (`@vivacius`)  
**Revisor Asignado:** Jhonatan Andrés Tapia Córdoba (`@JhonatanTC99`)  
**Fecha:** 2026-11-10  
**Estado:** Completado y verificado en `develop`

---

## 1. Propósito y Alcance
Establecer la configuración base del proyecto con `uv` sobre Python 3.13 (`.python-version`, `pyproject.toml` y `uv.lock`), asegurando la resolución determinista de dependencias para inferencia en CPU (`torch`, `transformers`, `safetensors`, `fastapi`, `pillow`) y herramientas de calidad (`pytest`, `pytest-cov`, `ruff`) sin emplear `pip` ni `requirements.txt`.

## 2. Escenarios de Aceptación (Gherkin)

### AC10.1 — Fijación de versión de Python
- **Dado** el archivo `.python-version` y la restricción `requires-python = ">=3.13"` en `pyproject.toml`,
- **Cuando** se inicializa el entorno con `uv sync --frozen`,
- **Entonces** se crea `.venv` utilizando exclusivamente el intérprete CPython 3.13.

### AC10.2 — Bloqueo determinista de dependencias CPU
- **Dado** el archivo `uv.lock` versionado en la raíz del repositorio,
- **Cuando** cualquier desarrollador o pipeline CI sincroniza el entorno,
- **Entonces** se instalan exactamente las mismas versiones de paquetes incluyendo `torch` CPU sin requerir CUDA.

### AC10.3 — Prohibición de requirements.txt
- **Dado** las reglas de gobernanza del proyecto,
- **Cuando** se inspecciona el árbol de archivos del repositorio,
- **Entonces** no existen archivos `requirements.txt` ni invocaciones directas a `pip install`.
