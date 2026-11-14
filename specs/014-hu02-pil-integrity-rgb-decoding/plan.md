# Plan de Implementación (Spec Kit): SPEC-014 HU-02 Decodificación Segura con Pillow, Integridad Binaria y Conversión RGB

**Identificador:** `SPEC-014`  
**Feature Branch:** `feature/hu02-preprocesamiento-contratos`  
**Spec Asociada:** [spec.md](./spec.md)  
**Fecha de Implementación de la Unidad:** 2026-11-11 (11/11/2026)  
**Fecha de Documentación SDD (Retrospectiva):** 2026-11-14 (14/11/2026)

---

## Pasos de Implementación y Verificación

1. Implementar sondeo de integridad con `Image.open(BytesIO(image_bytes))` y `probe_img.verify()`.
2. Verificar `detected_format in ALLOWED_PIL_FORMATS` para bloquear GIF/BMP/WEBP renombrados como `.jpg`.
3. Reabrir y ejecutar `image.load()`, comprobar dimensiones $\ge 32 \times 32$ px y aplicar `image.convert('RGB')`.
