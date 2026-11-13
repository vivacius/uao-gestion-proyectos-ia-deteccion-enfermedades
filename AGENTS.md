# Reglas Operativas para Agentes de IA (AGENTS.md)
<!-- Grupo 2 — Maestría en IA y Ciencia de Datos | UAO -->

Este documento establece las políticas de gobernanza, jerarquía de toma de decisiones, permisos y directrices técnicas para cualquier agente de inteligencia artificial (Gemini, Claude, GPT, Antigravity u otros) que interactúe con el repositorio.

---

## 1. Jerarquía y Gobernanza

Este repositorio capitaliza los **aprendizajes acumulativos del Módulo 1 (M1)**: modularidad en `src/` layout, alta cohesión, bajo acoplamiento, desarrollo guiado por pruebas (pytest AAA), entorno determinista con `uv`, linteo riguroso con Ruff y Gitflow estricto.

```
┌─────────────────────────────────────────────────────────────┐
│                 HUMANOS (EQUIPO GRUPO 2)                    │
│   Santiago Correa · José Silva · Jhonatan Tapia · John R.   │
│   - Máxima autoridad técnica, de diseño y arquitectónica.   │
│   - Únicos facultados para autorizar y fusionar Pull Regs.  │
└──────────────────────────────┬──────────────────────────────┘
                               │ Supervisión y directrices
┌──────────────────────────────┴──────────────────────────────┐
│                    AGENTES DE ASISTENCIA                    │
│                                                             │
│   ● Gemini / Antigravity CLI:                               │
│     - Orquestación SDD con Spec Kit (Specify, Plan, Tasks). │
│     - Ejecución de pruebas (pytest), análisis estático.     │
│     - Generación y actualización de diagramas (Archify).    │
│     - Creación de commits y PRs delegados por el equipo.    │
│                                                             │
│   ● GPT / Otros Modelos de Lenguaje:                        │
│     - Asistencia en redacción conceptual y documentación.   │
│     - Co-diseño de pruebas y consultas técnicas.            │
└─────────────────────────────────────────────────────────────┘
```

- **Primacía Humana:** Ningún agente de IA puede tomar decisiones unilaterales que contradigan la Constitución del proyecto (`.specify/memory/constitution.md`) ni los requisitos aprobados en la propuesta formal (`Plantilla.pdf`).
- **Aprobación de Cambios:** Toda modificación sustancial debe ser revisada y aprobada por un humano mediante un Pull Request formal.

---

## 2. Matriz de Responsabilidades por Historia de Usuario

| Historia de Usuario | Responsable Humano | Rol | Agente Principal | Alcance Técnico |
| :--- | :--- | :--- | :--- | :--- |
| **HU-01** (2 SP) | Santiago Correa | DevOps | Gemini / Antigravity | Tooling base, entorno `uv`, linters `ruff`. |
| **HU-02** (3 SP) | José Silva | ML | Gemini / Antigravity | Preprocesamiento, contratos de tensores $[1, 3, 224, 224]$. |
| **HU-03** (3 SP) | Jhonatan Tapia | ML | Gemini / Antigravity | Carga segura SafeTensors e inferencia CPU $< 300$\,ms. |
| **HU-04** (2 SP) | John Restrepo | Backend | Gemini / Antigravity | Postproceso, mapeo a español, filtro $\tau=0.60$ y descargo agronómico. |
| **HU-05** (3 SP) | Jhonatan Tapia | Backend | Gemini / Antigravity | API REST asíncrona FastAPI, OpenAPI y contratos Pydantic. |
| **HU-06** (3 SP) | John Restrepo | Frontend | Gemini / Antigravity | Interfaz Streamlit para técnicos de campo (Top-3 y alertas). |
| **HU-07** (3 SP) | Santiago Correa | Testing | Gemini / Antigravity | Suite `pytest` AAA (unitarias + integración), cobertura $\ge 85\%$. |
| **HU-08** (2 SP) | José Silva | DevOps | Gemini / Antigravity | Empaquetado Wheel (`uv build`) y contenerización Docker CPU (M4). |

- **Revisor de Código General (Code Reviewer):** Jhonatan Tapia.
- **Revisión Cruzada Obligatoria:** Todo PR requiere revisión aprobada de un compañero distinto del autor del cambio.
- **Separación de Alcance M3 vs M4:** HU-01 a HU-07 corresponden al Módulo 3 (inferencia CPU DINOv2, FastAPI, Streamlit, Pytest). HU-08 queda expresamente diferida para el Módulo 4 (Docker multi-etapa y empaquetado Wheel).

---

## 3. Permisos y Restricciones de los Agentes

### Acciones Permitidas para los Agentes:
1. Leer y analizar cualquier archivo dentro del repositorio.
2. Ejecutar comandos de verificación en entorno aislado (`uv run pytest`, `uv run ruff check .`, `uv run ruff format --check .`).
3. Generar y refinar artefactos de especificación en `specs/` y `.specify/` usando las fases de Spec Kit.
4. Generar diagramas de arquitectura con Archify en `docs/architecture/` tras validación estática local.
5. Gestionar memoria técnica en Engram MCP sin exponer bases de datos locales ni claves privadas.
6. Crear commits y abrir Pull Requests hacia `develop` bajo Conventional Commits y plantilla institucional `.github/PULL_REQUEST_TEMPLATE.md` cuando sea expresamente delegado y autorizado por el equipo humano en una unidad de trabajo.

### Restricciones Estrictas (Acciones Prohibidas):
1. **NO modificar Git history sin autorización:** No ejecutar `git merge`, `git rebase` ni alterar ramas protegidas (`main`, `develop`).
2. **NO auto-aprobar PRs ni ejecutar merge:** La fusión a `develop` o `main` es potestad exclusiva del desarrollador humano tras la revisión aprobada de un par. Queda prohibido cualquier merge automático por parte de agentes.
3. **NO conmutar ramas automáticamente:** Los scripts de Spec Kit no deben cambiar ni crear ramas Git sin autorización explícita.
4. **NO instalar paquetes con pip directo ni generar requirements.txt:** Usar exclusivamente `uv add` / `uv sync` en Python 3.13 sin alterar el Python global del sistema.
5. **NO introducir notebooks (`.ipynb`), Colab ni código muerto:** Solo código modular en `src/`, `api/`, `ui/` y `tests/`.
6. **NO comitear artefactos pesados ni secretos:** Prohibido comitear `model.safetensors`, `.venv/`, `.env`, tokens, bases SQLite o dependencias externas en cuarentena (`.agents/skills/archify/`).

---

## 4. Estándares de Calidad y Verificación

- **Estilo y Linteo:** PEP 8 estricto validado con Ruff (`ruff check .` y `ruff format --check .` deben retornar código 0).
- **Tipado y Docstrings:** Contratos de entrada/salida tipados (`type hints`) y docstrings explicativos del *porqué* en toda API pública.
- **Patrón de Pruebas:** Pruebas unitarias e integradas con `pytest` bajo estructura Arrange-Act-Assert (AAA).
- **Cobertura:** Meta obligatoria $\ge 85\%$ en `src/` y `api/`.
- **Plantilla de PR:** Uso riguroso de `.github/PULL_REQUEST_TEMPLATE.md` en cada entrega.

---

## 5. Uso de Herramientas del Proyecto

1. **Spec Kit (Specify 1.2.2):** Herramienta formal para Spec-Driven Development (SDD). Fases: `specify`, `clarify`, `plan`, `checklist`, `tasks`, `analyze`, `implement`, `converge`.
2. **Archify:** Diagramación arquitectónica declarativa (C4 / vistas de componentes) guardada en `docs/architecture/`. Debe ser auditada con SkillSpector antes de su adopción.
3. **Engram MCP:** Registro y consulta de decisiones arquitectónicas y memoria técnica por HU, manteniendo Git como única fuente oficial de verdad.
4. **GGA (Git Governance Agent / Hooks):** Control preventivo de pre-commit para evitar commits que violen convenciones o incluyan binarios pesados.
