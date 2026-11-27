# Plan Técnico (Retrospectivo): Manual Operativo de Despliegue VPS, TLS y Reversión (SPEC-058)

- **Estado:** Implementado y verificado en PR #45, PR #60 · Issue #49, #51.
- **Artefactos cubiertos:** `docs/deployment-m4.md`.
- **Síntesis técnica:** Documenta aprovisionamiento Ubuntu, firewall UFW (22/80/443), emisión Certbot, verificación E2E y procedimiento de rollback por IMAGE_TAG SHA.
- **Validación:** Confirmada mediante revisión de pares y checks de CI en `develop`.
