---
name: academic-compliance
description: >-
  Verify accumulated M1-M4 academic requirements, precedence rules, forbidden
  technologies, and protected capabilities before planning or implementing any
  task in the repository.
---

# Academic Compliance (M1–M4)

Use this skill at the start of any unit to align scope and decisions with [AGENTS.md](../../../AGENTS.md) and [docs/academic-compliance-matrix.md](../../../docs/academic-compliance-matrix.md) (SSOT).

## Procedure

1. **Locate applicable IDs:** Check [docs/academic-compliance-matrix.md](../../../docs/academic-compliance-matrix.md) § 1 (`M1-01..M4-12`, `TOOL-01..TOOL-09`) and § 2 (10 protected capabilities).
2. **Apply cumulative precedence:**
   - All `M1`–`M4` rules remain active cumulatively.
   - Only when an explicit incompatibility exists between official course rules, apply `M4 > M3 > M2 > M1`.
   - Never override user instructions or approved human decisions.
3. **Classify every item accurately:**
   - `REQUISITO`: Official course obligation.
   - `MATERIAL`: Teaching recommendation or reference resource.
   - `DECISIÓN`: Team architectural or governance agreement.
   - `RESULTADO`: Observed verification output (never invent or extrapolate).
4. **Enforce hard prohibitions:**
   - **No Streamlit** as an evaluable M3/M4 frontend (`M3-02`, `D-04`); UI must consume FastAPI strictly over HTTP.
   - **No `pip` or `requirements.txt`** (`M1-02`); use `uv` with Python 3.13.
   - **No `.ipynb` notebooks**, dead code, or coupling `ui/` to `torch`/`transformers`.
   - **No unverified compliance claims:** Distinguish `VERIFICADO`, `REPORTADO`, `PARCIAL`, and `PENDIENTE`.
5. **Guard protected capabilities:** Before touching `src/`, `api/`, `ui/`, `tests/`, `model.safetensors`, MLflow artifacts, Docker, or CI, verify invariants and required evidence in [docs/academic-compliance-matrix.md § 2](../../../docs/academic-compliance-matrix.md).
