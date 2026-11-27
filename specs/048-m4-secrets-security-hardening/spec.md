# Feature Specification: Seguridad, Secretos CI/CD, Protección de Ramas y Auditoría de Datos Personales

**Feature Branch**: `feature/m4-plan-01-specs-048-050`

**Created**: 2026-11-23

**Status**: Draft (Prospectiva — elaborada antes de configurar secretos o protecciones)

**Input**: Issue `#50` (`[M4-SEC]`) — Definición prospectiva del manejo seguro de credenciales CI/CD, protección de la rama `develop` en GitLab (`89374502`) y corrección segura de exposición de identificaciones personales sin reescribir historial destructivamente.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Secretos CI/CD protegidos y con privilegios mínimos (Priority: P1)

Como responsable de seguridad M4, quiero que todas las credenciales entre GitHub, GitLab, Container Registry y VPS se almacenen exclusivamente como variables protegidas/enmascaradas con privilegios mínimos y expiración acotada, para cumplir `M4-06` y `TOOL-07` sin riesgo de filtración en código o logs.

**Why this priority**: Representa el 15 % directo de la rúbrica M4 y bloquea de forma segura la sincronización (`#46`), el pipeline (`#48`) y el despliegue (`#51`).

**Independent Test**: Verificar en GitHub Settings y GitLab CI/CD Variables (`89374502`) que las variables requeridas existen marcadas como `Protected` y `Masked`, y que ningún archivo o log imprime valores sensibles.

**Acceptance Scenarios**:

1. **Given** el proyecto GitLab `89374502` y el repositorio GitHub `vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades`, **When** se crean el PrAT (`write_repository`), el Deploy Token (`read_registry`) y las variables SSH de `deploy_vps`, **Then** todos quedan almacenados exclusivamente en GitHub Secrets / GitLab CI/CD Variables (`Protected` + `Masked`) con expiración acotada.
2. **Given** un pipeline ejecutado en GitLab o GitHub Actions, **When** se inspeccionan los logs públicos, **Then** ninguna credencial, llave privada ni IP privada aparece en texto plano.

---

### User Story 2 - Protección de rama `develop` en GitLab (Priority: P1)

Como equipo de desarrollo, quiero que la rama `develop` en GitLab (`89374502`) esté protegida contra `force push` y modificaciones manuales, permitiendo únicamente el push fast-forward de sincronización desde GitHub, para alinear la política de publicación en Container Registry (`M4-05`).

**Why this priority**: Actualmente `develop` en GitLab figura con `protected=False`; protegerla evita divergencias y habilita el acceso a variables protegidas en CI/CD.

**Independent Test**: Consultar `glab api projects/89374502/repository/branches/develop` y confirmar `protected == true` y `allow_force_push == false`.

**Acceptance Scenarios**:

1. **Given** la rama `develop` desprotegida en GitLab `89374502`, **When** un `Owner` aplica la regla de protección, **Then** `protected` pasa a `true` y `allow_force_push` a `false`, permitiendo push fast-forward a la identidad autorizada de sincronización.

---

### User Story 3 - Auditoría y corrección segura de datos personales (Priority: P2)

Como equipo M4, quiero auditar el repositorio y la documentación pública en busca de identificaciones personales o correos sensibles expuestos y corregirlos de forma segura mediante commits limpios (sin `git filter-repo` ni reescritura destructiva de historial), para mantener higiene institucional antes de la sustentación.

**Why this priority**: Previene exposición innecesaria de datos personales respetando la prohibición de reescribir historial en `AGENTS.md` § 3.

**Independent Test**: Ejecutar búsqueda automatizada de patrones sensibles sobre el árbol de trabajo y verificar que no existen identificaciones personales indebidas en documentación o configuraciones.

**Acceptance Scenarios**:

1. **Given** una revisión sistemática de `docs/`, `deploy/`, `specs/` y configuraciones, **When** se detecte cualquier dato personal innecesario en archivos versionados, **Then** se reemplaza mediante PR limpia sin alterar historial Git (`no force-push`, `no rebase`).

### Edge Cases

- **Rotación de tokens expirados:** Si un PrAT o Deploy Token caduca, debe rotarse en GitLab y actualizarse en GitHub Secrets/CI Variables sin dejar valores antiguos en archivos locales.
- **Variables protegidas en ramas no protegidas:** Si `develop` no se marca como protegida en GitLab, los jobs en `develop` no podrán leer variables marcadas como `Protected`.

## Requirements *(mandatory)*

- **FR-001**: Toda credencial (`GITLAB_SYNC_TOKEN`, `DEPLOY_TOKEN`, `SSH_PRIVATE_KEY`, `SSH_KNOWN_HOSTS`, `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_PATH`, `PUBLIC_HOST`, `LETSENCRYPT_EMAIL`) DEBE residir fuera de Git en Secrets/Variables protegidas y enmascaradas (cuando aplique).
- **FR-002**: La rama `develop` en GitLab `89374502` DEBE configurarse como protegida con `allow_force_push = false`.
- **FR-003**: Cualquier corrección de datos personales en archivos versionados DEBE realizarse sin reescritura destructiva de historial Git.

### Key Entities

- **GitHub Repository Secrets:** Almacén de credenciales para workflows autorizados (`GITLAB_SYNC_TOKEN`).
- **GitLab CI/CD Variables (`89374502`):** Almacén protegido/enmascarado para `deploy_vps` y Registry.

## Success Criteria *(mandatory)*

- **SC-001**: 100 % de las variables sensibles configuradas como `Protected`/`Masked` y `0` secretos detectados en el repositorio o logs.
- **SC-002**: `develop` en GitLab `89374502` verificada con `protected=true` y `allow_force_push=false` vía `glab api`.
- **SC-003**: Auditoría documental limpia de identificaciones personales antes del `28/11/2026`.

---

<!-- [M1-M4 GOVERNANCE EXTENSION] -->
## M1–M4 Academic Alignment & Protected Capabilities

> **Referencias normativas:** [AGENTS.md](../../AGENTS.md) · [Constitución](../../.specify/memory/constitution.md) · [Matriz Académica M1–M4](../../docs/academic-compliance-matrix.md)

- **ID Estable y Trazabilidad:** `SPEC-048` | **Issue:** `#50` (`@JhonatanTC99`) | **Condición temporal:** **Prospectiva**.
- **Requisitos académicos aplicables:** `M4-06`, `TOOL-06`, `TOOL-07`.
- **Tecnologías prohibidas:** Streamlit, `pip`, `requirements.txt`, `.ipynb`.
- **Capacidades protegidas:** Contratos M3, `.env` ignorado, `.github/PULL_REQUEST_TEMPLATE.md` intacta y `specs/001..040/`.
<!-- [/M1-M4 GOVERNANCE EXTENSION] -->
