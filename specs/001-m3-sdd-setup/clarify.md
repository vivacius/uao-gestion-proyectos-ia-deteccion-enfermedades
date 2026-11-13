# Clarificaciones Técnicas y Desriesgo (Clarify) — Unidad M3-G2

**Feature**: `001-m3-sdd-setup`
**Fecha**: 2026-11-12
**Participantes**: Equipo Grupo 2 (Santiago Correa, José Silva, Jhonatan Tapia, John Restrepo) y Asistente Técnico Gemini.

---

## 1. Preguntas Clave y Clarificaciones de Alcance

### Q1: Delimitación de alcance entre Módulo 3 y Módulo 4
- **Pregunta:** ¿Se deben construir o validar contenedores Docker, Docker Compose o empaquetar paquetes Wheel en esta unidad M3-G2 o durante el desarrollo del Módulo 3?
- **Clarificación / Decisión:** **NO.** Las actividades de contenerización (Docker multi-etapa), orquestación (Docker Compose) y distribución en Wheel (`uv build`) pertenecen a la **HU-08 (Ticket #11, José Silva)** y quedan expresamente diferidas para el **Módulo 4**. En el Módulo 3 el foco técnico exclusivo es:
  1. Inferencia local con DINOv2 en CPU.
  2. Servicio REST asíncrono con FastAPI (`api/`).
  3. Frontend web desacoplado (`ui/web/`) y aplicación de escritorio Tkinter (`ui/desktop_app.py`) para técnicos.
  4. Suite automatizada con pytest AAA y cobertura $\ge 85\%$ (`tests/`).

### Q2: Estrategia de carga de pesos y conectividad de red en runtime
- **Pregunta:** ¿Cómo debe comportarse el cargador de pesos y qué garantías de aislamiento de red se exigen?
- **Clarificación / Decisión:** La carga debe realizarse estrictamente desde el archivo local `model.safetensors` usando la biblioteca `safetensors.torch`. Queda prohibida cualquier descarga o consulta a Hugging Face Hub durante el ciclo de vida de la aplicación (`local_files_only=True` o carga manual del diccionario de tensores). Los archivos binarios pesados (`*.safetensors`, `*.pt`, `*.bin`) están protegidos en `.gitignore` y no se suben al repositorio remoto.

### Q3: Metas de latencia y protocolos de medición
- **Pregunta:** ¿Cómo se evalúan las metas de $< 300$\,ms para inferencia pura en CPU (HU-03 / AC3.3) y $p95 < 450$\,ms para la API E2E (HU-05 / AC5.2)?
- **Clarificación / Decisión:** Corresponden a metas de rendimiento operacional sobre una CPU de referencia de 2 vCPUs bajo protocolo formal de evaluación (warm-up previo de 5 inferencias y promedio sobre 20 repeticiones con lote unitario $N=1$). En la suite de pruebas unitarias regulares, se evalúa la lógica del contrato y se simulan componentes con mocks para garantizar que la suite corra en $< 10$\,s (AC7.1). Las pruebas de latencia se ejecutan en scripts dedicados de benchmark o pruebas de integración.

### Q4: Integración de Skills externas (Archify) y Política de Seguridad
- **Pregunta:** ¿Cuál es el requisito de seguridad antes de habilitar e integrar Archify en el proyecto?
- **Clarificación / Decisión:** Se exige una auditoría estática local completa mediante **SkillSpector** sobre la totalidad del repositorio y recursos de la skill (`tt-a1i/archify`), inspeccionando permisos de ejecución, invocaciones a subshell, accesos a red y manipulación de archivos. La skill solo puede ser integrada si el reporte concluye con 0 hallazgos CRITICAL y 0 HIGH no mitigados.

### Q5: Gestión de Memoria Técnica (Engram MCP) y Control de Commits (GGA)
- **Pregunta:** ¿Cómo se comparten las configuraciones de Engram MCP y GGA entre los miembros sin generar dependencias de ruta absoluta ni filtrar información privada?
- **Clarificación / Decisión:**
  - **Engram MCP:** Se documenta una plantilla de configuración de cliente MCP (`claude_desktop_config.json` / Antigravity MCP) con rutas parametrizadas (`${WORKSPACE_ROOT}`) y almacenamiento en base de datos local no versionada (`engram.db` excluida en `.gitignore`). Git y Spec Kit continúan siendo la única fuente oficial de requisitos y tareas.
  - **GGA (Git Governance Agent):** Se verifica su soporte en Windows y Python 3.13 con `uv`. Si requiere dependencias globales o herramientas no estándar, se documenta su integración como hook preventivo opcional o se reporta la restricción sin forzar instalaciones improvisadas.

### Q6: Autonomía de Scripts en Spec Kit y Gestión de Ramas Git
- **Pregunta:** ¿Los scripts de Spec Kit (`create-new-feature.ps1`, etc.) pueden o deben crear o conmutar ramas de Git automáticamente?
- **Clarificación / Decisión:** **NO.** Para cumplir rigurosamente con la gobernanza de Gitflow y evitar manipulaciones no supervisadas del árbol de trabajo, los scripts de Spec Kit se ejecutan con parámetros explícitos de directorio y persistencia (`001-m3-sdd-setup`), mientras que la rama activa de Git (`feature/m3-sdd-setup`) es gestionada de forma controlada y explícita por el desarrollador.
