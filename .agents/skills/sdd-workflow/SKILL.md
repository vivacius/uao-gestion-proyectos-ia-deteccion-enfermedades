---
name: sdd-workflow
description: >-
  Execute prospective Spec-Driven Development (SDD) in Spec Kit before any code,
  config, or governance change, preserving historical specs and honest
  traceability.
---

# SDD Workflow (Spec Kit)

Use this skill before creating or modifying code, infrastructure, or normative documents.

## Procedure

1. **Follow the end-to-end flow:** `Historia → Issue/Project → SPEC prospectiva → tareas → implementación → pruebas → PR revisada → merge → Done`.
   - Enforce GitHub Projects Kanban columns and WIP limits: `Backlog`, `In Progress` (max team members = 4), `In Review` (max 2), `Done`, tracking **WIP**, **throughput**, **work item age**, and **cycle time**.
2. **Verify prospective order:** Create `specs/NNN-<slug>/` (`spec.md`, `plan.md`, `tasks.md`) **before** implementing changes. Never backdate or claim prospective validity for retrospective specs.
3. **Check next ID:** Inspect `specs/` to pick the next sequential `NNN` without altering `specs/001..040/` (historical) or prior approved specs.
4. **Link all traceability artifacts:**
   - Reference matrix IDs (`M1..M4`, `TOOL-XX`) from [docs/academic-compliance-matrix.md](../../../docs/academic-compliance-matrix.md).
   - Write verifiable **Given-When-Then** acceptance criteria.
   - Link the associated GitHub Issue and target PR using the official [.github/PULL_REQUEST_TEMPLATE.md](../../../.github/PULL_REQUEST_TEMPLATE.md) **without modifying or replacing it** (add extra M3/M4 traceability in the PR description body).
5. **Maintain honest status:**
   - Explicitly declare temporal nature: prospective vs retrospective (`specs/010..040/` are documented retrospective records and must never be presented as prior design).
   - Distinguish *implemented*, *verified*, *ready for PR*, and *merged*.
   - Leave incomplete tasks unchecked (`[ ]`) with exact observed blockers instead of marking them done.
5. **Scope control:** Execute one controllable unit at a time and verify protected capabilities are intact before closing.
