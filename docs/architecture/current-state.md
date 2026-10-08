# SkillForge — current-state audit

Last reviewed: **2026-10-07 (America/Sao_Paulo)**. Scope: phase 00, documentation and safe local checks only. Git HEAD: `5f571a8`. No application code, dependencies or benchmark results were changed.

## Baseline inventory (00.01)

The repository is a single Next.js application at the root, not the monorepo illustrated in README. Inventory commands: `rg --files`, `git ls-files`, `git status --short`, root directory listing, and `find .github docs packages tests skills evals -type d`. Empty directories were checked separately; their presence does not establish implementation.

```text
app/                         page.tsx, layout.tsx, globals.css, favicon.ico
public/                      file.svg, globe.svg, next.svg, vercel.svg, window.svg
package.json                 dev, build, start, lint scripts
package-lock.json            npm lockfile, lockfileVersion 3
next.config.ts               cacheComponents, partialPrefetching, Tailwind Turbopack rule
eslint.config.mjs             Next core-web-vitals and TypeScript configurations
tsconfig.json                strict, noEmit, bundler resolution, @/* root alias
AGENTS.md                    Next local-guide rule and mandatory plan tracking
README.md, LICENSE           target vision; MIT, copyright 2026 Vitor Prampolin
plan.md, plans/00–08          progress tracking and detailed phase checklists
skills/nextjs-component/      SKILL.md and three reference documents
scripts/                     run-eval-001.py, run-eval-001.sh; two empty TS placeholders
evals/datasets/EVAL-001.md    UserCard task, paired protocol and manual rubric
evals/results/               .gitkeep and ignored local preparation artifacts
docs/, packages/, tests/,
.github/workflows/           empty scaffolding before this audit
CONTRIBUTING.md,
CODE_OF_CONDUCT.md           zero-byte placeholders
AGENTS-plan-section.md,
install-agent-plan.sh,
skillforge-plan-pack.zip     planning-package support artifacts, not application features
```

Additional empty scaffolding: `packages/{configs,skill-runner}`, `tests/{integration,e2e}`, `evals/{rubrics,baselines}`, `skills/{nextjs-form,nextjs-layout,nextjs-datatable}`, and `skills/nextjs-component/{scripts,assets/templates}`. Generated/local directories `.next`, `node_modules`, and `next-env.d.ts` exist; they are not a clean-clone verification.

Installed versions read from local package metadata: Next 16.4.0; React and React DOM 19.3.0; TypeScript 5.9.3; ESLint 9.39.5; Tailwind CSS and @tailwindcss/turbopack 4.3.3. Runtime commands returned Node v24.14.0, npm 11.9.0 and Python 3.14.7. The first version probe failed on the unexported `@tailwindcss/turbopack/package.json` subpath (exit 1); reading that JSON directly succeeded (exit 0). No installation was performed.

Configured commands: `npm run dev` → `next dev`; `npm run build` → `next build`; `npm run start` → `next start`; `npm run lint` → `eslint`. There are no package scripts for typecheck, test, evaluation or skill validation. The installed TypeScript binary can be used directly.

Initial `git status --short` (before audit edits):

```text
 M .gitignore
 M AGENTS.md
?? AGENTS-plan-section.md
?? CODE_OF_CONDUCT.md
?? CONTRIBUTING.md
?? evals/
?? install-agent-plan.sh
?? plan.md
?? plans/
?? scripts/
?? skillforge-plan-pack.zip
?? skills/
```

These pre-existing changes were preserved. `.gitignore` excludes evaluation outputs except `.gitkeep`, so ignored preparations do not appear in a normal Git inventory and will not accompany a clean clone.

## Implemented artifacts and limits (00.02)

| Area | Observed evidence | Assessment |
|---|---|---|
| Frontend | `app/page.tsx` is the Next welcome page; layout uses Geist fonts and Create Next App metadata; CSS defines Tailwind/theme colors | Framework scaffold exists; no SkillForge dashboard or discovery screens |
| Instructions | `AGENTS.md` includes installed Next documentation rule and plan workflow | Repository instructions exist; no instruction files overwritten |
| Skill | `skills/nextjs-component/SKILL.md` has name/description and links to architecture, shadcn and accessibility references | One authored skill; metadata/reference structural checks pass; no effectiveness claim |
| Dataset | `evals/datasets/EVAL-001.md` requests UserCard and a demo, paired baseline/skill protocol, six manual 0–2 criteria | Dataset exists; README calls EVAL-001 a loading button, so README is stale here |
| Specific runner | `scripts/run-eval-001.py` plus shell wrapper implement prepare/run modes, fixture copies, hashes, Codex invocation, timeout, event parsing and type/lint collection | Inspected prototype, not a verified general provider/orchestrator service |
| Generic tooling | `scripts/run-evals.ts`, `scripts/validate-skills.ts` are zero bytes | Not implemented |
| Backend and data | No backend package, FastAPI endpoints, domain registry, SQLite persistence or API client found | Phases 01–02 not implemented |
| Providers/scoring | Runner hard-codes Codex CLI 0.161.0 and writes a mutable manifest; rubric remains manual | Partial precursor to phases 03–04; no interchangeable adapter, cancellation, immutable manifest, automated scoring or failure test suite |
| Containers/API models/CI | No Docker/Compose files, API/local model adapters or workflow files found | Phases 06–07 and CI not implemented |
| Release documentation | MIT LICENSE has content; contributor and conduct files are empty | Partial assets only; phase 08 acceptance not verified |

The runner preserves HOME, creates fresh child Codex state and uses an allowlisted environment; its own documentation acknowledges that workspace-write is not a filesystem read jail. These are inspected controls, not a new isolation/security certification. Static review also shows missing checker records use `not_configured_or_unavailable`, while the aggregate failure predicate defaults a missing exit code to zero; do not equate an arm's completion status with every check having passed. No fix was made in this audit.

### Existing EVAL-001 evidence

Both local manifests were parsed directly:

- `evals/results/EVAL-001/20261007T234914Z-uq4dnbcd/manifest.json`
- `evals/results/EVAL-001/20261007T235326Z-3x5q56j2/manifest.json`

Both report `status: prepared`, arms `baseline` and `with-skill` as `not_run`, and `usage: null`. Their dependency-lock hashes match the current `package-lock.json` (computed with Python SHA-256). Each directory contains prompt, supplied skill text, fixture hashes, isolation audit, CLI version and per-arm command arrays. No events, generated output or scored benchmark was found in the results inventory.

`evals/results/EVAL-001/preparation/isolation-check.log` records an earlier parity check as PASS. That is historical evidence, not a parity check rerun in this audit. The results README also records a prior unavailable PyYAML validator; that validator was not invoked here. Neither `--prepare` nor `--run` was executed in this audit. No model/provider compatibility, token consumption, costs or quality improvement has been established.

## Verification performed (00.03)

All current checks below ran locally on the existing working tree, with no dependency installation or paid model calls.

| Exact command / procedure | Exit/result | Limits |
|---|---|---|
| `npm run lint` | 0, no diagnostics | Current configured ESLint scope only |
| `./node_modules/.bin/tsc --noEmit --incremental false` | 0, no diagnostics | Existing generated `.next/types` and `next-env.d.ts` are present; not a clean checkout build |
| `bash -n scripts/run-eval-001.sh` | 0 | Shell syntax only |
| Python: `ast.parse(Path('scripts/run-eval-001.py').read_text())` | 0, PASS | Syntax only; does not execute runner |
| Python assertions on skill opening frontmatter, name, description and each relative reference target | 0, PASS | Structural check, not full Agent Skills schema validation |
| Python JSON parsing of both manifests and SHA-256 comparison of lockfile | 0, both prepared/not_run/null and matching lock | Existing local preparation only |
| `git diff --check` | 0 | Tracked changes only; new documentation checked separately after writing |
| Test command | not-configured | No test script, test files or configured test framework found |

Build, development server, browser behavior, accessibility, clean installation, provider authentication and runtime benchmark execution were not verified. Lint/typecheck do not prove those behaviors. The missing test suite does not prevent completion of inventory task 00.03, whose acceptance explicitly includes not-configured outcomes.

## Existing decisions recorded (00.04)

[0001 — Local-first architecture](../decisions/0001-local-first-architecture.md) records the already stated decisions in `plan.md`: root Next.js application, Python/FastAPI orchestration, SQLite metadata with JSONL and immutable manifests as the target, and a host executor for authenticated CLIs. These are architectural direction, not implemented services.

Phase 00 is complete as an audit. Phases 01–08 remain not-started against their acceptance criteria; existing precursor artifacts are catalogued above. The smallest next eligible implementation task is **01.01**, creating the backend package and documenting Python dependencies/version. No MVP success criterion is yet verified.
