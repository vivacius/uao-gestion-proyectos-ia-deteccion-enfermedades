# Especificación Técnica (Spec Kit): SPEC-024 HU-05 Endpoint GET /health y Diagnóstico de Disponibilidad del Modelo

**Identificador:** `SPEC-024`  
**Feature Branch:** `feature/modelo-enfermedades-plantas`  
**Historia / Issue Asociado:** HU-05 (Issue [#8](https://github.com/vivacius/uao-gestion-proyectos-ia-deteccion-enfermedades/issues/8) · 3 SP)  
**Responsable:** Jhonatan Andrés Tapia Córdoba (`@JhonatanTC99`)  
**Revisor Asignado:** Santiago Correa Campaña (`@vivacius`)  
**Fecha:** 2026-11-11  
**Estado:** Completado y verificado en `develop`

---

## 1. Propósito y Alcance
Implementar en `api/main.py` el endpoint `GET /health` que permite a clientes (interfaz web, app Tkinter, Docker healthcheck y balanceadores) verificar si el servicio está activo y si el modelo DINOv2-small se encuentra correctamente cargado en CPU (`status='ok'`) o en estado degradado (`status='degraded'`).

## 2. Escenarios de Aceptación (Gherkin)

### AC24.1 — Respuesta saludable con modelo en CPU
- **Dado** el modelo DINOv2-small cargado correctamente en memoria,
- **Cuando** se realiza una petición `GET /health`,
- **Entonces** retorna HTTP 200 con `status='ok'`, `model_available=True`, `architecture='Dinov2ForImageClassification'`, `device='cpu'` y `num_classes=38`.

### AC24.2 — Diagnóstico degradado sin caída del endpoint
- **Dado** una ausencia o fallo de carga de los pesos del modelo (`ModelLoadError`),
- **Cuando** se consulta `GET /health`,
- **Entonces** retorna HTTP 200 con `status='degraded'`, `model_available=False` y el detalle diagnóstico en `detail`.
