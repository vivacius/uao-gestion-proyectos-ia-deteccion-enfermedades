# Plan de Implementación (Spec Kit): SPEC-019 HU-04 Catálogo Bilingüe y Traducción Agronómica de las 38 Categorías

**Identificador:** `SPEC-019`  
**Feature Branch:** `feature/modelo-enfermedades-plantas`  
**Spec Asociada:** [spec.md](./spec.md)

---

## Pasos de Implementación y Verificación

1. Definir el dataclass inmutable `CategoryInfo` en `src/labels.py`.
2. Mapear los 14 cultivos en `PLANT_TRANSLATIONS_ES` y las 27 condiciones en `CONDITION_TRANSLATIONS_ES` incluyendo nombres científicos.
3. Implementar `parse_category_label()` con soporte de fallback limpio para etiquetas desconocidas.
