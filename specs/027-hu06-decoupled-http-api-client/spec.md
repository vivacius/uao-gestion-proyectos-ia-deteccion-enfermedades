# Especificación Técnica (Spec Kit): SPEC-027 HU-06 Cliente HTTP Desacoplado para Consumo de la API REST

**Identificador:** `SPEC-027`  
**Feature Branch:** `feature/interfaz-escritorio-tkinter`  
**Historia / Issue Asociado:** HU-06 (Issue [#9](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/9) · 3 SP)  
**Responsable:** John Restrepo Aparicio (`@JohnRestrepo-coder`)  
**Revisor Asignado:** Jhonatan Andrés Tapia Córdoba (`@JhonatanTC99`)  
**Fecha de Implementación de la Unidad:** 2026-11-11 (11/11/2026)  
**Fecha de Documentación SDD (Retrospectiva):** 2026-11-14 (14/11/2026)  
**Trazabilidad Temporal:** Especificación documentada retrospectivamente el 14/11/2026 (no elaborada antes de implementar; la fecha histórica 2026-11-11 corresponde a la implementación de la unidad)  
**Estado:** Completado y verificado en `develop`

---

## 1. Propósito y Alcance
Implementar en `ui/api_client.py` el cliente HTTP desacoplado (`check_api_health`, `predict_image_via_api`, `get_api_base_url` y `ApiClientError`) usando `httpx`, garantizando que la capa de presentación consuma el modelo exclusivamente vía HTTP REST sin importar PyTorch, Transformers ni cargar `model.safetensors`.

## 2. Escenarios de Aceptación (Gherkin)

### AC27.1 — Separación estricta entre UI y motor de IA
- **Dado** el módulo `ui/api_client.py`,
- **Cuando** se inspeccionan sus dependencias e importaciones,
- **Entonces** utiliza únicamente `httpx` y librerías estándar, sin importar `torch`, `transformers` ni `src.model_loader`.

### AC27.2 — Manejo resiliente de errores de red y respuestas HTTP
- **Dado** una caída de conexión (`httpx.RequestError`) o un error HTTP (`400`, `415`, `503`) devuelto por la API,
- **Cuando** se invoca `predict_image_via_api()`,
- **Entonces** se captura el fallo y se lanza `ApiClientError` con el mensaje claro en español y el `status_code` asociado.
