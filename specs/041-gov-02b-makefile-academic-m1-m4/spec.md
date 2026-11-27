# Especificación Técnica (Spec Kit): SPEC-041 Makefile Académico M1–M4 y Estándar Operativo

**Identificador:** `SPEC-041`  
**Feature Branch:** `feature/docs`  
**Unidad / Historia Asociada:** `GOV-02B` (Matriz Académica `M1`–`M4` / Recomendación docente)  
**Fecha de Elaboración SDD (Prospectiva):** 2026-11-21  
**Trazabilidad Temporal:** **Especificación prospectiva elaborada ANTES de implementar el `Makefile`** (no retrospectiva).  
**Estado:** En progreso (`GOV-02B`)  
**Artefactos Relacionados:** [plan.md](./plan.md) · [tasks.md](./tasks.md)

---

## 1. Propósito y Alcance
Incorporar un `Makefile` en la raíz del repositorio que consolide de forma segura, reproducible y multiplataforma (Linux / Windows con GNU Make) los comandos cotidianos del proyecto: sincronización (`uv`), calidad estática (`ruff`), pruebas (`pytest` unitarias, integración y cobertura), empaquetado (`uv build`), ejecución local (`uvicorn`, `mlflow`), contenedores (`docker build` / `docker compose`) y verificación de salud (`health`), sin modificar las capacidades técnicas protegidas definidas en `docs/academic-compliance-matrix.md`.

---

## 2. Escenarios de Aceptación (Gherkin)

### AC41.1 — Targets completos y no destructivos
- **Dado** el archivo `Makefile` en la raíz del repositorio,
- **Cuando** se inspeccionan sus targets y recetas,
- **Entonces** incluye `help`, `sync`, `lint`, `format-check`, `test-unit`, `test-integration`, `test`, `coverage`, `build`, `api`, `mlflow`, `docker-build`, `docker-up`, `docker-down`, `docker-ps`, `health` y `ci`, sin invocar `pip`, `requirements.txt` ni comandos destructivos sobre archivos o datos locales.

### AC41.2 — Fallo estricto en Quality Gates (`ci`, `lint`, `format-check`, `test*`)
- **Dado** los targets de calidad (`lint`, `format-check`, `test-unit`, `test-integration`, `test`, `coverage`, `ci`),
- **Cuando** alguno de los comandos subyacentes (`uv run ruff` o `uv run pytest`) retorna código distinto de `0`,
- **Entonces** el target falla propagando el código de salida de error sin enmascarar fallos.

### AC41.3 — Compatibilidad Windows 11 / Linux y declaración de requisitos
- **Dado** un entorno Windows 11 o Linux,
- **Cuando** se documenta y utiliza el `Makefile`,
- **Entonces** las recetas evitan sintaxis exclusiva de bash no portable cuando no es necesaria, utilizan `uv run` / `docker` / `python` directamente, y `help`, `README.md` y `docs/academic-compliance-matrix.md` declaran explícitamente los requisitos (GNU Make, Docker daemon activo, `model.safetensors` local).

### AC41.4 — Preservación de capacidades protegidas
- **Dado** los artefactos protegidos en `docs/academic-compliance-matrix.md` (§ 2),
- **Cuando** se implementa `GOV-02B`,
- **Entonces** permanecen intactos `src/`, `api/`, `ui/`, `tests/`, `Dockerfile`, `docker-compose.yml`, `scripts/`, `.github/workflows/ci.yml`, `.specify/memory/constitution.md`, `AGENTS.md` y `specs/001..040/`.
