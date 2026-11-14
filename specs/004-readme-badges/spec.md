# Especificación Técnica (Spec Kit): T-01 y T-03 Actualización de README y Badges Veraces

**Feature Branch:** `feature/readme-badges-t01`  
**Actividades Asociadas:** T-01 (README principal) y T-03 (Badges veraces)  
**Responsable:** Santiago Correa Campaña (`@vivacius`)  
**Revisor Asignado:** Jhonatan Andrés Tapia Córdoba (`@JhonatanTC99`)  
**Fecha:** 2026-11-12

---

## 1. Propósito y Alcance
Alinear `README.md` con las decisiones vigentes del Módulo 3 (D-01: retiro de Streamlit, delimitación M3 vs. M4 para HU-08, arquitectura por capas, comandos reales con `uv` y `pytest`) y publicar únicamente *badges* respaldados por evidencia real del repositorio.

## 2. Escenarios de Aceptación (Gherkin)
- **AC-RM-01:** **Dado** el retiro obligatorio de Streamlit (D-01), **cuando** se consulta `README.md`, **entonces** no contiene instrucciones de `streamlit run` como entregable vigente y documenta el frontend desacoplado sin Streamlit en curso bajo HU-06.
- **AC-RM-02:** **Dado** el requisito de veracidad (T-03), **cuando** se revisan los *badges* de `README.md`, **entonces** reflejan únicamente métricas comprobadas (Python 3.13, `uv`, Ruff, pytest, FastAPI, licencia del modelo) sin incluir badge falso de CI en verde mientras el workflow no haya pasado en `develop`.
- **AC-RM-03:** **Dado** el alcance M3 vs. M4, **cuando** se consulta la sección de Docker/Wheel, **entonces** se indica explícitamente que HU-08 (#11) está diferida a M4.
