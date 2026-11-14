# Plan de Implementación (Spec Kit): SPEC-015 HU-02 Contrato de Normalización ImageNet y Tensor [1, 3, 224, 224]

**Identificador:** `SPEC-015`  
**Feature Branch:** `feature/hu02-preprocesamiento-contratos`  
**Spec Asociada:** [spec.md](./spec.md)

---

## Pasos de Implementación y Verificación

1. Definir constantes contractuales `RESIZE_SHORTEST_EDGE = 256`, `CROP_SIZE = 224`, `EXPECTED_TENSOR_SHAPE = (1, 3, 224, 224)`, `IMAGENET_MEAN` e `IMAGENET_STD`.
2. Implementar `normalize_pil_to_tensor()` con interpolación bicúbica, recorte central y normalización tensorial en PyTorch.
3. Implementar `preprocess_image()` integrando `BitImageProcessor` (o fallback determinista) con verificación explícita de `EXPECTED_TENSOR_SHAPE`.
