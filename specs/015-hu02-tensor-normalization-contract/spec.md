# Especificación Técnica (Spec Kit): SPEC-015 HU-02 Contrato de Normalización ImageNet y Tensor [1, 3, 224, 224]

**Identificador:** `SPEC-015`  
**Feature Branch:** `feature/hu02-preprocesamiento-contratos`  
**Historia / Issue Asociado:** HU-02 (Issue [#5](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/5) · 3 SP · PR [#18](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/pull/18))  
**Responsable:** José Isaac Silva Calderón (`@josesilvacalderon111`)  
**Revisor Asignado:** Jhonatan Andrés Tapia Córdoba (`@JhonatanTC99`)  
**Fecha:** 2026-11-11  
**Estado:** Completado y verificado en `develop`

---

## 1. Propósito y Alcance
Implementar en `src/preprocessing.py` (`normalize_pil_to_tensor` y `preprocess_image`) la transformación matemática determinista alineada con `preprocessor_config.json`: redimensionado bicúbico del lado más corto a `256 px`, recorte central (`center_crop`) a `224×224 px`, reescalado `[0.0, 1.0]` (`1/255`), normalización por canal con media ImageNet `[0.485, 0.456, 0.406]` y desviación estándar `[0.229, 0.224, 0.225]`, garantizando un tensor PyTorch `pixel_values` de forma `(1, 3, 224, 224)` y `dtype=torch.float32` en CPU.

## 2. Escenarios de Aceptación (Gherkin)

### AC15.1 — Forma y tipo de dato del tensor (AC2.2)
- **Dado** cualquier imagen RGB válida de entrada (rectangular o cuadrada),
- **Cuando** se ejecuta `normalize_pil_to_tensor()` o `preprocess_image()`,
- **Entonces** el tensor resultante tiene forma exacta `(1, 3, 224, 224)`, tipo `torch.float32` y dispositivo `cpu`.

### AC15.2 — Fidelidad numérica de normalización ImageNet (AC2.3)
- **Dado** una imagen de prueba con valores RGB conocidos,
- **Cuando** se transforma mediante `normalize_pil_to_tensor()`,
- **Entonces** los valores del tensor coinciden con `(píxel / 255.0 - mean) / std` usando `IMAGENET_MEAN` e `IMAGENET_STD`.
