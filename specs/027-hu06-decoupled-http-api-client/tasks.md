# Tasks (Spec Kit): SPEC-027 HU-06 Cliente HTTP Desacoplado para Consumo de la API REST

**Feature Branch:** `feature/interfaz-escritorio-tkinter` | **Spec:** [spec.md](./spec.md)

- [x] **TSK-027-01:** Crear `ui/api_client.py` con funciones `check_api_health` y `predict_image_via_api`.
- [x] **TSK-027-02:** Implementar manejo de timeouts, errores de conexión y parseo de `detail` en `ApiClientError`.
- [x] **TSK-027-03:** Cubrir todos los caminos de éxito y error con mocks de `httpx` en `tests/unit/test_api_and_loader_mocked.py`.
