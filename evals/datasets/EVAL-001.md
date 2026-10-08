# EVAL-001: reusable UserCard

## Prompt

<!-- PROMPT_START -->
Implement a reusable, accessible, responsive UserCard in this existing Next.js project.

Export UserCard and its TypeScript props from components/user-card.tsx. Accept a required name and profileHref, optional email, role, avatarUrl, status (active or inactive), and className. Display identity, optional details, text status when supplied, an avatar with a usable missing/broken-image fallback, and a clearly named profile link. Use native semantics and visible keyboard focus. Avoid duplicate IDs or nested interactive controls when several cards appear together.

Use existing styling conventions and installed UI primitives where available. Do not invent shadcn/ui imports if it is absent. Support a 320px viewport, wide layouts, long names/emails, and enlarged text without overflow or clipped controls. Keep the component reusable without data fetching or application-specific state. Choose appropriate server/client boundaries.

Add app/user-card-demo/page.tsx demonstrating a complete user, missing optional fields, a broken avatar, and long content. Do not modify existing application files, package/configuration files, or dependencies. Read the relevant installed Next.js documentation before using framework APIs. Do not install dependencies, access external sources, delegate work, or request unrestricted permissions. Work only in this workspace. Run installed TypeScript and ESLint checks if available and report any checks that could not be performed.

If task-specific instructions are supplied, follow them. Report implementation and validation results without claiming unobserved browser behavior.
<!-- PROMPT_END -->

## Evaluation protocol

Use the exact extracted prompt in both arms, identical fixture snapshots, the same explicitly selected model and reasoning effort, and fresh sessions. The treatment supplies the full nextjs-component skill and references as developer instructions; the baseline supplies none. Native skill discovery is disabled in both arms. This evaluates supplied skill guidance, not automatic skill selection or progressive disclosure.

The runner requires Codex CLI 0.161.0, uses workspace-write with approval policy never, disables web search, ignores user config and rules, and skips host skill discovery. It uses fresh Codex state directories and an allowlisted environment. System/managed configuration causes a preflight stop rather than silently weakening isolation. No AGENTS.md is copied; project instruction loading is disabled in both arms. The existing dependencies are copied, not installed or symlinked to writable project dependencies.

## Rubric (manual, 0–2 each; 12 points maximum)

| Criterion | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Reuse and types | Missing/broken API | Partial props or avoidable coupling | Exported typed contract, optional fields handled, styling extensible |
| Semantics and keyboard | Inaccessible controls | Partial semantics/focus | Named link, logical headings, visible keyboard focus, distinct repeated cards |
| Avatar and status | Broken identity/status | Missing one fallback | Missing and failed images handled, status conveyed in text |
| Responsive layout | Overflow/clipping | Works only for ordinary content | 320px, wide, long content and 200% text checks pass |
| Framework and composition | Invalid imports/boundaries | Unnecessary client scope or duplication | Valid boundaries and reuse of available primitives |
| Verification and scope | Missing output or unrelated edits | Partial checks/evidence | Demo cases, type/lint pass, scoped changes, honest limitations |

Record code evidence and browser observations separately. Unperformed manual checks are pending, not passed. Verify absence of unrelated edits and instruction leakage in logs before scoring. A failed command or incomplete arm invalidates an overall comparison. A single pair is exploratory; repeat with reversed order before making claims. Report input, cached input, and output tokens separately when emitted; missing usage is null, never zero. Do not infer cost or causal improvement from one pair.

## Running

Preparation only (no model calls): `bash scripts/run-eval-001.sh --prepare --model gpt-6-astra`

Execution requires `OPENAI_API_KEY` in the invoking environment (passed as `CODEX_API_KEY` to Codex exec); personal login credentials are not copied.

Execute later: `bash scripts/run-eval-001.sh --run --model gpt-6-astra`

Optional: `--effort low|medium|high` and `--order baseline-first|skill-first`.

Each invocation creates a unique result directory under evals/results/EVAL-001. Temporary workspaces remain available for inspection; their paths are recorded. Credentials are never copied into results. Inspect logs before sharing them.

Isolation controls: [Codex configuration reference](https://developers.openai.com/codex/config-reference). CLI flags and the skip_host_skill_discovery feature were checked locally against 0.161.0.
