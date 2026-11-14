# Plan de Implementación (Spec Kit): SPEC-033 HU-07 Generadores Deterministas de Imágenes Sintéticas para Pruebas (conftest.py)

**Identificador:** `SPEC-033`  
**Feature Branch:** `feature/hu07-tests-coverage`  
**Spec Asociada:** [spec.md](./spec.md)

---

## Pasos de Implementación y Verificación

1. Implementar `create_test_image_bytes()` en `tests/conftest.py` dibujando una silueta foliar determinista con `ImageDraw`.
2. Exponer fixtures reutilizables: `valid_jpeg_bytes`, `valid_png_bytes`, `rgba_png_bytes`, `grayscale_jpeg_bytes`, `rectangular_jpeg_bytes`, `tiny_image_bytes`, `gif_image_bytes` y `corrupted_image_bytes`.
