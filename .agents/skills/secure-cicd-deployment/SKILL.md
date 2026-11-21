---
name: secure-cicd-deployment
description: >-
  Plan or verify M4 CI/CD pipelines, Docker CPU builds, Container Registry
  tagging, VPS reverse-proxy HTTPS deployment, and protected secrets while
  preserving M3 application contracts.
---

# Secure CI/CD and Deployment (M4)

Use this skill for M4 pipeline, container, registry, and VPS deployment units (`M4-01..M4-08`, `M4-11` in [docs/academic-compliance-matrix.md](../../../docs/academic-compliance-matrix.md)).

## Procedure

1. **Preserve M3 application invariants:** Keep `src/`, `api/`, `ui/` (no Streamlit), `Dockerfile` (CPU multi-stage, non-root `appuser`, `MODEL_DIR=/app/modelo_plantas`), `docker-compose.yml`, and `deploy/nginx.conf` contracts intact unless explicitly authorized.
2. **Enforce pipeline stages:** Require `lint` (Ruff) → `test` (`pytest` AAA) → `build` (Docker CPU with reproducible `model.safetensors` handling) → `Registry` (immutable SHA/version tags) → `deploy` (VPS).
3. **Harden infrastructure & secrets:**
   - Store all credentials, SSH keys, and registry tokens strictly in protected/masked CI/CD variables or out-of-repo `.env` (`.gitignore`). Never expose secrets or private IPs in code, logs, or docs.
   - Require VPS firewall minimalism (SSH, HTTP/HTTPS) and valid TLS/HTTPS reverse proxy in production.
4. **Verify honestly:**
   - Confirm deployment via `GET /health` returning HTTP `200` and live public URL demonstration.
   - Never claim *zero-downtime* without load/cutover evidence.
   - Never provision VPS, configure GitLab, or deploy without explicit human authorization in the active unit.
