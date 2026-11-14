# Especificación Técnica (Spec Kit): SPEC-019 HU-04 Catálogo Bilingüe y Traducción Agronómica de las 38 Categorías

**Identificador:** `SPEC-019`  
**Feature Branch:** `feature/modelo-enfermedades-plantas`  
**Historia / Issue Asociado:** HU-04 (Issue [#7](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/7) · 2 SP)  
**Responsable:** John Restrepo Aparicio (`@JohnRestrepo-coder`)  
**Revisor Asignado:** Jhonatan Andrés Tapia Córdoba (`@JhonatanTC99`)  
**Fecha:** 2026-11-11  
**Estado:** Completado y verificado en `develop`

---

## 1. Propósito y Alcance
Construir en `src/labels.py` el diccionario taxonómico y las funciones de parseo (`parse_category_label`, `PLANT_TRANSLATIONS_ES`, `CONDITION_TRANSLATIONS_ES`) que transforman las 38 etiquetas crudas de PlantVillage (formato `Planta___Condición`) en información estructurada en español e inglés: nombre del cultivo (14 especies), nombre fitopatológico de la enfermedad o condición (26 patologías y 12 estados sanos) y estado general (`Sana` / `Enferma`).

## 2. Escenarios de Aceptación (Gherkin)

### AC19.1 — Cobertura exacta de las 38 clases del modelo
- **Dado** las 38 etiquetas definidas en `id2label` dentro de `config.json`,
- **Cuando** se procesan mediante `parse_category_label(raw_label)`,
- **Entonces** todas cuentan con traducción precisa al español para la planta y la patología o condición saludable.

### AC19.2 — Determinación automática de estado fitosanitario
- **Dado** una etiqueta cruda de PlantVillage,
- **Cuando** contiene el sufijo `healthy` o una patología,
- **Entonces** el objeto `CategoryInfo` establece `is_healthy = True` y `health_status = 'Sana'` (o `False` y `'Enferma'` en caso contrario).
