# Guía de Preparación del Entorno y Gobernanza (Getting Started)
<!-- Grupo 2 — Maestría en IA y Ciencia de Datos | UAO -->

Esta guía proporciona las instrucciones paso a paso para que cualquier integrante del Grupo 2 (Santiago, José, Jhonatan o John) reproduzca el entorno de desarrollo industrial, la gobernanza de agentes, el Spec Kit, las skills y la memoria técnica en **Windows** sin dependencias globales innecesarias.

---

## 1. Prerrequisitos del Sistema

1. **Sistema Operativo:** Windows 10 u 11 (PowerShell 5.1+ o PowerShell 7+).
2. **Gestor de Entorno Python:** `uv` (instalado en el sistema; no requiere instalación manual de Python global ya que `uv` gestiona Python 3.13 automáticamente).
   ```powershell
   # Si no tiene uv instalado:
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```
3. **Runtime de Node.js:** Node.js v18+ (necesario exclusivamente para ejecutar el renderizador de diagramas de Archify).
   ```powershell
   node --version  # Debe responder >= v18.0.0
   ```
4. **Git:** Git 2.40+ configurado con credenciales de GitHub.

---

## 2. Clonación y Sincronización del Proyecto

```powershell
# 1. Clonar el repositorio
git clone https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades.git
cd uao-gestion-proyectos-ia-deteccion-enfermedades

# 2. Situarse en develop (rama de integración)
git checkout develop

# 3. Sincronizar el entorno virtual determinista con uv (Python 3.13)
uv sync

# 4. Verificar calidad estática y suite de pruebas
uv run ruff check .
uv run ruff format --check .
uv run pytest -v
```

> [!IMPORTANT]
> Queda estrictamente prohibido utilizar `pip install`, crear entornos con `virtualenv`/`conda` o generar archivos `requirements.txt`. Toda dependencia se gestiona con `uv add` o `uv sync`.

---

## 3. Configuración de Spec Kit (Specify 1.2.2) y Gemini

El repositorio ya contiene la infraestructura compartida de Spec Kit versionada:
- `.specify/`: plantillas (`templates/`), scripts PowerShell (`scripts/powershell/`) y Constitución del proyecto (`memory/constitution.md`).
- `.gemini/commands/`: comandos slash para interacción con Gemini CLI (`speckit.specify`, `speckit.plan`, `speckit.tasks`, etc.).
- `specs/`: catálogo de especificaciones funcionales por unidad y backlog trazado.

### Comandos de Spec Kit disponibles:
Los scripts de PowerShell se encuentran en `.specify/scripts/powershell/`:
```powershell
# Crear o consultar una especificación (sin conmutar ramas Git):
powershell -ExecutionPolicy Bypass -File .specify/scripts/powershell/create-new-feature.ps1 -ShortName "mi-feature" -Number 002 "Descripcion de la funcionalidad"

# Generar plan de implementación a partir de la plantilla compartida:
powershell -ExecutionPolicy Bypass -File .specify/scripts/powershell/setup-plan.ps1

# Generar tareas a partir de la plantilla de tareas:
powershell -ExecutionPolicy Bypass -File .specify/scripts/powershell/setup-tasks.ps1
```

---

## 4. Diagramación Arquitectónica con Archify

La skill **Archify (v3.2.0)** se encuentra integrada en el alcance del proyecto dentro de `.agents/skills/archify/` y ha sido auditada previamente con **SkillSpector**.

### Verificación del funcionamiento:
```powershell
node .agents/skills/archify/bin/archify.mjs doctor
```
El resultado debe mostrar `Archify is ready.` con todas las verificaciones en `[ok]`.

### Generar o actualizar diagramas arquitectónicos:
```powershell
# Renderizar arquitectura a HTML interactivo y validar esquema:
node .agents/skills/archify/bin/archify.mjs render architecture docs/architecture/system-architecture.json docs/architecture/system-architecture.html

# Los diagramas generados quedan disponibles en:
# - docs/architecture/system-architecture.html (Interactivo con controles, zoom y temas)
# - docs/architecture/system-architecture.svg (Exportación vectorial legible)
```

---

## 5. Memoria Técnica con Engram MCP

**Engram MCP** permite registrar y consultar decisiones arquitectónicas, convenciones y descubrimientos por Historia de Usuario entre sesiones.

### Directrices de Gobernanza:
- **Git y Spec Kit son la única fuente oficial de verdad:** Los requisitos, especificaciones y criterios de aceptación residen en Git. Engram almacena memoria técnica auxiliar.
- **Sin compartir bases de datos locales ni secretos:** El archivo de base de datos local (`engram.db` o SQLite) está protegido en `.gitignore` y nunca se comitea.
- **Configuración local de MCP (`mcp_config.json`):**
  Si utiliza Gemini CLI, Antigravity o Claude Desktop, configure el servidor MCP apuntando a la instalación local sin rutas absolutas fijas de otros usuarios:
  ```json
  {
    "mcpServers": {
      "engram": {
        "command": "uv",
        "args": ["run", "engram-mcp"],
        "env": {
          "ENGRAM_DB_PATH": "./.engram.db"
        }
      }
    }
  }
  ```

### Protocolo de Registro de Decisiones por HU:
Al tomar una decisión de diseño relevante para una Historia de Usuario (ej. HU-02, HU-03):
1. **Registrar decisión:**
   ```text
   mem_save(
     project="uao-deteccion-enfermedades",
     type="decision",
     topic="HU-03-safetensors-loader",
     content="Se optó por carga en CPU mediante safetensors.torch con torch.no_grad() sin conexión a Hugging Face Hub para cumplir AC3.1 y AC3.2."
   )
   ```
2. **Consultar antecedentes antes de implementar:**
   ```text
   mem_search(query="HU-03 inferencia CPU latencia")
   ```

---

## 6. Control Preventivo de Commits y Gobernanza Gitflow

### Política de Commits y Ramas:
1. **Ramas protegidas:** Prohibido hacer commits directos a `main` o `develop`.
2. **Crear rama de trabajo:**
   ```powershell
   git checkout develop
   git pull origin develop
   git checkout -b feature/HU-XX-descripcion-breve
   ```
3. **Flujo TDD (Test-First):**
   - Escribir pruebas en `tests/unit/test_<modulo>.py` bajo patrón Arrange-Act-Assert (AAA).
   - Implementar código en `src/` o `api/`.
   - Validar linteo: `uv run ruff check .` y `uv run ruff format --check .`.
   - Validar suite: `uv run pytest -v` (tiempo de unitarias $< 10$\,s, cobertura $\ge 85\%$).
4. **Verificación preventiva antes de commitear:**
   - Asegurarse de que `model.safetensors`, `.venv/`, `.env` o bases de datos no estén staged (`git status`).
   - Usar *Conventional Commits*: `feat(hu-02): preprocesamiento y contratos de tensores`.
5. **Crear Pull Request:**
   - Abrir PR hacia `develop` utilizando obligatoriamente `.github/PULL_REQUEST_TEMPLATE.md`.
   - Completar la sección 10 ("Firma y revisión").
   - Solicitar revisión a un compañero (Jhonatan Tapia actúa como Code Reviewer general).
   - **La fusión a `develop` la realiza el autor únicamente tras contar con la aprobación explícita de un par.**
