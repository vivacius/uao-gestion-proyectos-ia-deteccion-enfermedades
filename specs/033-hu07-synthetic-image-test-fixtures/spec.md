# Especificación Técnica (Spec Kit): SPEC-033 HU-07 Generadores Deterministas de Imágenes Sintéticas para Pruebas (conftest.py)

**Identificador:** `SPEC-033`  
**Feature Branch:** `feature/hu07-tests-coverage`  
**Historia / Issue Asociado:** HU-07 (Issue [#10](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/10) · 3 SP)  
**Responsable:** Santiago Correa Campaña (`@vivacius`)  
**Revisor Asignado:** Jhonatan Andrés Tapia Córdoba (`@JhonatanTC99`)  
**Fecha:** 2026-11-11  
**Estado:** Completado y verificado en `develop`

---

## 1. Propósito y Alcance
Implementar en `tests/conftest.py` un conjunto completo de generadores y *fixtures* de `pytest` que construyen en memoria (`io.BytesIO`) imágenes sintéticas reproducibles en múltiples formatos y estados (JPEG RGB, PNG RGB, PNG RGBA con canal alfa, escala de grises `L`, imagen rectangular no cuadrada, imagen miniatura $< 32$ px, GIF no admitido y flujo de bytes JPEG truncado/corrupto) sin depender de archivos externos ni conexión a internet.

## 2. Escenarios de Aceptación (Gherkin)

### AC33.1 — Generación en memoria 100% autocontenida
- **Dado** la ejecución de `uv run pytest` en cualquier entorno local o runner de CI,
- **Cuando** se inyectan las fixtures de `tests/conftest.py`,
- **Entonces** todas las imágenes de prueba se generan al vuelo en RAM con Pillow sin leer datasets externos.

### AC33.2 — Cobertura de casos válidos, bordes y corruptos
- **Dado** las funciones `create_test_image_bytes` y fixtures asociadas en `tests/conftest.py`,
- **Cuando** son utilizadas por las suites unitaria e integrada,
- **Entonces** proveen casos para RGB, RGBA, escala de grises, dimensiones inválidas, formatos prohibidos (GIF) y bytes truncados.
