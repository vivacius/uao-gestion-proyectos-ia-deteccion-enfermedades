# Especificación Técnica (Spec Kit): SPEC-009 Elaboración de Model Card Fitosanitaria y Evidencia Documental

**Feature Branch:** `feature/m3-model-card`  
**Issue Asociado:** [#29 — [M3-DOC] Elaboración de Model Card Fitosanitaria y Evidencia Documental](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/29)  
**Responsable:** John Restrepo Aparicio (`@JohnRestrepo-coder`)  
**Revisores Asignados:** Jhonatan Andrés Tapia Córdoba (`@JhonatanTC99`), Santiago Correa Campaña (`@vivacius`)  
**Fecha:** 2026-11-13  
**Base:** `develop` (`734fbdf`)

---

## 1. Propósito y Alcance

Formalizar la documentación técnica, ética, operativa y de gobernanza del modelo clasificador fitosanitario mediante la elaboración de una **Model Card** rigurosa y estandarizada en `docs/model-card.md`, conforme al estándar fundacional de Mitchell et al. (2019) (*Model Cards for Model Reporting*) y las directrices del Anuncio 007 de la asignatura.

El documento consolida la ficha técnica de la arquitectura `rodynaemad/plant-disease-dinov2-small` (`Dinov2ForImageClassification`), delimita el alcance de cribado preliminar en campo, documenta con estricta honestidad científica las métricas reales observadas en el repositorio (benchmarks de CPU, HTTP y latencias de MLflow), analiza los factores de sesgo e introduce la trazabilidad completa de licenciamiento (código MIT, pesos CC BY-SA 4.0, arquitectura Apache 2.0 y dataset CC BY-SA 3.0).

> **Restricción estricta de no modificación:** Esta especificación no altera código ejecutable en `src/`, `api/`, `ui/`, `Dockerfile`, `pyproject.toml`, `uv.lock` ni las especificaciones previas `specs/001` a `specs/008`.

---

## 2. Escenarios de Aceptación (Gherkin)

### AC-MC-01 — Ficha Técnica y Especificación Arquitectónica del Modelo
- **Dado** el modelo adaptado servido bajo arquitectura Model-as-a-Service (MaaS) en el repositorio,
- **Cuando** se documenta su ficha técnica en `docs/model-card.md`,
- **Entonces** se detalla el identificador oficial `rodynaemad/plant-disease-dinov2-small` (`Dinov2ForImageClassification`), el formato de pesos `SafeTensors` (`model.safetensors`, ~88 MB), la inferencia local en CPU, el contrato tensorial de entrada $[1, 3, 224, 224]$ normalizado y el catálogo completo de las 38 clases botánicas distribuidas en 14 cultivos (`src/labels.py`).

### AC-MC-02 — Uso Previsto, Usuarios Objetivo y Alcance Operativo
- **Dado** el sistema de apoyo fitosanitario para campo,
- **Cuando** se define su espectro operacional y fronteras éticas,
- **Entonces** se estipula su propósito exclusivo como herramienta orientativa de cribado y tamizaje preliminar para agrónomos y agricultores, prohibiendo explícitamente su uso como diagnóstico fitosanitario definitivo, toma de decisiones destructivas o prescripción/aplicación química automatizada sin supervisión profesional humana.

### AC-MC-03 — Métricas Empíricas Reales, Sesgos y Honestidad Metodológica
- **Dado** el registro empírico consolidado en `docs/qa-e2e-benchmarks.md` y los 3 runs de MLflow (`SPEC-007`),
- **Cuando** se reporta el desempeño cuantitativo del sistema,
- **Entonces** se documentan únicamente los datos reales observados en CPU: latencia de inferencia pura (media 66.10 ms, p95 77.33 ms), latencia HTTP E2E secuencial (p95 81.39 ms), latencia HTTP concurrente con 4 workers (p95 314.60 ms), uso de RAM RSS (459.64 MB) y umbral de incertidumbre $\tau = 0.60$.
- **Y** se declara explícitamente que los benchmarks y runs de MLflow se ejecutaron sobre imágenes sintéticas deterministas sin ground truth, por lo que **no se reporta ni inventa accuracy ni Macro F1 clínico**.
- **Y** se analizan detalladamente cuatro factores de sesgo: iluminación/sombras, ángulo/enfoque, síntomas visuales cruzados y la brecha de dominio (*out-of-distribution*) entre laboratorio y campo real.

### AC-MC-04 — Trazabilidad Ética, Licenciamiento y Atribuciones
- **Dado** el marco legal y de atribuciones en `LICENSE`,
- **Cuando** se documenta la cadena de derechos y consideraciones éticas,
- **Entonces** se articulan la licencia MIT del código del repositorio, la licencia CC BY-SA 4.0 de los pesos adaptados, la licencia Apache 2.0 de la arquitectura base `dinov2-small` de Meta AI y la licencia CC BY-SA 3.0 del dataset PlantVillage, garantizando gobernanza de datos y privacidad en memoria volátil sin persistencia de imágenes.
