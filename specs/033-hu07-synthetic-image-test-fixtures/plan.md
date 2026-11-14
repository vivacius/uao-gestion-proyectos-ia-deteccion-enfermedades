# Plan de Implementación (Spec Kit): SPEC-033 HU-07 Generadores Deterministas de Imágenes Sintéticas para Pruebas (conftest.py)

**Identificador:** `SPEC-033`  
**Feature Branch:** `feature/hu07-tests-coverage`  
**Spec Asociada:** [spec.md](./spec.md) | **Tasks:** [tasks.md](./tasks.md)  
**Fecha de Implementación de la Unidad:** 2026-11-11 (11/11/2026)  
**Fecha de Documentación SDD (Retrospectiva):** 2026-11-14 (14/11/2026)

---

## Pasos de Implementación y Verificación

1. Implementar `create_test_image_bytes()` en `tests/conftest.py` dibujando una silueta foliar determinista con `ImageDraw`.
2. Exponer fixtures reutilizables: `valid_jpeg_bytes`, `valid_png_bytes`, `rgba_png_bytes`, `grayscale_jpeg_bytes`, `rectangular_jpeg_bytes`, `tiny_image_bytes`, `gif_image_bytes` y `corrupted_image_bytes`.
