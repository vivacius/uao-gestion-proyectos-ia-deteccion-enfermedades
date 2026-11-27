# Tasks (Spec Kit): SPEC-041 Makefile Académico M1–M4 y Estándar Operativo

**Feature Branch:** `feature/docs` | **Spec:** [spec.md](./spec.md) | **Plan:** [plan.md](./plan.md) | **Fecha SDD (Prospectiva):** 2026-11-21

- [x] **TSK-041-01:** Confirmar estado Git (`feature/docs`) y disponibilidad de herramientas (`make`, `uv`, `docker`).
- [x] **TSK-041-02:** Crear `Makefile` en la raíz con los 17 targets acordados (`help` a `ci`), parametrización limpia y compatibilidad Windows/Linux.
- [ ] **TSK-041-03:** Validar targets seguros de QA y lectura disponibles sin iniciar servicios persistentes ni alterar contenedores. *(Parcial: `ruff check .` y `ruff format --check .` en código 0; `pytest tests/unit` bloqueado en `test_api_health_when_model_fails_to_load` dentro del sandbox; `make` no instalado en Windows).*
- [x] **TSK-041-04:** Actualizar `docs/academic-compliance-matrix.md` registrando el `Makefile` y resultados reales de validación.
- [x] **TSK-041-05:** Actualizar `README.md` documentando los targets del `Makefile` y sus requisitos.
- [x] **TSK-041-06:** Verificar que no existan modificaciones fuera de alcance ni regresiones en capacidades protegidas.
