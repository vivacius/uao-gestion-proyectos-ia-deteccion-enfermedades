# Especificación Técnica (Spec Kit): SPEC-032 Decisión Arquitectónica D-01: Retiro Definitivo de Streamlit del Proyecto

**Identificador:** `SPEC-032`  
**Feature Branch:** `chore/remove-streamlit`  
**Historia / Issue Asociado:** HU-06 / HU-08 (PR [#32](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/pull/32))  
**Responsable:** José Isaac Silva Calderón (`@josesilvacalderon111`)  
**Revisor Asignado:** Jhonatan Andrés Tapia Córdoba (`@JhonatanTC99`)  
**Fecha:** 2026-11-13  
**Estado:** Completado y verificado en `develop`

---

## 1. Propósito y Alcance
Materializar la decisión arquitectónica **D-01** del Grupo 2 eliminando por completo `ui/streamlit_app.py` y la dependencia `streamlit` de `pyproject.toml` y `uv.lock`, reduciendo la superficie de dependencias de la imagen Docker CPU y consolidando exclusivamente el frontend web desacoplado (`ui/web/static/`) y la aplicación nativa de escritorio en Tkinter (`ui/desktop_app.py`).

## 2. Escenarios de Aceptación (Gherkin)

### AC32.1 — Ausencia total de Streamlit en código y dependencias
- **Dado** el árbol del repositorio, `pyproject.toml` y `uv.lock`,
- **Cuando** se auditan las dependencias y módulos en `ui/`,
- **Entonces** no existe `ui/streamlit_app.py` ni el paquete `streamlit` en el entorno virtual.

### AC32.2 — Reducción de peso y complejidad del empaquetado
- **Dado** la construcción del paquete Wheel y de la imagen Docker,
- **Cuando** se ejecuta `uv sync --frozen --no-dev`,
- **Entonces** no se descargan dependencias transitivas de Streamlit (`altair`, `pydeck`, `tornado`), agilizando el build en CPU.
