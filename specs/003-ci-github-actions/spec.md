# Especificación Técnica (Spec Kit): T-04 Quality Gate en GitHub Actions

**Feature Branch:** `feature/ci-github-actions`  
**Actividad / Historia Asociada:** T-04 (Transversal CI) · Soporte a HU-01 (Issue [#4](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/4)) y HU-07 (Issue [#10](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/10))  
**Responsable:** Santiago Correa Campaña (`@vivacius`)  
**Revisor Asignado:** Jhonatan Andrés Tapia Córdoba (`@JhonatanTC99`)  
**Fecha:** 2026-11-12

---

## 1. Propósito y Alcance
Implementar un flujo de integración continua ligero (*Quality Gate*) en `.github/workflows/ci.yml` para validar automáticamente cada Pull Request hacia `develop` y cada push a `develop`, sin descargar ni cargar pesos reales de DINOv2 (`model.safetensors`) ni ejecutar despliegues productivos (reservados a M4).

## 2. Escenarios de Aceptación (Gherkin)

### AC-CI-01 — Activación en PR y Push a `develop`
- **Dado** un Pull Request dirigido a la rama `develop` (o un push a `develop`),
- **Cuando** GitHub Actions ejecuta `.github/workflows/ci.yml`,
- **Entonces** prepara Python 3.13 mediante `astral-sh/setup-uv@v5` e instala dependencias deterministas con `uv sync --frozen` sin usar `pip` ni `requirements.txt`.

### AC-CI-02 — Controles de Calidad y Pruebas Unitarias
- **Dado** el entorno instalado en el runner `ubuntu-latest`,
- **Cuando** el workflow ejecuta `uv run ruff check .`, `uv run ruff format --check .` y `uv run pytest tests/unit -v --cov=src --cov=api --cov-report=term-missing`,
- **Entonces** reporta con veracidad el estado de lint, formato y pruebas unitarias con mocks sin descargar pesos de Hugging Face.
