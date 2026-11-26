# Post-Mortem Técnico y Lecciones Aprendidas (M1–M4)

**Fecha:** `2026-11-25`  
**Alcance:** Incidentes reales observados durante la integración M3–M4 del Grupo 2 (UAO).

---

## 1. Incidentes Reales Documentados

| ID | Incidente observado | Causa raíz | Resolución aplicada |
| :--- | :--- | :--- | :--- |
| **INC-01** | Diagrama Archify `system-architecture.svg` renderizado en negro en `README.md` de GitHub (PR #36). | El sanitizador de GitHub elimina bloques `<style>` y variables CSS de SVG embebidos como imagen. | Exportación de `docs/architecture/system-architecture.html` a `docs/architecture/system-architecture.png` (PR #37). |
| **INC-02** | Colisión de numeración SDD `SPEC-046` entre PR #45 (`specs/046-m4-github-gitlab-registry/`) y PR #47 (`specs/046-m4-github-gitlab-sync/`). | Dos ramas desarrolladas en paralelo reservaron el mismo prefijo numérico `046`. | Solicitud de ajuste (`CHANGES REQUESTED`) en PR #45 para conservar la `SPEC-046` de `develop` y mantener `SPEC-047` en PR #45. |
| **INC-03** | Uso de `git push --force` y token en URL remota detectados en revisión de `.github/workflows/mirror-to-gitlab.yml` (PR #45). | Implementación inicial de espejo con fallback `--force` y URL `oauth2:${GITLAB_TOKEN}@...`. | Bloqueo preventivo en revisión cruzada (`@JhonatanTC99` / `@vivacius`) exigiendo `fast-forward` estricto y credencial efímera fuera de URL. |
| **INC-04** | Fallo de `uv run` offline tras agregar `[build-system]` (`setuptools>=77.0.0`) en `pyproject.toml` (PR #33). | `uv run` intenta resolver/compilar el paquete editable en red si no se usa `--no-sync` tras cambios de build-system. | Documentación operativa de `uv sync` tras merges de dependencias y uso de `--no-sync` en entornos sin red. |
| **INC-05** | Exposición de números de cédula (`C.C.`) en `documento/Plantilla.tex` (líneas 106, 108, 110, 112). | Inclusión de identificaciones académicas en el documento LaTeX versionado en repositorio público. | Hallazgo auditado en `SPEC-048` / `Issue #50`; pendiente decisión docente/equipo antes de modificar el documento M2. |

---

## 2. Lecciones Aprendidas Clave

1. **Revisión cruzada obligatoria antes del merge:** Detectó a tiempo el `push --force`, el manejo del token en URL y la colisión `SPEC-046` antes de contaminar `develop`.
2. **Probar renderizado real en GitHub y en vivo:** Un SVG válido localmente puede fallar bajo el sanitizador de GitHub; verificar en la vista real evitó presentar un diagrama roto en sustentación.
3. **Separar PRs por responsabilidad:** Mantener la Enmienda Constitucional (`PR #54`) aislada de cambios documentales o de pipeline agiliza la aprobación unánime (`M4-09`).
