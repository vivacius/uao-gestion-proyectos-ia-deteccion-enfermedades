# Especificación Técnica (Spec Kit): SPEC-014 HU-02 Decodificación Segura con Pillow, Integridad Binaria y Conversión RGB

**Identificador:** `SPEC-014`  
**Feature Branch:** `feature/hu02-preprocesamiento-contratos`  
**Historia / Issue Asociado:** HU-02 (Issue [#5](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/5) · 3 SP)  
**Responsable:** José Isaac Silva Calderón (`@josesilvacalderon111`)  
**Revisor Asignado:** Jhonatan Andrés Tapia Córdoba (`@JhonatanTC99`)  
**Fecha:** 2026-11-11  
**Estado:** Completado y verificado en `develop`

---

## 1. Propósito y Alcance
Garantizar en `validate_and_open_image` (`src/preprocessing.py`) que los bytes recibidos correspondan a una imagen real e íntegra mediante doble verificación con Pillow (`probe_img.verify()` y `image.load()`), comprobación del formato interno decodificado (`JPEG` o `PNG`), validación de dimensiones mínimas ($32 \times 32$ px) y conversión obligatoria al espacio de color `RGB` de 3 canales.

## 2. Escenarios de Aceptación (Gherkin)

### AC14.1 — Detección de archivos corruptos o falsificados
- **Dado** un archivo de texto renombrado como `.jpg` o un flujo JPEG truncado,
- **Cuando** se procesa en `validate_and_open_image()`,
- **Entonces** Pillow detecta la anomalía y se lanza `CorruptedImageError` (subclase de `InvalidImageFormatException`, HTTP 400).

### AC14.2 — Validación de dimensiones mínimas y conversión a RGB
- **Dado** una imagen válida en modo `RGBA` (4 canales) o escala de grises `L` (1 canal) con dimensiones $\ge 32 \times 32$ px,
- **Cuando** finaliza `validate_and_open_image()`,
- **Entonces** retorna un objeto `PIL.Image.Image` con `mode == 'RGB'` listo para la transformación tensorial.
