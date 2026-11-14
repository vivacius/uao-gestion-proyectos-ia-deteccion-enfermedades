# Tasks (Spec Kit): SPEC-009 Model Card Fitosanitaria

**Feature Branch:** `feature/m3-model-card` | **Issue:** [#29](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/29)  
**Responsable:** John Restrepo Aparicio (`@JohnRestrepo-coder`)

---

- [x] **TSK-MC-01:** Crear rama `feature/m3-model-card` desde `develop` (`734fbdf`) y redactar especificación SDD (`specs/009-m3-model-card/` con `spec.md`, `plan.md`, `tasks.md`).
- [x] **TSK-MC-02:** Elaborar `docs/model-card.md` siguiendo el estándar de Mitchell et al. (2019) y cubriendo exhaustivamente los criterios `AC-MC-01` a `AC-MC-04`.
- [x] **TSK-MC-03:** Enlazar `docs/model-card.md` en el árbol documental de `README.md` sin alterar contratos de código.
- [x] **TSK-MC-04:** Ejecutar Quality Gate completo (`ruff check .`, `ruff format --check .`, `pytest tests/unit`) asegurando código 0.
- [ ] **TSK-MC-05:** Realizar commit con Conventional Commits, publicar rama remota y abrir Pull Request formal hacia `develop` solicitando revisión a `@JhonatanTC99` y `@vivacius`.
