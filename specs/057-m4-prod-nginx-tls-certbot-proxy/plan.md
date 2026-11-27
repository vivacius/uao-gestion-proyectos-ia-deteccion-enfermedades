# Plan Técnico (Retrospectivo): Proxy Inverso Nginx con TLS/HTTPS y Renovación Certbot (SPEC-057)

- **Estado:** Implementado y verificado en PR #45 · Issue #49.
- **Artefactos cubiertos:** `deploy/nginx.prod.conf.template`.
- **Síntesis técnica:** Enruta tráfico HTTPS (443) hacia el frontend estático y FastAPI con proxy same-origin, redirección HTTP->HTTPS y desafío ACME de Certbot.
- **Validación:** Confirmada mediante revisión de pares y checks de CI en `develop`.
