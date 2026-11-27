---
name: github-gitlab-operations
description: >-
  Coordinate read and authorized write operations across GitHub (primary repo)
  and GitLab (M4 CI/CD and Registry) using gh, glab, and MCPs without exposing
  secrets or bypassing human review.
---

# GitHub and GitLab Operations

Use this skill when querying or operating remote repositories, Issues, PRs, branches, or pipelines (`TOOL-01..TOOL-07` in [docs/academic-compliance-matrix.md](../../../docs/academic-compliance-matrix.md)).

## Procedure

1. **Respect platform roles:**
   - **GitHub:** Primary repository, Issues, PRs, Kanban, and human peer review (`gh` CLI / GitHub MCP).
   - **GitLab:** M4 CI/CD, Container Registry, and VPS deployment (`glab` CLI / GitLab MCP), subject to approved sync architecture (`TOOL-05`). Never assume GitHub↔GitLab mirroring is configured without evidence.
2. **Distinguish CLI, MCP, and remote state:** Verify authentication and permissions (`gh auth status`, `glab auth status`) before claiming connectivity. Never print, log, or commit tokens/PATs.
3. **Separate read vs write actions:**
   - **Read-only (safe):** `gh pr view`, `gh pr checks`, `gh run view`, `git fetch origin --prune`, `git status`.
   - **Write (requires explicit unit authorization):** `git commit`, `git push`, `gh pr create`, `gh pr merge`, branch deletion, or GitLab registry/pipeline triggers.
4. **Enforce Gitflow & human review:**
   - Never commit/push directly to `main` or `develop`.
   - Never self-approve, force-push, `reset --hard`, `git clean`, or `merge` without peer approval and green CI.
   - Use [.github/PULL_REQUEST_TEMPLATE.md](../../../.github/PULL_REQUEST_TEMPLATE.md) and Conventional Commits.
5. **Safe branch cleanup:** Delete a `feature/*` branch (local/remote) **only** after confirming PR state is `MERGED`, its commits are ancestors of `origin/develop`, and the local working tree has no unintegrated work.
