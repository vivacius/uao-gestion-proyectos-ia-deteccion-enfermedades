# Especificación Técnica (Spec Kit): SPEC-013 HU-02 Validación Defensiva de Metadatos, Extensiones y Tipos MIME

**Identificador:** `SPEC-013`  
**Feature Branch:** `feature/hu02-preprocesamiento-contratos`  
**Historia / Issue Asociado:** HU-02 (Issue [#5](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/5) · 3 SP)  
**Responsable:** José Isaac Silva Calderón (`@josesilvacalderon111`)  
**Revisor Asignado:** Jhonatan Andrés Tapia Córdoba (`@JhonatanTC99`)  
**Fecha:** 2026-11-11  
**Estado:** Completado y verificado en `develop`

---

## 1. Propósito y Alcance
Implementar en `src/preprocessing.py` (`validate_file_metadata` y controles iniciales de `validate_and_open_image`) la validación temprana de tamaño de archivo (no vacío y $\le 10$ MB), extensión de nombre de archivo (`.jpg`, `.jpeg`, `.png`) y encabezado `Content-Type` (`image/jpeg`, `image/jpg`, `image/png`) antes de invocar el decodificador de imagen.

## 2. Escenarios de Aceptación (Gherkin)

### AC13.1 — Rechazo de archivos vacíos y sobredimensionados
- **Dado** un payload de `0 bytes` o superior a `10 MB`,
- **Cuando** se invoca `validate_and_open_image()`,
- **Entonces** se lanza `EmptyImageError` (HTTP 400) o `ImageTooLargeError` (HTTP 413) de forma inmediata.

### AC13.2 — Filtro estricto de extensión y MIME type
- **Dado** un archivo con extensión `.gif`, `.pdf`, `.txt` o MIME `text/plain`,
- **Cuando** se ejecuta `validate_file_metadata()`,
- **Entonces** se lanza `UnsupportedImageFormatError` (HTTP 415) detallando los formatos admitidos.
