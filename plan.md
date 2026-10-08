# SkillForge — Implementation Plan

> Status: **in-progress** · Strategy: **local-first** · License: **MIT**
>
> This file is the **single source of truth for project progress**. The README describes the vision; this plan tracks what is actually implemented and verified. Do not mark a task complete solely because a file exists or an agent claimed success.

## Operating rules

1. At the **start** of each implementation task, read `plan.md`, the relevant `plans/NN-*.md`, and `AGENTS.md`. Check Git status and inspect affected files.
2. Select the **smallest unchecked item** whose dependencies are satisfied. Do not execute an entire phase unless requested.
3. Before edits, briefly state the selected item, impacted files, verification and risks.
4. After edits, run relevant checks; update the matching task checkbox, phase status, `Last reviewed`, and the **Progress log** with a reference to evidence (command and actual result). If checks cannot run, leave task unchecked and document blocker.
5. Update this master status table only after the phase file reflects its actual progress. Never silently skip or reorder prerequisites.
6. Never delete or reset project changes to satisfy this plan. Request explicit approval for destructive changes, paid API runs, installing new global dependencies, or exposure of credentials.
7. The master plan lives at `plan.md`; detailed checklists live at `plans/`. Update both in the same change when progress advances.

## Legend

- `not-started`: no verified work in phase
- `in-progress`: work underway, at least one task started/verified
- `blocked`: cannot proceed without external input or fix
- `done`: all checklist items verified with evidence

## Phase overview

| Phase | Topic | Status | Prerequisite | Detail |
|---|---|---|---|---|
| 00 | Inventory & Baseline | done | None | [plans/00-inventory-baseline.md](plans/00-inventory-baseline.md) |
| 01 | Python Backend Foundation | in-progress | 00 | [plans/01-python-backend-foundation.md](plans/01-python-backend-foundation.md) |
| 02 | Domain Models & Evaluation Registry | not-started | 01 | [plans/02-domain-models-evaluation-registry.md](plans/02-domain-models-evaluation-registry.md) |
| 03 | Local CLI Provider Adapters | not-started | 02 | [plans/03-local-cli-provider-adapters.md](plans/03-local-cli-provider-adapters.md) |
| 04 | Benchmark Orchestrator & Scoring | not-started | 03 | [plans/04-benchmark-orchestrator-scoring.md](plans/04-benchmark-orchestrator-scoring.md) |
| 05 | Next.js Dashboard MVP | not-started | 04 | [plans/05-next.js-dashboard-mvp.md](plans/05-next.js-dashboard-mvp.md) |
| 06 | Docker Local Development | not-started | 05 | [plans/06-docker-local-development.md](plans/06-docker-local-development.md) |
| 07 | API and Local Model Providers | not-started | 04,05 | [plans/07-api-and-local-model-providers.md](plans/07-api-and-local-model-providers.md) |
| 08 | Open Source Release & CI | not-started | 06,07 | [plans/08-open-source-release-ci.md](plans/08-open-source-release-ci.md) |

## Current position

- **Phase 00 audited and complete.** Last reviewed: **2026-10-07 (America/Sao_Paulo)**. See [current-state evidence](docs/architecture/current-state.md). Phase 01 has now started; **01.01 is verified**. Next eligible task: **01.02** (health/info endpoints).
- Verified existing assets: root Next.js scaffold, one authored skill with references, EVAL-001 dataset and a dedicated prototype runner. Two ignored preparation manifests are `prepared`, both arms `not_run`, usage `null`. Generic scripts and contributor documents are empty placeholders.
- Backend package and pinned dependency baseline are implemented; isolated installation, packaging, lock consistency and imports passed on Python 3.14.7. See [backend verification](backend/README.md). HTTP service and tests remain pending.
- During phase 00, lint and TypeScript passed on the local tree; tests were not configured. Dashboard, general adapters, persistence, Docker and CI remain unimplemented. Phases 02–08 remain not-started; precursor artifacts do not complete those phases.
- Do not duplicate installation or claim phase 00 is complete without checking the actual repository.
- Planned architecture: Next.js UI → FastAPI → benchmark orchestrator → CLI/API/local adapters → reports; Docker for reproducible web/API services, host executor for authenticated local CLIs initially.

## Success criteria for the MVP

- [ ] User can discover installed skills and benchmark cases in a browser.
- [ ] User can compare baseline vs skill without writing arbitrary shell commands.
- [ ] At least one local CLI backend produces a traceable, validated run.
- [ ] An unavailable provider or check never turns into a fabricated pass.
- [ ] Docker starts the app services; host-only credentials are not mounted in containers.

## Decisions and change control

- Keep the existing Next.js project at repository root until a migration has documented value.
- Start with SQLite for local run metadata; retain JSONL logs and immutable run manifests.
- A raw API model needs a controlled tool executor to fairly compare with CLI agents; label execution type in every run.
- Use Python/FastAPI for orchestration; never expose arbitrary host command execution to untrusted web clients.
- If project direction changes, update this plan and affected phases before implementing the new direction.

## Progress log

| Date (UTC or with timezone) | Phase / item | Evidence and observation | State |
|---|---|---|---|
| 2026-10-07 | Planning package | Roadmap and phase definitions authored; no repository implementation checked | planning |
| 2026-10-07 (America/Sao_Paulo) | 00.01–00.04 | [Audit](docs/architecture/current-state.md) and [existing decisions](docs/decisions/0001-local-first-architecture.md) recorded. Lint, direct TypeScript, shell syntax and Python structural checks exit 0; tests not configured. No benchmark or new functionality executed | phase 00 done; implementation pending |
| 2026-10-07 (America/Sao_Paulo) | 01.01 | [Backend package and evidence](backend/README.md): pinned Python/dependencies, uv lockfile, isolated sync, sdist/wheel build, dependency/lock checks and imports exit 0; no HTTP endpoints yet | phase 01 in-progress; 01.01 done |
