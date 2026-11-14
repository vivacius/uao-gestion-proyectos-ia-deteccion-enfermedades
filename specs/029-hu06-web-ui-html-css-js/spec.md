# Especificación Técnica (Spec Kit): SPEC-029 HU-06 Interfaz Web Desacoplada AgroScan AI en HTML5, CSS3 y JavaScript Vanilla

**Identificador:** `SPEC-029`  
**Feature Branch:** `feature/hu-06-interfaz-web`  
**Historia / Issue Asociado:** HU-06 (Issue [#9](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/9) · 3 SP · PR [#22](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/pull/22))  
**Responsable:** John Restrepo Aparicio (`@JohnRestrepo-coder`)  
**Revisor Asignado:** Jhonatan Andrés Tapia Córdoba (`@JhonatanTC99`)  
**Fecha:** 2026-11-12  
**Estado:** Completado y verificado en `develop`

---

## 1. Propósito y Alcance
Implementar en `ui/web/static/` (`index.html`, `styles.css`, `app.js`) la interfaz web moderna y responsiva **AgroScan AI** sin depender de Streamlit, permitiendo arrastrar y soltar fotografías foliares (drag & drop), validar formato y tamaño en el cliente, invocar `POST /predict` vía `fetch`, renderizar el Top-3 probabilístico, mostrar alertas para $\tau < 0.60$ y mantener un historial local en `localStorage`.

## 2. Escenarios de Aceptación (Gherkin)

### AC29.1 — Interfaz web pura sin acoplamiento con Python ni Streamlit
- **Dado** los activos estáticos en `ui/web/static/`,
- **Cuando** se cargan en cualquier navegador moderno,
- **Entonces** operan mediante HTML5 semántico, CSS3 y JavaScript Vanilla consumiendo la API REST vía `fetch`.

### AC29.2 — Visualización de resultados, alerta de umbral e historial local
- **Dado** el resultado devuelto por `POST /predict`,
- **Cuando** es procesado por `ui/web/static/app.js`,
- **Entonces** renderiza el diagnóstico en español, el desglose Top-3, la alerta preventiva cuando la confianza es $< 60\%$ y guarda el registro en `localStorage`.
