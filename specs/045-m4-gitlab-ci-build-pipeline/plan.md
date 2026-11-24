# Plan de Implementación (Spec Kit): SPEC-045 Pipeline GitLab CI/CD, Quality Gate y Build en Container Registry

**Identificador:** `SPEC-045`  
**Feature Branch:** `feature/m4-gitlab-ci-pipeline`  
**Spec Técnica:** [spec.md](./spec.md)  
**Tasks:** [tasks.md](./tasks.md)  
**Fecha SDD (Prospectiva):** 2026-11-22  

---

## 1. Estrategia y Enfoque

El plan aprovecha la experiencia y validación previa del job en GitLab personal (`juanalvear01/copiamodulo2`, pipeline exitoso #3098012937), incorporando las lecciones y directivas estructurales aportadas por el docente:
1. **Unificación y limpieza de variables:**
   - Un solo bloque `variables` en la raíz.
   - Fijación estricta de versiones: Astral `uv:0.13.9` con Python `3.13` sobre `trixie-slim`.
   - Modos defensivos de `uv`: `UV_LINK_MODE: copy`, `UV_FROZEN: "1"`, `UV_PYTHON_DOWNLOADS: never`.
   - `GIT_DEPTH: "1"` para clonación ultrarrápida.
2. **Optimización de Calidad:**
   - Job `lint` independiente y liviano sin dependencias de machine learning.
   - Job `run_test` ejecutando el entorno completo, con `PYTEST_ADDOPTS` inyectando `--junitxml=report.xml` y `--cov-report=xml:coverage.xml`.
   - Incorporación del guard `pytest.importorskip("tkinter")` en `tests/unit/test_desktop_app.py` para prevenir fallos espurios en entornos headless/runner slim.
3. **Fase de Construcción (Build):**
   - Job `package_wheel`: Construye sdist y wheel con `uv build` y archiva `dist/`.
   - Job `build_docker`: Usa `docker:27-cli` con servicio `docker:27-dind` (Docker-in-Docker), descarga los pesos SafeTensors mediante Git LFS (o validación local), construye la imagen oficial en CPU y hace push autenticado al Container Registry de GitLab con variables `$CI_REGISTRY`, `$CI_REGISTRY_USER`, `$CI_REGISTRY_PASSWORD`.
4. **Verificación y Calidad Local:**
   - Verificar `ruff check .` y `ruff format --check .`.
   - Validar suite de pruebas unitarias localmente con `uv run pytest tests/unit`.
   - Asegurar que no se modifiquen recursos protegidos ni se incluyan credenciales o tokens.
