# Domain contracts

Last reviewed: **2026-10-07 (America/Sao_Paulo)**. Phase 02.01.
Implementation: `backend/app/schemas.py`; checks: `backend/tests/test_schemas.py`.

## Identity and versioning

Every top-level entity requires `id` and `version`, and emits `schema_version: "1"`.
`schema_version` identifies the JSON contract, while `version` identifies the
particular entity revision. Only contract version 1 is currently accepted.
Versions are opaque non-whitespace strings, not automatically generated SemVer:
callers may supply release labels or content digests when their provenance is known.
IDs permit ASCII letters, digits, dots, underscores, colons, slashes and hyphens,
starting with a letter or digit. IDs and versions are limited to 200 characters.
IDs are logical references, not filesystem paths or commands.

All models forbid extra fields and field reassignment. Required text must contain
at least one non-whitespace character. These contracts use the installed Pydantic
2.13.5; see [Pydantic models](https://docs.pydantic.dev/latest/concepts/models/)
for validation, serialization and schema generation APIs.

## Entities

| Schema | Required fields beyond identity | Optional/default fields |
|---|---|---|
| `Provider` | `name`, `execution_type` | `availability: unknown`, capabilities with unknown values |
| `Model` | `name`, versioned `provider` reference | capabilities with unknown values |
| `Skill` | `name`, `description` | None |
| `Evaluation` | `name`, `description`, `prompt` | None |
| `Run` | versioned `provider`, `model`, `evaluation` references; `execution_type`, `variant`, timezone-aware `created_at` | `status: pending`; nullable `skill`, `started_at`, `finished_at`, `usage` |

`EntityRef` contains required `id` and `version`. References preserve the selected
revision rather than resolving to a mutable latest version. Existence, uniqueness
and cross-reference consistency (for example, model/provider association) require
the future registry; these schemas alone do not check them.

`execution_type` is `cli_agent`, `api_model` or `local_model`. It describes the
execution category, not whether tools, authentication or a provider are available.
Provider availability is `unknown`, `available` or `unavailable`. Capability fields
`tools`, `streaming` and `usage` are strict booleans or null: null means unknown.
No default claims availability or compatibility. Model capabilities are explicit
per-model observations, not automatically inherited from a provider.

## Run semantics

A `Run` represents one evaluation arm. Its `version` is the caller-assigned run
record revision, separate from `schema_version`. A paired experiment/grouping
contract, scoring and persisted state transitions remain future work.

- `baseline` requires a null skill; `with_skill` requires a versioned skill reference.
- `pending` has no start/end timestamps.
- `running` requires a start timestamp and no finish timestamp.
- `completed`, `failed` and `cancelled` require a finish timestamp.
- `completed` also requires a start timestamp. A preflight failure or cancellation
  before launch may have no start timestamp.
- Start cannot precede creation; finish cannot precede start (or creation if no start).
  All supplied timestamps must have a timezone.
- `completed` records execution status only. It does not assert passed checks,
  accessibility, manual review or a quality score.
- Unknown usage is null. `TokenUsage` also preserves null independently for
  `input_tokens`, `cached_input_tokens` and `output_tokens`. Known counts must be
  nonnegative integers; booleans and numeric strings are rejected. Cached-token
  inclusion semantics are provider-specific; no total or cost is inferred.

For example, this synthetic pending baseline can be passed to
`Run.model_validate(...)`; it is not benchmark evidence:

```json
{
  "schema_version": "1",
  "id": "example-run",
  "version": "1",
  "provider": {"id": "example-cli", "version": "adapter-1"},
  "model": {"id": "example-model", "version": "snapshot-1"},
  "evaluation": {"id": "example-eval", "version": "revision-1"},
  "execution_type": "cli_agent",
  "variant": "baseline",
  "created_at": "2026-10-07T12:00:00Z"
}
```

## Boundaries and migration

This change adds contracts only: no file loader, discovery endpoint, database,
provider execution or migration is implemented. Credential fields and arbitrary
command/config dictionaries are not part of the contracts. Validation errors
hide inputs in their string representation; callers must still avoid logging raw
payloads or `ValidationError.errors()` with input values included.

The existing skill frontmatter and EVAL-001 Markdown do not declare explicit
entity versions. Their metadata/version provenance must be addressed in 02.02;
this task neither rewrites them nor invents a verified revision. The experimental
EVAL-001 manifest uses paired arms and different status names, so it is not a
serialized `Run`. Mapping/importing that format needs an explicit future adapter.

Schema tests here validate the new contract. The combined registry fixture and
loader tests in 02.04 remain pending until the registry exists.

## Verification

On 2026-10-07 (America/Sao_Paulo), with Python 3.14.7:

```bash
UV_CACHE_DIR=/private/tmp/skillforge-uv-cache uv run --project backend --locked --offline pytest -c backend/pyproject.toml backend/tests -q -W error
```

Exit 0: **59 tests and 17 subtests passed**, no warnings. New cases cover all five
JSON round trips and JSON Schema generation, explicit identity/version fields,
unsupported schema versions, forbidden extras, null/zero distinction, strict token
counts, versioned references and run/timestamp invariants. Existing endpoint,
settings, CORS and logging tests remain passing. No provider calls were made.
