# Especificación Técnica (Spec Kit): SPEC-034 HU-07 Suite de Pruebas Unitarias AAA para Preprocesamiento, Taxonomía y Postprocesamiento

**Identificador:** `SPEC-034`  
**Feature Branch:** `feature/hu07-tests-coverage`  
**Historia / Issue Asociado:** HU-07 (Issue [#10](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/10) · 3 SP)  
**Responsable:** Santiago Correa Campaña (`@vivacius`)  
**Revisor Asignado:** Jhonatan Andrés Tapia Córdoba (`@JhonatanTC99`)  
**Fecha:** 2026-11-11  
**Estado:** Completado y verificado en `develop`

---

## 1. Propósito y Alcance
Desarrollar las suites de pruebas unitarias rápidas bajo el patrón **Arrange-Act-Assert (AAA)** en `tests/unit/test_preprocessing_unit.py` y `tests/unit/test_labels_and_postprocessing.py`, verificando todos los contratos de validación de imagen, normalización tensorial `(1, 3, 224, 224)`, traducción de las 38 etiquetas al español, cálculo de Softmax y ranking Top-3 sin tocar `model.safetensors`.

## 2. Escenarios de Aceptación (Gherkin)

### AC34.1 — Verificación exhaustiva del preprocesamiento y sus excepciones
- **Dado** la suite `tests/unit/test_preprocessing_unit.py`,
- **Cuando** se ejecuta con `uv run pytest tests/unit/test_preprocessing_unit.py`,
- **Entonces** valida todos los rechazos (`EmptyImageError`, `ImageTooLargeError`, `UnsupportedImageFormatError`, `CorruptedImageError`, `InvalidImageFormatException`) y la forma `(1, 3, 224, 224)` en `float32`.

### AC34.2 — Verificación de las 38 clases y postprocesamiento Top-3
- **Dado** la suite `tests/unit/test_labels_and_postprocessing.py`,
- **Cuando** se ejecuta con `uv run pytest tests/unit/test_labels_and_postprocessing.py`,
- **Entonces** comprueba la traducción de las 38 categorías, el orden descendente de probabilidades, la suma unitaria de Softmax y la presencia del descargo agronómico.
