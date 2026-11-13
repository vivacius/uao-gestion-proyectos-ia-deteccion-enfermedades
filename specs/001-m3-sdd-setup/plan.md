# Implementation Plan: M3-G2 — Gobernanza, Spec Kit, Skills y Herramientas

**Branch**: `feature/m3-sdd-setup` | **Fecha**: 2026-11-12 | **Spec**: [spec.md](./spec.md)

---

## 1. Arquitectura Técnica y Stack Tecnológico

```
┌────────────────────────────────────────────────────────────────────────┐
│                        ESTRUCTURA DEL PROYECTO                         │
│                                                                        │
│   src/                                                                 │
│   ├── preprocessing.py    # Ingestión, redimensión 224x224, norm.      │
│   ├── model_loader.py     # SafeTensors loader determinista en CPU     │
│   ├── inference.py        # torch.no_grad(), predicción de logits      │
│   ├── postprocessing.py   # Softmax, filtro tau=0.60, descargo         │
│   └── labels.py           # Diccionario 38 clases en español           │
│                                                                        │
│   api/                                                                 │
│   ├── main.py             # FastAPI app, endpoints /health, /predict   │
│   └── schemas.py          # Contratos Pydantic de entrada y salida     │
│                                                                        │
│   ui/                                                                  │
│   ├── desktop_app.py      # Aplicación de escritorio Tkinter            │
│   ├── web/                # Frontend web HTML/CSS/JS (HU-06)           │
│   └── api_client.py       # Cliente HTTP desacoplado hacia la API      │
│                                                                        │
│   tests/                                                               │
│   ├── unit/               # Mocks, AAA, tiempo de ejecución < 10 s     │
│   └── integration/        # TestClient E2E sobre pipeline completo     │
│                                                                        │
│   .specify/               # Plantillas, scripts y memoria de Spec Kit  │
│   .gemini/commands/       # Slash commands de Spec Kit para Gemini CLI │
│   docs/                   # Arquitectura, manuales y guías de inicio   │
└────────────────────────────────────────────────────────────────────────┘
```

- **Lenguaje y Entorno:** Python 3.13 administrado exclusivamente con `uv`.
- **Framework de Inferencia:** PyTorch 2.6.0 (CPU) + SafeTensors.
- **Servicio Web:** FastAPI 0.115+ / Uvicorn / Pydantic v2.
- **Interfaz de Usuario:** Tkinter (incluido en la biblioteca estándar de Python) y frontend web HTML5/CSS3/JavaScript Vanilla.
- **Calidad y Testing:** Pytest 8.3+, Pytest-Cov, Ruff 0.9+.
- **Gobernanza y SDD:** GitHub Spec Kit 1.2.2 con integración Gemini.

---

## 2. Alineación con los Principios de la Constitución

| Principio Constitucional | Requisito Operativo | Mecanismo de Verificación en Plan |
| :--- | :--- | :--- |
| **I. Arquitectura Modular** | Alta cohesión en `src/`, `api/`, `ui/`. Sin acoplamiento circular. | Verificación de contratos Pydantic y separación estricta de capas. |
| **II. Entorno uv Determinista** | Python 3.13 con `uv.lock`. Sin `pip` ni `requirements.txt`. | Comprobación en `pyproject.toml`, bloqueo en pre-commit y CI. |
| **III. Test-First (AAA)** | Cobertura combinada $\ge 85\%$. Unitarias en $< 10$\,s. | Suite `pytest` con reporte de cobertura e informe de tiempos. |
| **IV. Gitflow y Revisión PR** | Ramas `feature/*` ➔ PR revisado ➔ `develop`. Límite WIP = 1. | Uso obligatorio de `.github/PULL_REQUEST_TEMPLATE.md` y revisión por pares. |
| **V. Calidad Estática y Seguridad** | `ruff check` y `ruff format` en 0. Cero pesos o secretos comiteados. | Linters automáticos y exclusión estricta en `.gitignore`. |

---

## 3. Fases de Implementación de la Unidad M3-G2

### Fase 1: Gobernanza Git y Configuración de Ramas
- Confirmación de estado de PR #14 (Fusionado en `develop` con aprobación formal de `vivacius`).
- Actualización de `develop` local mediante avance rápido (`fast-forward`).
- Creación de la rama `feature/m3-sdd-setup` sin modificar `main`.

### Fase 2: Infraestructura Spec Kit e Integración Gemini
- Inicialización determinista de Spec Kit 1.2.2 con opción `--integration gemini`.
- Exclusión en `.gitignore` de datos de sesión y archivos temporales personales de agentes.
- Creación de `.specify/memory/constitution.md` y `AGENTS.md` alineados a la propuesta M2.
- Incorporación del catálogo completo de 8 HU, 25 AC y 21 SP en las especificaciones.

### Fase 3: Auditoría y Activación de la Skill Archify
- Clonación/descarga de la skill oficial desde `tt-a1i/archify`.
- Inspección de licencia, dependencias y versión/commit.
- Auditoría estática exhaustiva con SkillSpector (búsqueda de riesgos de red, ejecución arbitraria o escalamiento).
- Habilitación en el proyecto y generación del diagrama arquitectónico actual (`docs/architecture/`).

### Fase 4: Gobernanza de Memoria (Engram MCP) y Control Preventivo (GGA)
- Verificación de la conexión y configuración de Engram MCP sin exponer bases de datos privadas ni rutas absolutas.
- Evaluación de compatibilidad de GGA en Windows/uv.
- Elaboración de la guía de inicio y reproducción (`docs/getting-started.md`).

---

## 4. Puertas de Calidad (Quality Gates) para Cierre de Fase
1. **Gate A (Gitflow):** Rama de trabajo creada desde el último commit de `develop`; árbol de trabajo limpio.
2. **Gate B (Spec Kit):** Comandos `/speckit.*` operativos; especificaciones y tareas trazadas 1:1 con las 8 HU.
3. **Gate C (Seguridad Skills):** Reporte de SkillSpector sin hallazgos CRITICAL ni HIGH.
4. **Gate D (Arquitectura):** Diagrama interactivo y estático accesible en `docs/architecture/` representando la estructura real.
5. **Gate E (Reproducibilidad):** Guía verificada paso a paso para cualquier integrante del equipo.
