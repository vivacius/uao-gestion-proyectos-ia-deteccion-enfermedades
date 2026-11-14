# Especificación Técnica (Spec Kit): SPEC-028 HU-06 Interfaz Gráfica Nativa de Escritorio en Tkinter para Técnicos de Campo

**Identificador:** `SPEC-028`  
**Feature Branch:** `feature/interfaz-escritorio-tkinter`  
**Historia / Issue Asociado:** HU-06 (Issue [#9](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/9) · 3 SP · PR [#16](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/pull/16))  
**Responsable:** John Restrepo Aparicio (`@JohnRestrepo-coder`)  
**Revisor Asignado:** Jhonatan Andrés Tapia Córdoba (`@JhonatanTC99`)  
**Fecha:** 2026-11-11  
**Estado:** Completado y verificado en `develop`

---

## 1. Propósito y Alcance
Desarrollar en `ui/desktop_app.py` (`PlantDiseaseDesktopApp`) una aplicación de escritorio nativa en español basada en **Tkinter** y `PIL.ImageTk` que permita a técnicos agrícolas seleccionar fotografías foliares desde su equipo, previsualizar la hoja, consultar el estado del backend FastAPI en hilos secundarios (`threading.Thread`) sin congelar la ventana, visualizar el Top-3 con barras de progreso y recibir alertas ante confianza $< 60\%$.

## 2. Escenarios de Aceptación (Gherkin)

### AC28.1 — Ejecución asíncrona en hilo secundario sin bloqueo de GUI
- **Dado** el usuario selecciona una imagen y presiona «Analizar Hoja» en la ventana Tkinter,
- **Cuando** se ejecuta la petición HTTP hacia FastAPI,
- **Entonces** la petición corre en un `threading.Thread(daemon=True)` manteniendo la interfaz fluida y actualizando los widgets mediante `root.after()`.

### AC28.2 — Visualización completa de diagnóstico, Top-3 y alerta de incertidumbre
- **Dado** una respuesta exitosa de `POST /predict`,
- **Cuando** se renderiza en `PlantDiseaseDesktopApp`,
- **Entonces** muestra planta, condición, estado (`Sana`/`Enferma`), confianza, latencia en ms, barras Top-3, alerta si `confidence < 0.60` y descargo agronómico.
