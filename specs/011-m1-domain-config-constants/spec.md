# Especificación Técnica (Spec Kit): SPEC-011 Configuración Centralizada de Dominio, Rutas y Límites Operativos

**Identificador:** `SPEC-011`  
**Feature Branch:** `feature/m1-domain-config`  
**Historia / Issue Asociado:** HU-01 / HU-02 (Issue [#4](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/4), [#5](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/5))  
**Responsable:** Santiago Correa Campaña (`@vivacius`)  
**Revisor Asignado:** Jhonatan Andrés Tapia Córdoba (`@JhonatanTC99`)  
**Fecha:** 2026-11-10  
**Estado:** Completado y verificado en `develop`

---

## 1. Propósito y Alcance
Centralizar en `src/config.py` las constantes operativas del sistema: resolución de rutas del modelo (`BASE_DIR`, `MODEL_DIR`, `REQUIRED_MODEL_FILES`), dispositivo de cómputo (`DEVICE = 'cpu'`), restricciones de archivos de entrada (`MAX_IMAGE_SIZE_MB = 10`, `MIN_IMAGE_DIMENSION = 32`, `ALLOWED_EXTENSIONS`, `ALLOWED_MIME_TYPES`, `ALLOWED_PIL_FORMATS`), `DEFAULT_TOP_K = 3` y el descargo agronómico oficial (`AGRONOMIC_DISCLAIMER`).

## 2. Escenarios de Aceptación (Gherkin)

### AC11.1 — Resolución flexible de directorio del modelo
- **Dado** la función `resolve_model_dir()` en `src/config.py`,
- **Cuando** se define la variable de entorno `MODEL_DIR` o se colocan los pesos en la raíz o en `modelo_plantas/`,
- **Entonces** el sistema localiza automáticamente la carpeta que contiene `config.json`, `preprocessor_config.json` y `model.safetensors`.

### AC11.2 — Constantes de validación e inferencia desacopladas
- **Dado** los módulos `src/preprocessing.py`, `src/postprocessing.py` y `api/main.py`,
- **Cuando** importan parámetros operativos desde `src/config.py`,
- **Entonces** no existen valores mágicos (magic numbers) dispersos en la lógica de negocio.
