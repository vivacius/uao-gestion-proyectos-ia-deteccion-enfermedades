# Plan de Implementación (Spec Kit): SPEC-028 HU-06 Interfaz Gráfica Nativa de Escritorio en Tkinter para Técnicos de Campo

**Identificador:** `SPEC-028`  
**Feature Branch:** `feature/interfaz-escritorio-tkinter`  
**Spec Asociada:** [spec.md](./spec.md)

---

## Pasos de Implementación y Verificación

1. Diseñar e implementar `PlantDiseaseDesktopApp` en `ui/desktop_app.py` con paleta visual agronómica.
2. Integrar previsualización de imagen con Pillow (`ImageOps.contain` y `ImageTk.PhotoImage`).
3. Conectar `check_api_health` y `predict_image_via_api` mediante hilos de trabajo y `root.after`.
