# Especificación Técnica (Spec Kit): SPEC-045 Pipeline GitLab CI/CD, Quality Gate y Build en Container Registry

**Identificador:** `SPEC-045`  
**Feature Branch:** `feature/m4-gitlab-ci-pipeline`  
**Unidad / Historia Asociada:** `M4-03`, `M4-04`, `M4-05`, `TOOL-03`, `TOOL-05`, `TOOL-09` (Módulo 4: Producción, CI/CD y cierre)  
**Fecha de Elaboración SDD (Prospectiva):** 2026-11-22  
**Trazabilidad Temporal:** **Especificación prospectiva elaborada ANTES de implementar `.gitlab-ci.yml` y ajustes asociados.**  
**Estado:** En progreso  
**Responsable:** John Restrepo (Grupo 2 - UAO)  
**Artefactos Relacionados:** [plan.md](./plan.md) · [tasks.md](./tasks.md)

---

## 1. Propósito y Alcance

Implementar el archivo de configuración `.gitlab-ci.yml` en la raíz del repositorio oficial, adaptando las directivas oficiales del curso y las prácticas pedagógicas transmitidas por el docente (imagen oficial Astral `uv:0.13.9-python3.13-trixie-slim`, variables deterministas, gestión de caché por job, `auto_cancel`, reportes JUnit y de cobertura, y separación de responsabilidades entre análisis estático y pruebas), integrando:
1. **Etapa `quality`:**
   - **`lint`:** Análisis estático con Ruff (`check` y `format --check`) sobre Python 3.13 instalando únicamente el grupo de desarrollo en modo `--no-install-project` para feedback ultrarrápido sin dependencias pesadas.
   - **`run_test`:** Ejecución de pruebas unitarias mediante la interfaz operativa del proyecto (`Makefile` y `uv run pytest`), con variables de entorno para emisión automática de reporte JUnit (`PYTEST_ADDOPTS="--junitxml=report.xml"`) y reporte Cobertura XML para GitLab CI UI. Inclusión de dependencias de sistema Debian 13 (`trixie-slim`: `make`, `libgl1`, `libglib2.0-0t64`, `libxcb1`, etc.) y protección condicional ante ausencia de servidor gráfico para Tkinter (`pytest.importorskip("tkinter")`).
2. **Etapa `build`:**
   - **`package_wheel`:** Construcción de paquetes distribuibles Wheel y sdist en `dist/` usando `uv build` y guardados como artefactos de CI (`HU-08`, `SPEC-036`).
   - **`build_docker`:** Construcción de la imagen Docker en CPU (`Dockerfile` multi-etapa) y publicación en el **GitLab Container Registry** (`$CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA` y `$CI_REGISTRY_IMAGE:latest`) autenticándose con las variables predefinidas de GitLab (`$CI_REGISTRY_USER`, `$CI_REGISTRY_PASSWORD`).
3. **Coordinación y arquitectura de repositorios:**
   - Documentación clara de la sincronización entre GitHub (`origin`, repositorio principal de código y gobernanza) y GitLab (`gitlab`, plataforma de ejecución CI/CD y Container Registry).

---

## 2. Escenarios de Aceptación (Gherkin)

### AC45.1 — Pipeline declarativo con variables deterministas y cache aislado
- **Dado** el archivo `.gitlab-ci.yml` en la raíz del repositorio,
- **Cuando** GitLab CI evalúa la configuración,
- **Entonces** utiliza la imagen oficial `ghcr.io/astral-sh/uv:0.13.9-python3.13-trixie-slim`, define un único bloque `variables` con `UV_LINK_MODE: copy`, `UV_CACHE_DIR`, `UV_FROZEN: "1"`, `UV_PYTHON_DOWNLOADS: never`, y aísla la caché por job mediante `prefix: $CI_JOB_NAME`.

### AC45.2 — Calidad estática bloqueante sin sobrecoste (`lint`)
- **Dado** el job `lint` en la etapa `quality`,
- **Cuando** se ejecuta en el runner de GitLab,
- **Entonces** instala exclusivamente el grupo `dev` sin empaquetar el proyecto (`uv sync --only-group dev --no-install-project`), ejecuta `ruff check .` y `ruff format --check .`, y falla de inmediato ante cualquier discrepancia de estilo o PEP 8.

### AC45.3 — Pruebas unitarias reproducibles y reportes para GitLab (`run_test`)
- **Dado** el job `run_test` en la etapa `quality`,
- **Cuando** se ejecuta en el runner de GitLab,
- **Entonces** instala las dependencias necesarias de Debian 13 (`make`, bibliotecas X11/GL con transición `libglib2.0-0t64`), omite la descarga pesada de LFS en pruebas con mocks (`GIT_LFS_SKIP_SMUDGE: "1"`), ejecuta la suite de pruebas unitarias y genera los artefactos `report.xml` (JUnit) y reporte de cobertura para la interfaz visual de GitLab.

### AC45.4 — Empaquetado Wheel y Docker Container Registry (`build`)
- **Dado** la etapa `build` en GitLab CI,
- **Cuando** se ejecuta tras superar la etapa `quality`,
- **Entonces** `package_wheel` genera distribuciones en `dist/`, y `build_docker` compila la imagen en CPU y la publica en GitLab Container Registry etiquetada con `$CI_COMMIT_SHORT_SHA` y `latest`.

### AC45.5 — Preservación de capacidades protegidas y cero secretos en Git
- **Dado** el código fuente y las capacidades de M1–M3,
- **Cuando** se incorporan las configuraciones de CI/CD,
- **Entonces** no se expone ningún secreto, token o credencial en el repositorio ni en los logs, y se preservan intactas las capacidades de inferencia, API FastAPI y frontends desacoplados.
