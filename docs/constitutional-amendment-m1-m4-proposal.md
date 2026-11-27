# Propuesta de Enmienda Constitucional (M1–M4)

**Estado:** `BORRADOR — PENDIENTE DE APROBACIÓN UNÁNIME`  
**Unidad origen:** `GOV-03A` ([SPEC-042](../specs/042-gov-03a-agents-constitution-proposal/spec.md))  
**Documento objetivo (sin modificar):** [.specify/memory/constitution.md](../.specify/memory/constitution.md) (v1.0.0, ratificada `2026-11-12`)  
**Requisito de aprobación:** Consenso unánime de los **4 integrantes del Grupo 2** (`.specify/memory/constitution.md`, § Gobernanza y Enmiendas) y trazabilidad en `M4-09`.

> **Nota:** Este documento **no** modifica la Constitución vigente. Presenta las reformas mínimas necesarias para alinear la Constitución (redactada en M3) con la realidad técnica verificada y los requisitos acumulativos `M1`–`M4`.

---

## Resumen de Enmiendas Propuestas

| ID | Sección afectada | Motivo / Discrepancia | Requisitos relacionados |
| :--- | :--- | :--- | :--- |
| `ENM-01` | Preámbulo y Gobernanza | Incorporar jerarquía acumulativa `M1`–`M4` (`M4 > M3 > M2 > M1` solo ante incompatibilidad). | `M1`–`M4`, `TOOL-08` |
| `ENM-02` | Principio I (Excepciones y Endpoints) | Alinear nombres reales de excepciones (`D-05`) y listar `GET /model-info` (`M3-03`). | `M3-03`, `M3-04`, `D-05` |
| `ENM-03` | Principio I (Frontend desacoplado) | Incluir frontend web estático y prohibición expresa de Streamlit (`M3-02`, `D-04`). | `M3-02`, `D-04` |
| `ENM-04` | Principio II (`requires-python`) | Resolver rango Python en `pyproject.toml` vs Constitución/SPEC-010 (`D-03`). | `M1-02`, `D-03` |
| `ENM-05` | Principio III y V (Pruebas y LFS) | Incorporar mínimo académico de 120 pruebas y aclarar uso de Git LFS para `model.safetensors` (`D-08`). | `M1-03`, `M1-06`, `D-08` |
| `ENM-06` | Roles y Quality Gates | Actualizar estado de `HU-08` base (hecha en M3) vs M4 (`D-02`) y añadir Gates M4 (`M4-01..M4-12`). | `M4-01..M4-12`, `D-02` |
| `ENM-07` | Gobernanza y Herramientas | Referenciar `docs/academic-compliance-matrix.md` como SSOT y coordinación GitHub/GitLab (`TOOL-01..09`). | `M4-09`, `TOOL-01..09` |

---

## Detalle de Enmiendas

### `ENM-01` — Jerarquía normativa y alcance acumulativo M1–M4
- **Texto actual afectado** (`.specify/memory/constitution.md`, § Preámbulo y § Gobernanza y Enmiendas):
  > *«Esta Constitución define los principios de gobernanza técnica [...] basado en visión artificial (DINOv2) en CPU.»* / *«La presente Constitución tiene rango supremo sobre cualquier convención no documentada.»*
- **Redacción propuesta:**
  > *«Esta Constitución rige de forma subordinada a las instrucciones del usuario y a las reglas académicas oficiales del curso, las cuales son acumulativas (`M1`–`M4`). Únicamente ante incompatibilidad explícita entre reglas oficiales prevalece la posterior (`M4 > M3 > M2 > M1`).»*
- **Justificación:** Evita rigidez entre hitos y formaliza la precedencia declarada en `GOV-02` y `GOV-03A`.
- **Requisitos académicos relacionados:** `M1`–`M4`, `M4-09`, `TOOL-08`.
- **Impactos:** Ninguno en código; clarifica la jerarquía normativa para humanos y agentes.

### `ENM-02` — Alinear excepciones de preprocesamiento y endpoints FastAPI (`D-05`)
- **Texto actual afectado** (Principio I, viñetas `src/preprocessing.py` y `api/main.py`):
  > *«Lanza `InvalidImageFormatException` ante archivos corruptos o formatos inválidos.»* / *«endpoints `GET /health`, `POST /predict` y `GET /docs`»*
- **Redacción propuesta:**
  > *«Lanza `ImageValidationError` (`CorruptedImageError`, `UnsupportedImageFormatError`, `ImageSizeExceededError`, definidos en `src/exceptions.py`) ante archivos inválidos.»* / *«endpoints `GET /health`, `GET /model-info`, `POST /predict` y `GET /docs`»*
- **Justificación:** Corrige la discrepancia `D-05` entre el nombre histórico en la Constitución y la implementación real verificada.
- **Requisitos académicos relacionados:** `M3-03`, `M3-04`.
- **Impactos:** Elimina ambigüedad documental; sin cambios en código ni pruebas.

### `ENM-03` — Frontend desacoplado Web + Desktop y prohibición de Streamlit (`D-04`)
- **Texto actual afectado** (Principio I, viñeta `ui/`):
  > *«`ui/desktop_app.py` y `ui/api_client.py`: Interfaz de usuario de escritorio desacoplada para técnicos de campo, consumiendo la API vía cliente HTTP.»*
- **Redacción propuesta:**
  > *«`ui/desktop_app.py`, `ui/api_client.py` y `ui/web/static/`: Interfaces desacopladas (escritorio Tkinter y web HTML/CSS/JS) que consumen la API exclusivamente vía HTTP. Queda expresamente prohibido el uso de Streamlit como interfaz evaluable en M3 y M4.»*
- **Justificación:** Incorpora la decisión arquitectónica `D-01` (`specs/032`) y el frontend web implementado en M3.
- **Requisitos académicos relacionados:** `M3-02`, `M1-01`.
- **Impactos:** Refuerza la prohibición evaluativa de Streamlit en M4.

### `ENM-04` — Precisión del rango Python (`D-03`)
- **Texto actual afectado** (Principio II):
  > *«Se utiliza exclusivamente `uv` sobre Python 3.13.»*
- **Redacción propuesta:**
  > *«Se utiliza `uv` con Python 3.13 como versión objetivo de ejecución y CI (`.python-version` = `3.13`, `pyproject.toml` `requires-python` = `">=3.12,<3.14"` o `">=3.13,<3.14"` según decida el equipo).»*
- **Justificación:** Resuelve explícitamente la discrepancia `D-03` entre `.python-version`/`SPEC-010` y `pyproject.toml`.
- **Requisitos académicos relacionados:** `M1-02`.
- **Impactos:** Requiere decisión humana sobre si restringir `pyproject.toml` a `>=3.13,<3.14` o mantener compatibilidad `>=3.12,<3.14`.

### `ENM-05` — Umbral mínimo de pruebas y Git LFS para pesos (`D-08`)
- **Texto actual afectado** (Principio III y Principio V):
  > Cobertura $\ge 85\%$ sin mencionar explícitamente el piso de 120 pruebas; Principio V prohíbe `*.safetensors` sin mencionar la excepción versionada por Git LFS.
- **Redacción propuesta:**
  > En Principio III: añadir *«Mínimo académico de 120 pruebas AAA sin reducir las capacidades vigentes.»* En Principio V: aclarar *«Prohibido subir pesos binarios directamente al historial Git estándar; `model.safetensors` se gestiona exclusivamente mediante Git LFS (`.gitattributes`), prohibiendo binarios sin LFS, secretos y bases de datos locales no autorizadas.»*
- **Justificación:** Alineación con `M1-03`, `M1-06` y la realidad de `.gitattributes` / `.gitignore` (`D-08`).
- **Requisitos académicos relacionados:** `M1-03`, `M1-06`, `M4-06`.
- **Impactos:** Evita falsas contradicciones sobre el versionado LFS del modelo.

### `ENM-06` — Estado de `HU-08` y Quality Gates de M4 (`D-02`, `M4-01..M4-12`)
- **Texto actual afectado** (Tabla de Roles y sección *Puertas de Calidad (Quality Gates) para M3*):
  > Trata `HU-08` como trabajo futuro M4 y limita las puertas de calidad a M3.
- **Redacción propuesta:**
  > Distinguir `HU-08 base` (Wheel y Docker CPU/Compose implementados en M3) de `M4` (pipeline CI/CD completo `lint → test → build → deploy` en GitLab, Container Registry, VPS, HTTPS/TLS, secretos en CI/CD y verificación `GET /health` en producción). Añadir la sección *Puertas de Calidad para M4*.
- **Justificación:** Corrige la obsolescencia `D-02` e incorpora los requisitos `M4-01..M4-12`.
- **Requisitos académicos relacionados:** `M1-05`, `M4-01`..`M4-12`.
- **Impactos:** Habilita la evaluación formal de M4 sin reescribir la historia de M3.

### `ENM-07` — Matriz SSOT y coordinación GitHub / GitLab (`TOOL-01..09`)
- **Texto actual afectado** (Principio IV y Gobernanza):
  > Solo contempla GitHub y no referencia `docs/academic-compliance-matrix.md` ni `Makefile`.
- **Redacción propuesta:**
  > Designar `docs/academic-compliance-matrix.md` como fuente única de trazabilidad de requisitos `M1`–`M4` y capacidades protegidas; reconocer `Makefile` como interfaz operativa estándar; definir a **GitHub** como repositorio principal de código/PR/Kanban y a **GitLab** como plataforma de CI/CD, Container Registry y despliegue M4, sujeto a arquitectura de sincronización aprobada (`TOOL-05`) y uso autorizado de `gh`/`glab`/MCPs.
- **Justificación:** Evita duplicar tablas en la Constitución (`docs/academic-compliance-matrix.md § 4`) e integra las herramientas transversales de M4.
- **Requisitos académicos relacionados:** `M4-09`, `M4-10`, `TOOL-01`..`TOOL-09`.
- **Impactos:** Mantiene la Constitución concisa y prepara la gobernanza M4.

---

## Acta de Aprobación Unánime Requerida (Para uso posterior)

Para ratificar esta enmienda como **Versión 2.0.0** de `.specify/memory/constitution.md`, se requiere la aprobación explícita de los 4 integrantes del Grupo 2:

- [ ] Santiago Correa
- [ ] José Silva
- [ ] Jhonatan Tapia
- [x] John Restrepo — ratificado en Issue #52 (2026-11-26)
