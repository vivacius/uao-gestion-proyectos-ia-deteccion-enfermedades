# Tasks (Spec Kit): SPEC-045 Pipeline GitLab CI/CD, Quality Gate y Build en Container Registry

**Feature Branch:** `feature/m4-gitlab-ci-pipeline` | **Spec:** [spec.md](./spec.md) | **Plan:** [plan.md](./plan.md) | **Fecha SDD (Prospectiva):** 2026-11-22

- [x] **TSK-045-01:** Confirmar estado Git en rama `feature/m4-gitlab-ci-pipeline` y registrar la especificación prospectiva `SPEC-045`.
- [x] **TSK-045-02:** Aplicar protección defensiva en `tests/unit/test_desktop_app.py` (`pytest.importorskip("tkinter")`) para compatibilidad con runners CI sin GUI.
- [x] **TSK-045-03:** Redactar y configurar `.gitlab-ci.yml` integrando las variables del docente, workflow con `auto_cancel`, etapa `quality` (`lint`, `run_test`) y etapa `build` (`package_wheel`, `build_docker` con GitLab Container Registry).
- [x] **TSK-045-04:** Validar calidad estática localmente con Ruff (`ruff check .` y `ruff format --check .`) y pruebas unitarias con `pytest`.
- [x] **TSK-045-05:** Actualizar la [Matriz de Cumplimiento Académico](../../docs/academic-compliance-matrix.md) reflejando el progreso de `M4-03`, `M4-04`, `M4-05` y `TOOL-03`.
- [x] **TSK-045-06:** Verificar integridad de capacidades protegidas, ausencia de credenciales/secretos y preparar commit bajo Conventional Commits.
