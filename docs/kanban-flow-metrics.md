# Métricas de Flujo y Auditoría Kanban (M1–M4)

**Fecha de corte:** `2026-11-25`  
**Tablero oficial:** [GitHub Project #1 — UAO Grupo 2](https://github.com/users/vivacius/projects/1)  
**Repositorio:** `vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades`

---

## 1. Política WIP y Estructura del Tablero

El tablero utiliza exactamente cuatro columnas de flujo continuo:

| Columna | Límite WIP | Estado al `2026-11-25` | Ítems activos |
| :--- | :---: | :---: | :--- |
| **Backlog** | Sin límite | 3 | `#49`, `#50`, `#51` |
| **In Progress** | Máx. **4** (1/dev) | 1 | `#46` |
| **In Review** | Máx. **2** | 2 | `#48` (PR #45), `#52` (PR #54) |
| **Done** | Acumulado | 14 | `#4`–`#11`, `#20`–`#22`, `#28`–`#30` |

---

## 2. Throughput Verificado (PRs Fusionados)

Conteo directo desde la API de GitHub al `2026-11-25`: **35 Pull Requests fusionados** en `develop` y `main`.

| Integrante / Cuenta | PRs Fusionados | Notas de Trazabilidad |
| :--- | :---: | :--- |
| `@vivacius` (Santiago Correa) | 12 | `HU-01`, `HU-07`, `SC-01` (#25), `SC-02` (#34), Archify README (#36/#37) |
| `@JhonatanTC99` (Jhonatan Tapia) | 10 | `HU-03`, `HU-05`, MLflow (#31), Gobernanza M4 (#42, #43), `SPEC-046..050` (#47, #53) |
| `@josesilvacalderon111` (José Silva) | 9 | `HU-02`, retiro Streamlit (#32), Docker/Wheel (#33), licencia (#23) |
| `@JohnRestrepo-coder` (John Restrepo) | 3 | `HU-04`, `HU-06` (#22, #27), Model Card (#35) |
| `@jracoder01-jpg` (cuenta auxiliar equipo) | 1 | Pipeline base GitLab `.gitlab-ci.yml` (#44) |
| **Total acumulado** | **35** | **100 % con flujo por PR hacia `develop`/`main`** |

---

## 3. Work Item Age y Nota Metodológica sobre Cycle Time

- **Work Item Age (ítems M4 abiertos desde `2026-11-23`):** los 6 Issues M4 (`#46`, `#48`–`#52`) registran una antigüedad de **2 días** al `2026-11-25`, con `#48` y `#52` ya en `In Review`.
- **Diferenciación metodológica (`Cycle Time`):** GitHub Projects v2 no expone por defecto un log histórico retroactivo de transiciones entre columnas (*In Progress → In Review → Done*). Por honestidad documental (`SPEC-050`, FR-002/FR-003), **no se reportan tiempos de ciclo exactos por columna como si hubieran sido medidos**, sino únicamente las métricas directamente verificables en GitHub (WIP activo, throughput de PRs y edad desde apertura de Issues).
