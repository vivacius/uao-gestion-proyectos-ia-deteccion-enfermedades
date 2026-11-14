# Plan de Implementación (Spec Kit): SPEC-011 Configuración Centralizada de Dominio, Rutas y Límites Operativos

**Identificador:** `SPEC-011`  
**Feature Branch:** `feature/m1-domain-config`  
**Spec Asociada:** [spec.md](./spec.md)  
**Fecha de Implementación de la Unidad:** 2026-11-10 (10/11/2026)  
**Fecha de Documentación SDD (Retrospectiva):** 2026-11-14 (14/11/2026)

---

## Pasos de Implementación y Verificación

1. Implementar `resolve_model_dir()` con soporte para variable de entorno `MODEL_DIR`, subdirectorio `modelo_plantas/` y raíz del proyecto.
2. Definir constantes inmutables de formatos permitidos (`.jpg`, `.jpeg`, `.png`), tipos MIME y tamaño máximo configurable.
3. Centralizar `DEVICE = 'cpu'`, `DEFAULT_TOP_K = 3` y el texto de `AGRONOMIC_DISCLAIMER`.
