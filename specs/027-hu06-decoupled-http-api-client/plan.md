# Plan de Implementación (Spec Kit): SPEC-027 HU-06 Cliente HTTP Desacoplado para Consumo de la API REST

**Identificador:** `SPEC-027`  
**Feature Branch:** `feature/interfaz-escritorio-tkinter`  
**Spec Asociada:** [spec.md](./spec.md)

---

## Pasos de Implementación y Verificación

1. Implementar `get_api_base_url()` respetando la variable de entorno `API_BASE_URL`.
2. Implementar `check_api_health()` contra `GET /health` y `predict_image_via_api()` enviando `multipart/form-data` a `POST /predict`.
3. Crear la excepción `ApiClientError` para desacoplar errores de transporte HTTP de la lógica visual.
