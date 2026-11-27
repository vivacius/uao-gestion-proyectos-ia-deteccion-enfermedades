# Constitución del Proyecto (`CONSTITUTION.md`)

**Proyecto:** Sistema de Clasificación Asistida de Enfermedades en Plantas (`DINOv2-small` en CPU)  
**Grupo:** 2 — Maestría en Inteligencia Artificial y Ciencia de Datos (UAO)  
**Versión vigente:** `2.0.0` (ratificada `2026-11-12`, Enmienda M4 `ENM-01`–`ENM-07` aprobada por consenso unánime en `PR #54` el `2026-11-26`)  
**Documento normativo completo (Spec Kit):** [`.specify/memory/constitution.md`](.specify/memory/constitution.md)  
**Matriz SSOT M1–M4:** [`docs/academic-compliance-matrix.md`](docs/academic-compliance-matrix.md)

---

## Principios Fundamentales

1. **Arquitectura modular (`src/` layout):** Separación estricta entre dominio (`src/`), API REST FastAPI (`api/`), interfaces desacopladas (`ui/desktop_app.py`, `ui/web/static/`) y pruebas (`tests/`). Prohibido Streamlit en M3/M4 y notebooks (`.ipynb`).
2. **Entorno determinista (`uv` + Python 3.13):** Prohibido `pip` y `requirements.txt`. Todo cambio de dependencias actualiza `pyproject.toml` y `uv.lock`.
3. **Pruebas AAA y cobertura ($\ge 85\%$):** Mínimo académico de 120 pruebas AAA (actualmente **365 unitarias + 6 integración**, `98 %` cobertura).
4. **Gitflow, Kanban y revisión por pares:** Ramas protegidas `main` y `develop` (PR obligatorio, mínimo 1 aprobación, CI verde, sin `force push` ni borrado). Tablero Kanban de 4 columnas con WIP máximo `4/2`.
5. **Calidad estática, seguridad y Git LFS:** `uv run ruff check .` y `ruff format --check .` en `0`; pesos `model.safetensors` gestionados exclusivamente por Git LFS; cero secretos en código, logs o historial.

## Puertas de Calidad (M3–M4)

- **Gates 1–5 (M3):** SDD prospectivo, tipado y docstrings, Ruff limpio, Pytest $\ge 85\%$, revisión cruzada.
- **Gates 6–8 (M4):** Pipeline GitLab (`quality → test → build → deploy`), imagen en Container Registry trazable por SHA, secretos protegidos/enmascarados, VPS con firewall, proxy inverso HTTPS/TLS válido y `GET /health` `200 OK`.

> Toda reforma a esta Constitución requiere consenso unánime de los 4 integrantes del Grupo 2 (**Santiago Correa**, **José Silva**, **Jhonatan Tapia** y **John Restrepo**).
