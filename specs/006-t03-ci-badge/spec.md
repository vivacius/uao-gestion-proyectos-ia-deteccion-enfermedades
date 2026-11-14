# Especificación Técnica (Spec Kit): T-03 Badge Real de CI en README

**Feature Branch:** `feature/t03-ci-badge`  
**Actividad Asociada:** T-03 (Badges veraces)  
**Responsable:** Santiago Correa Campaña (`@vivacius`)  
**Revisor Asignado:** Jhonatan Andrés Tapia Córdoba (`@JhonatanTC99`)  
**Fecha:** 2026-11-12

## Propósito y Escenarios de Aceptación
- **AC-BDG-01:** **Dado** que el workflow `Quality Gate CI (M3)` (`.github/workflows/ci.yml`) pasó en verde en `develop` (Run `#43361515853`), **cuando** se actualiza `README.md`, **entonces** se incorpora el badge oficial de GitHub Actions apuntando a `branch=develop` y se retira el aviso de CI pendiente.
