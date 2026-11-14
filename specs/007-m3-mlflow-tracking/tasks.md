# Tasks (Spec Kit): SPEC-007 Integración de MLflow Tracking y Model Registry

**Identificador:** `SPEC-007`  
**Feature Branch:** `feature/m3-mlflow-tracking`  
**Unidad de Trabajo:** `M3-IMP-MLF-01`  
**Issue Asociado:** Issue [#28](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/28)

---

## Tareas de Fase A: Aislamiento y Contratos
- [x] **TSK-MLF-A1:** Consultar HEAD actualizado de `origin/develop` (`c0fa59c`) y árbol limpio.
- [x] **TSK-MLF-A2:** Crear y conmutar a la rama `feature/m3-mlflow-tracking`.
- [x] **TSK-MLF-A3:** Revisar AGENTS.md, Constitución del proyecto, propuesta M2 y directrices del Anuncio 007.
- [x] **TSK-MLF-A4:** Resolver colisión de identificadores asignando `SPEC-007` y vinculando al Issue #28.
- [x] **TSK-MLF-A5:** Elaborar especificación SDD completa (`spec.md`, `plan.md`, `tasks.md`) en `specs/007-m3-mlflow-tracking/`.
- [x] **TSK-MLF-A6:** Auditar disponibilidad de datos de evaluación locales, pesos SafeTensors y etiquetas fitosanitarias (confirmar modelo local en raíz y ausencia de ground-truth etiquetado).

---

## Tareas de Fase B: Implementación
- [x] **TSK-MLF-B1:** Agregar dependencia `mlflow` mediante `uv add mlflow` compatible con Python 3.13, actualizando `pyproject.toml` y `uv.lock`.
- [x] **TSK-MLF-B2:** Actualizar `.gitignore` para blindar directorios de tracking y artefactos (`mlruns/`, `mlartifacts/`, `mlflow_data/`, `*.db`).
- [x] **TSK-MLF-B3:** Diseñar e implementar script reproducible `scripts/run_mlflow_benchmark.py` con logging de parámetros, métricas reales CPU, artefactos (`.json`, `.csv`) y tags trazables.
- [x] **TSK-MLF-B4:** Configurar los 3 runs comparables y genuinamente distintos (Baseline $\tau=0.60$, Strict $\tau=0.80$, Exploratory $\tau=0.40$).
- [x] **TSK-MLF-B5:** Integrar empaquetado y registro en *Model Registry* bajo el nombre `dinov2-plant-disease-classifier` (Versión 1) vinculado a la inferencia de FastAPI.
- [x] **TSK-MLF-B6:** Crear suite de pruebas unitarias `tests/unit/test_mlflow_benchmark.py` con patrón AAA para asegurar aislamiento y cero regresiones.

---

## Tareas de Fase C: Validación
- [x] **TSK-MLF-C1:** Ejecutar `scripts/run_mlflow_benchmark.py` localmente y verificar la persistencia de los 3 runs.
- [x] **TSK-MLF-C2:** Levantar servidor local de MLflow en `http://127.0.0.1:5050` y validar conectividad HTTP/API.
- [x] **TSK-MLF-C3:** Confirmar registro de métricas reales (latencia mean/p50/p95, throughput), tags, parámetros, artefactos y el modelo en Model Registry.
- [x] **TSK-MLF-C4:** Ejecutar suite completa de pruebas unitarias (`uv run pytest tests/unit/`) y verificar 170 passed, 2 skipped, 0 failed, 99% cobertura en src/ y api/.
- [x] **TSK-MLF-C5:** Ejecutar linters y formato con Ruff (`uv run ruff check .` y `uv run ruff format --check .`) asegurando código 0.

---

## Tareas de Fase D: Git, Dependencias y Entrega
- [x] **TSK-MLF-D1:** Documentar control de diferencias con PR #26 en `pyproject.toml` y `uv.lock`.
- [x] **TSK-MLF-D2:** Verificar que ningún artefacto pesado, log ni base SQLite esté rastreado por Git (`git status`).
- [ ] **TSK-MLF-D3:** Crear commit estructurado bajo Conventional Commits en `feature/m3-mlflow-tracking`.
- [ ] **TSK-MLF-D4:** Redactar informe técnico completo M3-IMP-MLF-01 con instrucciones de reproducción en Windows y Linux.
