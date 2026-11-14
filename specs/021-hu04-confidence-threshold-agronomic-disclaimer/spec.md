# Especificación Técnica (Spec Kit): SPEC-021 HU-04 Umbral de Confianza (tau=0.60) y Descargo de Responsabilidad Agronómica

**Identificador:** `SPEC-021`  
**Feature Branch:** `feature/modelo-enfermedades-plantas`  
**Historia / Issue Asociado:** HU-04 (Issue [#7](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/7) · 2 SP)  
**Responsable:** John Restrepo Aparicio (`@JohnRestrepo-coder`)  
**Revisor Asignado:** Jhonatan Andrés Tapia Córdoba (`@JhonatanTC99`)  
**Fecha:** 2026-11-11  
**Estado:** Completado y verificado en `develop`

---

## 1. Propósito y Alcance
Incorporar en la lógica de postprocesamiento y presentación el criterio de incertidumbre agronómica basado en el umbral $\tau = 0.60$ (60% de confianza) para alertar al usuario ante predicciones dudosas o imágenes fuera de distribución, e incluir obligatoriamente en toda respuesta el descargo de responsabilidad agronómica (`AGRONOMIC_DISCLAIMER`).

## 2. Escenarios de Aceptación (Gherkin)

### AC21.1 — Inclusión obligatoria del descargo agronómico
- **Dado** cualquier resultado generado por `process_logits()` y retornado por `POST /predict`,
- **Cuando** se serializa la respuesta,
- **Entonces** el campo `disclaimer` incluye el aviso formal indicando que la predicción es orientativa y no sustituye un diagnóstico fitopatológico profesional.

### AC21.2 — Alerta preventiva por confianza inferior a tau=0.60
- **Dado** una predicción cuya confianza principal es $< 0.60$ ($< 60\%$),
- **Cuando** se visualiza en las interfaces de usuario (Tkinter y Web) o se evalúa en el benchmark,
- **Entonces** se activa la advertencia visual de baja confianza recomendando tomar otra fotografía o consultar a un ingeniero agrónomo.
