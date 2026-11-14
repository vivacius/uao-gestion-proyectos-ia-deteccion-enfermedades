# Especificación Técnica (Spec Kit): HU-07 Aislamiento de Pruebas Unitarias y Cobertura

**Feature Branch:** `feature/hu07-tests-coverage`  
**Historia Asociada:** HU-07 (Issue [#10](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/10) · 3 SP)  
**Responsable:** Santiago Correa Campaña (Testing / QA)  
**Revisor Asignado:** Jhonatan Andrés Tapia Córdoba (Code Reviewer)  
**Fecha:** 2026-11-12

---

## 1. Propósito y Alcance
Consolidar la suite de pruebas unitarias en `tests/unit/` garantizando aislamiento completo mediante *mocks* (sin lectura de `model.safetensors` ni descargas de red), cobertura $\ge 85\%$ sobre `src/` y `api/`, y verificación real de ejecución bajo `uv run pytest`.

> **Delimitación colaborativa:** Esta unidad modifica únicamente pruebas (`tests/unit/`) y artefactos Spec Kit (`specs/`), sin alterar código funcional en `src/`, `api/` ni `ui/` propiedad de otros integrantes.

## 2. Escenarios de Aceptación (Gherkin)

### AC7.1 — Aislamiento y Mocks en Suite Unitaria
- **Dado** el conjunto de pruebas en `tests/unit/`,
- **Cuando** se ejecuta `uv run pytest tests/unit`,
- **Entonces** todas las pruebas pasan utilizando *mocks* para `AutoImageProcessor`, `AutoModelForImageClassification`, `get_model_bundle` y cliente HTTP sin cargar pesos reales en disco.

### AC7.3 — Cobertura Combinada $\ge 85\%$
- **Dado** el código fuente en `src/` y `api/`,
- **Cuando** se ejecuta `uv run pytest tests/unit --cov=src --cov=api --cov-report=term-missing`,
- **Entonces** la cobertura total combinada supera el $85\%$, cubriendo los flujos críticos de `src/inference.py`, `src/model_loader.py` y el `lifespan` de `api/main.py`.

### Calidad y Gobernanza (AGENTS.md)
- **Dado** el archivo modificado `tests/unit/test_api_and_loader_mocked.py`,
- **Cuando** se ejecutan `uv run ruff check` y `uv run ruff format --check`,
- **Entonces** ambos retornan código de salida `0` y todas las pruebas nuevas siguen el patrón Arrange-Act-Assert (AAA).
