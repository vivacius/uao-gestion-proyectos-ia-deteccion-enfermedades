<!--
╔══════════════════════════════════════════════════════════════════════════╗
║  📌 INSTRUCCIONES PARA ESTUDIANTES UAO — Gestión de Proyectos en IA y CD ║
╚══════════════════════════════════════════════════════════════════════════╝

1. Copia este archivo TAL CUAL a `.github/PULL_REQUEST_TEMPLATE.md` en la raíz
   de tu repositorio. GitHub lo cargará automáticamente en cada Pull Request.
2. Una PR = UN solo propósito (una funcionalidad, una corrección o un refactor
   pequeño). Si mezclas varias historias, la revisión se rechaza.
3. La PR NO se fusiona sin al menos UNA revisión aprobada de otro integrante.
4. Aplica a los 6 proyectos del Módulo 1 (Neumonía · PCBA · Subacuática ·
   Metal · Tela · AI Model Recovery): cambia solo los nombres de los módulos
   de tu caso.
-->

## 1. Identificación de la Pull Request

| Campo | Valor |
| :--- | :--- |
| **Equipo / Grupo** | *(ej. Grupo 3 — Visión Industrial)* |
| **Integrantes que participaron** | *(nombres de quienes escribieron código en esta PR)* |
| **Proyecto del Módulo 1** | *(uno de los 6: Neumonía · PCBA · Subacuática · Metal · Tela · AI Doctors)* |
| **Rama origen ➔ destino** | `feature/…` ➔ `develop` |
| **Issue / Ticket asociado** | `#__` *(tablero de GitHub Projects)* |
| **Módulo / Entrega** | *(ej. M1 — Semana 2)* |

---

## 2. Título de la Pull Request (Conventional Commits)

El título **debe** comenzar con un prefijo, escribirse en imperativo y tener **≤ 72 caracteres**.

| Prefijo | Cuándo usarlo | Ejemplo |
| :--- | :--- | :--- |
| `feat:` | Nueva funcionalidad o módulo MVC | `feat(preprocess): parametrizar CLAHE y resize` |
| `fix:` | Corrección de bug, warning o deprecación | `fix(load_model): corregir ruta del artefacto en CPU` |
| `test:` | Pruebas unitarias nuevas o refactorizadas | `test(detector): 24 pruebas AAA para bounding boxes` |
| `refactor:` | Clean Code sin cambiar el comportamiento | `refactor(integrator): inyectar el preprocesador por contrato` |
| `chore:` | Docker, `uv`, Makefile, CI, dependencias | `chore(ci): agregar job de pytest en GitHub Actions` |
| `docs:` | README, docstrings masivos, `docs/` | `docs(readme): badges y diagrama de arquitectura` |

> 💡 Puedes añadir alcance entre paréntesis: `feat(read_img): …`

---

## 3. Tipo de cambio

- [ ] `feat` — Nueva funcionalidad
- [ ] `fix` — Corrección de error
- [ ] `test` — Pruebas unitarias
- [ ] `refactor` — Mejora de estructura (Clean Code)
- [ ] `chore` — Infraestructura, dependencias o contenedor
- [ ] `docs` — Documentación
- [ ] ⚠️ **Breaking change** (si lo marcas, describe el impacto en la sección 8)

---

## 4. Capas MVC y archivos afectados

Marca las capas que toca esta PR (ajusta los nombres a los módulos de tu caso):

- [ ] **Modelo (Model)** — carga del artefacto, inferencia, explicabilidad
      (`load_*.py`, `explain_*.py` / `grad_cam.py` / `detect_*.py`)
- [ ] **Controlador (Controller)** — lectura, preprocesamiento y orquestación
      (`read_*.py`, `preprocess_*.py` / `*_extractor.py`, `integrator.py`)
- [ ] **Vista (View)** — interfaz y reporte
      (`app.py`, `report.py`)
- [ ] **Pruebas** (`tests/test_*.py`)
- [ ] **Infraestructura** (`Dockerfile`, `pyproject.toml`, `uv.lock`, `Makefile`, `.github/workflows/`)
- [ ] **Documentación y licencia** (`README.md`, `docs/**`, `LICENSE`)

---

## 5. Descripción de los cambios

**Historia de usuario / problema que resuelve:**
*(ej. «Como analista necesito que la UI acepte imágenes que no son JPG para no fallar en la demo»)*

### 📝 Resumen técnico
*(qué cambió, en qué archivos y por qué; sé concreto)*
-

### 🧩 Justificación de diseño (Clean Code)
- **Alta cohesión:** *(por qué este módulo tiene una única responsabilidad)*
- **Bajo acoplamiento:** *(qué contrato/interfaz se usa y qué NO se conoce del módulo vecino)*
- **Contrato de entrada/salida:** *(firma y tipos; ej. `uint8 (H,W) ➔ float32 (1,512,512,1)`)*

### 🔀 Alternativas consideradas y trade-offs
- **Opción A:** … **Opción B:** … → **Elegida:** … porque…

---

## 6. Evidencia de pruebas (obligatoria)

```bash
# Ejecutar SOLO lo relacionado con esta PR y luego la suite completa
uv run pytest -v tests/test_<modulo>.py
uv run pytest -v
uv run ruff check src/ tests/

# Verificar el contenedor (si esta PR toca Docker o dependencias)
docker build -t <proyecto>:pr .
```

| Métrica | Valor |
| :--- | :--- |
| **Pruebas nuevas en esta PR** | __ |
| **Total acumulado del proyecto** | __ *(mínimo exigido: **120**)* |
| **Cobertura del módulo tocado** | __ % |

- [ ] Adjunté la **salida de `pytest`** o una captura de pantalla con el resultado.
- [ ] El pipeline de **GitHub Actions** quedó en verde.

---

## 7. Checklist obligatorio pre-PR (Reglas de Juego UAO)

**Entorno y dependencias**
- [ ] Corrí todo con **`uv`** sobre **Python 3.13** (sin `pip`, sin `requirements.txt`).
- [ ] `uv run pytest -v` pasa **completo** y sin *warnings* ni deprecaciones.
- [ ] `uv run ruff check src/ tests/` sin hallazgos (PEP 8).
- [ ] Si agregué una dependencia, actualicé `pyproject.toml` **y** `uv.lock` en el mismo commit.

**Calidad de código**
- [ ] Docstrings y *type hints* en cada función/clase pública.
- [ ] Sin `print()` de depuración, sin código comentado muerto y sin `TODO` sin issue.
- [ ] Nombres descriptivos; una sola responsabilidad por función.
- [ ] Sin credenciales, tokens ni rutas personales en el código.

**Estructura del repositorio**
- [ ] Código en `src/`, pruebas en `tests/`, sin `.ipynb`, Colab ni Kaggle.
- [ ] `.gitignore` cubre pesos (`*.h5`, `*.pt`, `*.onnx`, `*.joblib`), `data/raw/`, `.venv/` y `.ipynb`.
- [ ] Verifiqué que **ningún archivo binario pesado** entró al commit (`git status`).

**Contenedor y UI**
- [ ] `docker build` construye y `docker run` ejecuta la inferencia **en CPU**.
- [ ] La interfaz (Streamlit o Tkinter) sigue funcionando con este cambio.

**Git y proceso**
- [ ] La PR es **pequeña y de un solo propósito**; la rama está actualizada desde `develop`.
- [ ] Los commits usan *Conventional Commits* con mensajes descriptivos.
- [ ] Asigné **revisor** (otro integrante) y etiquetas a la PR.

---

## 8. Impacto y riesgos

- **Módulos / archivos de mayor riesgo:** …
- **¿Rompe compatibilidad?** Sí / No — *si aplica, describe la migración*
- **Plan de reversión:** *(ej. `git revert` o restaurar desde la rama `develop`)*
- **¿Requiere datos, pesos o servicios externos para probarse?** *(idealmente no)*

---

## 9. Checklist del revisor (para el compañero que aprueba)

- [ ] El código hace **exactamente** lo que promete el título (alcance cerrado).
- [ ] Se respeta la **responsabilidad única** de cada módulo (alta cohesión).
- [ ] El módulo nuevo **no** accede a estructuras internas de otro (bajo acoplamiento).
- [ ] Las pruebas cubren casos borde: entrada vacía, `NaN`, forma/dimensión y tipo de dato.
- [ ] No hay secretos, binarios pesados ni `.ipynb` en el diff.
- [ ] Ausencia de duplicación innecesaria; nombres claros.
- [ ] Comentarios y docstrings explican **el porqué**, no el qué obvio.
- [ ] Aprobada por **al menos un integrante** antes de fusionar a `develop`.

---

## 10. Firma y revisión

| Integrante | Rol en la PR | ¿Revisó y aprobó? |
| :--- | :--- | :--- |
| | Autor / Desarrollador | — |
| | Revisor de código | [ ] Aprobado |
| | Revisor de código | [ ] Aprobado |

> 🔒 **Regla del curso:** la fusión a `develop` la hace el autor **después** de la aprobación de un compañero; a `main` solo se fusiona en los hitos de entrega.
