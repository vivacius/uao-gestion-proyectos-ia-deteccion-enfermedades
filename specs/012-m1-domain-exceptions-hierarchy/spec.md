# Especificación Técnica (Spec Kit): SPEC-012 Jerarquía de Excepciones de Dominio y Contratos de Error HTTP

**Identificador:** `SPEC-012`  
**Feature Branch:** `feature/m1-domain-exceptions`  
**Historia / Issue Asociado:** HU-02 / HU-05 (Issue [#5](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/5), [#8](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/8))  
**Responsable:** José Isaac Silva Calderón (`@josesilvacalderon111`)  
**Revisor Asignado:** Jhonatan Andrés Tapia Córdoba (`@JhonatanTC99`)  
**Fecha:** 2026-11-10  
**Estado:** Completado y verificado en `develop`

---

## 1. Propósito y Alcance
Diseñar e implementar en `src/exceptions.py` una jerarquía de excepciones de dominio encabezada por `PlantDiseaseAppError`, separando errores de carga del modelo (`ModelLoadError`), errores de inferencia (`InferenceError`) y errores de validación de imagen (`ImageValidationError`, `InvalidImageFormatException`, `EmptyImageError`, `ImageTooLargeError`, `UnsupportedImageFormatError`, `CorruptedImageError`) con códigos de estado HTTP semánticos (`400`, `413`, `415`, `500`, `503`).

## 2. Escenarios de Aceptación (Gherkin)

### AC12.1 — Contrato InvalidImageFormatException (HU-02 AC2.1)
- **Dado** un archivo vacío, corrupto o con formato inválido,
- **Cuando** es rechazado por la capa de preprocesamiento,
- **Entonces** se lanza una subclase de `InvalidImageFormatException` (que hereda de `ImageValidationError`) con su `status_code` correspondiente.

### AC12.2 — Mapeo semántico de códigos HTTP
- **Dado** las excepciones `EmptyImageError` (400), `CorruptedImageError` (400), `ImageTooLargeError` (413) y `UnsupportedImageFormatError` (415),
- **Cuando** son capturadas por la capa REST en `api/main.py`,
- **Entonces** retornan el código HTTP exacto y el nombre de la clase en `error_type`.
