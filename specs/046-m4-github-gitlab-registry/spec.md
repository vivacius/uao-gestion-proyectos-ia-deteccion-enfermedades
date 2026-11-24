# Especificación Técnica (Spec Kit): SPEC-046 Integración GitHub–GitLab y Container Registry

**Identificador:** `SPEC-046`
**Feature Branch:** `feature/m4-github-gitlab-registry`
**Unidad / Historia Asociada:** `M4-03`, `M4-05`, `M4-06`, `TOOL-03`, `TOOL-04`, `TOOL-05`, `TOOL-07`
**Fecha de Elaboración SDD (Prospectiva):** 2026-11-24
**Trazabilidad Temporal:** **Especificación prospectiva elaborada ANTES de implementar el espejo GitHub → GitLab y los ajustes de Registry.**
**Estado:** En progreso — implementación local, sin push
**Responsable:** Frente B — DevOps (asignación por ratificar por el equipo)
**Artefactos Relacionados:** [plan.md](./plan.md) · [tasks.md](./tasks.md) · [docs/deployment-m4.md](../../docs/deployment-m4.md)

---

## 1. Propósito y Alcance

Definir y dejar reproducible la integración entre **GitHub** (fuente oficial de verdad: código, Issues, PRs, Kanban y revisión humana) y el proyecto definitivo de **GitLab** (`vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades`), que actúa como plataforma de CI/CD, Container Registry y despliegue del Módulo 4.

La unidad cubre:

1. **Sincronización automática GitHub → GitLab** disparada por cada push a `develop` (y, cuando la protección de rama lo permita, a `main`), preservando el SHA exacto del commit de origen.
2. **Publicación trazable de la imagen** en el Container Registry del proyecto GitLab, etiquetada con el SHA completo del commit y con `latest` únicamente para ramas de integración.
3. **Carga verificada de los pesos reales** (`model.safetensors`) durante el build, mediante Git LFS y una comprobación de tamaño que impida publicar una imagen con un puntero LFS.
4. **Documentación operativa** de la arquitectura de repositorios, variables requeridas (solo nombres, nunca valores) y verificación de la sincronización.

**Fuera de alcance:** provisión del VPS, TLS/HTTPS y job de despliegue (tratados en `SPEC-047`); cambios en la Constitución, la plantilla de PR, el modelo, la API o los frontends.

---

## 2. Restricciones y Decisiones de Diseño

| Decisión | Justificación |
| :--- | :--- |
| **GitHub es la fuente de verdad; GitLab es espejo de solo lectura para CI/CD.** | Evita divergencia de historia (`D-07`) y mantiene la gobernanza de PRs en GitHub. |
| **El espejo se ejecuta en GitHub Actions** (`mirror-to-gitlab.yml`). | GitLab.com Free no ofrece *pull mirroring*; un workflow en GitHub no requiere intervención manual y conserva el SHA. |
| **Token de GitLab en el secreto `GITLAB_TOKEN` de GitHub.** | Ningún token se versiona. Requiere que un administrador del repo GitHub cree el secreto (la cuenta actual no es admin). |
| **Push con `--force` solo hacia las ramas espejo `develop`/`main`.** | Un espejo debe reflejar exactamente el origen; se documenta como operación de sincronización, no como reescritura de trabajo local. |
| **Tags de imagen: `$CI_COMMIT_SHA` (completo) y `latest`.** | Trazabilidad inmutable por commit y compatibilidad con despliegues que usan `latest`. |
| **Sin secretos en el repositorio, logs, prompts o documentación.** | `TOOL-07` y Constitución § V. |

### 2.1 Bloqueos conocidos (no se declaran resueltos)

- El proyecto definitivo es `vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades` (ID 89374502), público e importado desde GitHub; `develop` está alineada en `589444f` al momento del diagnóstico.
- Los cuatro integrantes, incluida la cuenta `josesilvacalderon111`, tienen rol **Owner** en GitLab y pueden configurar variables, Registry y ramas protegidas.
- La cuenta actual tiene permiso `push` pero **no `admin`** en GitHub: no puede crear el secreto `GITLAB_TOKEN`. Requiere acción del propietario del repositorio.
- No hay VPS ni dominio aprovisionados; el despliegue real de `SPEC-047` permanece bloqueado hasta contar con esa infraestructura y autorización humana.

---

## 3. Escenarios de Aceptación (Gherkin)

### AC46.1 — Espejo automático en cada push a `develop`
- **Dado** un push autorizado a `develop` en GitHub y el secreto `GITLAB_TOKEN` configurado,
- **Cuando** se ejecuta el workflow `Mirror to GitLab`,
- **Entonces** la rama `develop` de GitLab queda apuntando exactamente al mismo SHA que GitHub, y el pipeline de GitLab se dispara sobre ese commit.

### AC46.2 — Espejo de `main` sin eludir la protección
- **Dado** un push autorizado a `main` en GitHub,
- **Cuando** el workflow intenta actualizar `main` en GitLab,
- **Entonces** la operación solo tiene éxito si la identidad del token está autorizada explícitamente para pushear a la rama protegida; en caso contrario el workflow falla de forma visible y no altera la rama.

### AC46.3 — Pesos reales en la imagen
- **Dado** el job `build_docker` en GitLab,
- **Cuando** construye la imagen,
- **Entonces** descarga los objetos Git LFS, verifica que `model.safetensors` supere 1 MB antes del build y falla si encuentra un puntero LFS.

### AC46.4 — Imagen trazable por commit
- **Dado** un build exitoso en `develop` o `main`,
- **Cuando** se publica la imagen,
- **Entonces** el Registry contiene el tag con el SHA completo del commit y el tag `latest`, y la imagen incluye las etiquetas OCI `org.opencontainers.image.revision` y `org.opencontainers.image.source`.

### AC46.5 — Cero secretos expuestos
- **Dado** el diff de la unidad,
- **Cuando** se revisa el repositorio y los logs del pipeline,
- **Entonces** no aparece ningún token, clave SSH, IP privada ni valor de variable protegida; solo se documentan nombres de variables.

---

## 4. Requisitos Trazables

| ID | Requisito | Evidencia esperada |
| :--- | :--- | :--- |
| `M4-03` | Pipeline CI/CD con etapas `quality → test → build → deploy`. | `.gitlab-ci.yml` válido y ejecutado en GitLab. |
| `M4-05` | Publicación en Container Registry con tags trazables. | Tag `$CI_COMMIT_SHA` visible en el Registry. |
| `M4-06` | Gestión segura de secretos. | Variables protegidas/enmascaradas; `.env` fuera de Git. |
| `TOOL-03` | GitLab como plataforma de CI/CD y Registry. | Proyecto `vivacius/...` con pipeline e imágenes. |
| `TOOL-05` | Integración GitHub ↔ GitLab definida y verificada. | Workflow de espejo y evidencia de SHAs iguales. |
| `TOOL-07` | Prohibición de exponer credenciales. | Auditoría del diff y de los logs. |

---

## 5. Capacidades Protegidas que No Se Modifican

- `src/`, `api/`, `ui/` (sin Streamlit), `Dockerfile` CPU multi-etapa y `MODEL_DIR=/app/modelo_plantas`.
- `docker-compose.yml` local y `deploy/nginx.conf` local (el despliegue productivo usa archivos separados).
- Suite `tests/`, umbral de cobertura ≥ 85 %, Ruff y Gitflow.
- Carácter retrospectivo de `specs/010..040/` y plantilla oficial de PR.

---

## 6. Criterio de Cierre

La unidad se considera **verificada** solo cuando exista evidencia remota de: workflow de espejo en verde, `develop` de GitLab con el mismo SHA que GitHub, pipeline de GitLab en verde y tag de imagen con el SHA completo. Mientras falten el token o los permisos, el estado es **implementado localmente, no verificado**.
