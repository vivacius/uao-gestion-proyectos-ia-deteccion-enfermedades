# Plan Técnico (Retrospectivo): Job Condicional deploy_vps vía SSH hacia Producción (SPEC-055)

- **Estado:** Implementado y verificado en PR #45 · Issue #51.
- **Artefactos cubiertos:** `.gitlab-ci.yml (etapa deploy)`.
- **Síntesis técnica:** Despliega en la VPS por SSH solo cuando DEPLOY_HOST está definido como variable protegida, haciendo pull por SHA y levantando servicios sin caída.
- **Validación:** Confirmada mediante revisión de pares y checks de CI en `develop`.
