# Plan de Implementación (Spec Kit): SPEC-013 HU-02 Validación Defensiva de Metadatos, Extensiones y Tipos MIME

**Identificador:** `SPEC-013`  
**Feature Branch:** `feature/hu02-preprocesamiento-contratos`  
**Spec Asociada:** [spec.md](./spec.md)

---

## Pasos de Implementación y Verificación

1. Implementar `validate_file_metadata(filename, content_type)` normalizando mayúsculas y parámetros de cabecera MIME.
2. Validar longitud en bytes en `validate_and_open_image()` previo a abrir `BytesIO`.
3. Cubrir casos borde (nombres con espacios, MIME con `; charset=binary`, archivos vacíos) en `tests/unit/test_preprocessing_unit.py`.
