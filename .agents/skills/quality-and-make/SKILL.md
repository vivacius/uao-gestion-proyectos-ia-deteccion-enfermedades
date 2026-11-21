---
name: quality-and-make
description: >-
  Run and verify project quality gates, tests, and packaging using the root
  Makefile, uv, Ruff, and pytest AAA without destructive commands or unnecessary
  long suite reruns.
---

# Quality and Make

Use this skill when validating code, documentation, or packaging with [Makefile](../../../Makefile) and `uv` (Python 3.13).

## Procedure

1. **Check tool availability first:** Do not assume `make` or `docker` is installed. Verify `make --version` before invoking `make <target>`; if GNU Make is unavailable (e.g., local Windows), run the equivalent `uv` command from [Makefile](../../../Makefile) directly and document the limitation.
2. **Select the minimum needed check:**
   - **Static lint & format:** `make lint` (`uv run ruff check .`) and `make format-check` (`uv run ruff format --check .`).
   - **Fast mocked unit tests:** `make test-unit` (`uv run pytest tests/unit -v`).
   - **Unit tests + coverage ($\ge 85\%$ on `src/`, `api/`):** `make coverage` (`uv run pytest tests/unit -v --cov=src --cov=api --cov-report=term-missing`).
   - **Integration tests (requires local `model.safetensors`):** `make test-integration` (`uv run pytest tests/integration -v`).
   - **Full suite / CI gate:** `make test` or `make ci`.
3. **Avoid redundant long runs:** For documentation-only changes, do not rerun full `pytest` or Docker builds unless explicitly requested; rely on targeted checks (`git diff`, link/secret checks, or Ruff if code touched).
4. **Enforce AAA & floor:** Keep minimum academic floor of 120 `pytest` AAA tests without reducing existing capabilities (`M1-03`).
5. **Report honestly & forbid destructive commands:**
   - Record exact exit codes, counts (`passed`/`skipped`), and environment blockers (e.g., sandbox `TestClient` limits vs GitHub Actions CI).
   - Never run `pip`, `requirements.txt`, `rm -rf`, `docker system prune`, or commands that alter `.venv/`, `mlflow_tracking.db`, or `mlruns/`.
