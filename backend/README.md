# SkillForge backend

Phase 01.01 introduces an installable Python package; 01.02 adds read-only
health and service-info endpoints. Phase 01.03 adds validated environment
settings, an explicit CORS allowlist and structured logging. Phase 01.04 adds
pytest coverage. See the [local development guide](../docs/guides/local-development.md) for two-terminal startup and shutdown.

## Environment and dependencies

Supported Python line: **3.14** (`>=3.14,<3.15`); local verification uses 3.14.7.
Other Python lines are not yet part of the supported baseline. `.python-version`
selects the minor line; it does not pin an interpreter patch release.

Direct dependencies are FastAPI 0.142.4, Pydantic 2.13.5 and Uvicorn 0.54.0; the build backend is
Hatchling 1.32.4. Versions were checked against the package publishers' PyPI
metadata: [FastAPI](https://pypi.org/project/fastapi/0.142.4/),
[Uvicorn](https://pypi.org/project/uvicorn/0.54.0/) and
[Hatchling](https://pypi.org/project/hatchling/1.32.4/).
`uv.lock` records the resolved runtime dependency graph. Uvicorn's optional
standard extras are omitted until needed.

With Python 3.14 and uv installed, from the repository root:

```bash
cd backend
uv sync --locked
uv run --no-sync python -c "import app, fastapi, uvicorn; print(app.__file__)"
```

Dependencies are installed in `backend/.venv`, not globally. The importable
package is `app`; its ASGI entrypoint is `app.main:app`. No paid model call is involved.

## HTTP contracts (01.02)

From `backend/`, run `uv run --no-sync python -m app`. This supported launcher
binds to `127.0.0.1:8000` and configures safe JSON logging before starting Uvicorn.

| Request | HTTP status | JSON response |
|---|---|---|
| `GET /health` | 200 | `{"status":"ok"}` |
| `GET /api/v1/info` | 200 | `{"name":"skillforge-backend","version":"0.1.0","api_version":"v1"}` |

Health is process liveness only; it does not check database or provider readiness.
Info contains only public metadata. Its `version` comes from the installed
`skillforge-backend` distribution, so it follows package releases; `api_version`
identifies the v1 contract. All fields are required, with string values.
Pydantic response models validate the outputs and expose their schemas in
`/openapi.json`, following the [FastAPI response model documentation](https://fastapi.tiangolo.com/tutorial/response-model/).
The package must be installed using the setup above before launching.
See the [local development guide](../docs/guides/local-development.md) for two-terminal startup and shutdown.

## Verification

Last reviewed: **2026-10-07 (America/Sao_Paulo)**. Verified with uv 0.12.17
and Python 3.14.7 on the current macOS host. Commands ran from repository root;
uv commands used `UV_CACHE_DIR=/private/tmp/skillforge-uv-cache`.

| Command | Actual result |
|---|---|
| `uv sync --project backend --python /opt/homebrew/bin/python3 --no-python-downloads` | Exit 0; resolved and installed 15 packages, including editable backend, in `backend/.venv` |
| `uv build --project backend --offline` | Exit 0; built sdist and wheel in `backend/dist` |
| `uv lock --project backend --check --offline` | Exit 0; lock matches project metadata |
| `uv pip check --python backend/.venv/bin/python` | Exit 0; all 15 installed packages compatible |
| `backend/.venv/bin/python -c 'import app, fastapi, uvicorn; from importlib.metadata import version; print(app.__file__); print(version("skillforge-backend"), fastapi.__version__, uvicorn.__version__)'` | Exit 0; local app package imports, versions 0.1.0 / 0.142.4 / 0.54.0 |
| Python `zipfile` inspection of built wheel | Exit 0; includes `app/__init__.py` and distribution metadata |

The initial sandboxed PyPI lookup failed on DNS; the permitted network retry
succeeded. Dependencies were installed locally, with no global installation.
At 01.01, no HTTP service, runtime endpoint or pytest suite was verified.
Cross-platform compatibility and other Python versions remain unverified.
Next.js source and dependencies remain unchanged.


### Endpoint verification — 01.02

Verified on 2026-10-07 (America/Sao_Paulo), Python 3.14.7:

- `UV_CACHE_DIR=/private/tmp/skillforge-uv-cache uv lock --project backend --offline`
  and `UV_CACHE_DIR=/private/tmp/skillforge-uv-cache uv sync --project backend --locked --offline`:
  exit 0. Pydantic was promoted from transitive to direct dependency at the existing
  locked version; no dependency version changed.
- `backend/.venv/bin/python /private/tmp/skillforge-check-0102.py`: exit 0.
  This temporary verification harness launched Uvicorn on an ephemeral loopback
  port, checked both exact JSON bodies, 200 status and JSON content type, required
  OpenAPI properties and response-model references, and metadata version parity.
  It also checked unknown-route 404 and POST 405 for both endpoints. The server
  was terminated in a finally block. The harness is session-local, not a committed
  regression suite; persistent pytest coverage remains task 01.04.
- The first HTTP attempt was blocked by the sandbox's loopback bind restriction;
  the permitted retry passed. No external provider or credentials were accessed.
- `UV_CACHE_DIR=/private/tmp/skillforge-uv-cache uv build --project backend --offline`: exit 0; updated sdist and wheel built successfully.


## Settings, CORS and logging (01.03)

Settings are read once at application creation from the process environment.
No dotenv file, credential file or provider configuration is read. Changes require
restarting the process. The application factory `create_app(settings)` accepts
explicit settings for checks and future integration.

| Variable | Default | Accepted values |
|---|---|---|
| `SKILLFORGE_CORS_ORIGINS` | `["http://localhost:3000","http://127.0.0.1:3000"]` | JSON array of explicit HTTP(S) origins; `[]` disables cross-origin access |
| `SKILLFORGE_LOG_LEVEL` | `INFO` | `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |
| `SKILLFORGE_PORT` | `8000` | Integer 1–65535; supported launcher always binds to loopback |

Origin entries cannot contain wildcards, credentials, paths, queries, fragments
or whitespace. Invalid configuration stops startup without printing its values.
For example, from `backend/`:

```bash
SKILLFORGE_CORS_ORIGINS='["http://localhost:3000"]' SKILLFORGE_PORT=8001 uv run --no-sync python -m app
```

CORS allows only GET and the middleware's standard safelisted headers, with
credentials disabled. Preflight requests for disallowed origins, methods or
headers return 400. Ordinary requests from disallowed origins receive no
allow-origin header: CORS is a browser policy, not authentication or a network
firewall. Configuration follows the [FastAPI CORS documentation](https://fastapi.tiangolo.com/tutorial/cors/).

The supported `python -m app` launcher replaces root/Uvicorn handlers with JSON
logging and disables Uvicorn access logs. Each request record includes UTC
`timestamp`, `level`, `event`, numeric `status` and `duration_ms`. Other server
records contain only timestamp, level and a generic `server_event`/`server_error`.
No raw messages, traceback text, request paths, queries, headers, bodies or
configuration values are formatted. This deliberately limits diagnostics to
avoid leaking secrets through arbitrary messages and exceptions. INFO request
records are suppressed at WARNING or higher; 5xx records use ERROR.

Direct Uvicorn CLI invocation or third-party handlers can bypass the launcher's
logging policy; use the documented launcher. This policy covers configured
Python logging handlers, not arbitrary print statements or future subprocess
output. Future diagnostics must preserve this data-minimization boundary.

### Verification — 01.03

Last reviewed: **2026-10-07 (America/Sao_Paulo)**.

- `backend/.venv/bin/python -m unittest discover -s backend/tests -v`: exit 0,
  four tests passed. Covers defaults/overrides, invalid settings, wildcard and
  credential-bearing origin rejection, allowed/denied/empty CORS origins,
  preflight method/header restrictions, JSON logging for 200/404/500, and
  exclusion of sentinel secrets in paths, queries, headers, bodies and exceptions.
  These are standard-library regression checks; the planned pytest setup in
  01.04 remains unchecked.
- `backend/.venv/bin/python /private/tmp/skillforge-check-0103.py`: exit 0.
  Session-local harness launched `python -m app` on a temporary loopback port,
  verified both existing JSON contracts, OpenAPI schemas, 404/405 responses,
  parsed server output as JSON and confirmed a query sentinel was absent.
  The server was stopped after verification. No model calls were made.
- Subprocess startup with a credential-bearing origin: nonzero exit as expected; sentinel value absent from stdout/stderr.
- `UV_CACHE_DIR=/private/tmp/skillforge-uv-cache uv build --project backend --offline`: exit 0, sdist and wheel built. `git diff --check`: exit 0.


## Running tests (01.04)

From the repository root:

```bash
uv sync --project backend --locked
uv run --project backend --locked --offline pytest -c backend/pyproject.toml backend/tests -q -W error
```

Or from `backend/`, after syncing: `uv run --locked --offline pytest -q -W error`.
The `dev` dependency group pins pytest 9.1.1 and httpx2 2.13.1, with transitive
versions recorded in `uv.lock`. `uv sync` includes this group by default; runtime-only
installations can use `uv sync --locked --no-dev`. No global installation is required.

The installed Starlette TestClient prefers httpx2. The initial httpx-based run
passed but emitted a deprecation warning; switching to httpx2 removed it.
The final suite passes with warnings treated as errors.

Coverage includes exact health/info JSON contracts, content types, installed
version parity, required OpenAPI response fields, 404/405 behavior, environment
settings reaching CORS, and invalid settings preventing application creation.
Pytest also collects the four existing unittest safety cases for settings, CORS
and JSON logging. An autouse fixture clears SkillForge environment overrides
for each test and restores logger handlers, levels, propagation and disabled
state afterward. Existing application module imports still occur at collection;
run the suite with valid startup configuration.

The HTTP client runs the ASGI application in-process; tests do not bind ports,
contact model providers or require credentials. This is not a browser/E2E suite.

### Verification — 01.04

Last reviewed: **2026-10-07 (America/Sao_Paulo)**, Python 3.14.7.

- `UV_CACHE_DIR=/private/tmp/skillforge-uv-cache uv sync --project backend`:
  exit 0; installed development dependencies in the backend virtual environment.
- `UV_CACHE_DIR=/private/tmp/skillforge-uv-cache uv run --project backend --locked --offline pytest -c backend/pyproject.toml backend/tests -q -W error`:
  exit 0, **15 passed, 17 subtests passed**, no warnings.
- `UV_CACHE_DIR=/private/tmp/skillforge-uv-cache uv pip check --python backend/.venv/bin/python`:
  exit 0; all 23 installed packages compatible.
- `git diff --check`: exit 0. Runtime application source was unchanged.


### Verification — 01.05

Last reviewed: **2026-10-07 (America/Sao_Paulo)**. The
[local development guide](../docs/guides/local-development.md) documents setup,
loopback addresses, independent terminals, shutdown, CORS and port conflicts.
`python3 /private/tmp/skillforge-check-0105.py` exited 0: backend health before
frontend startup, concurrent frontend HTML/API JSON responses, exact CORS origin,
frontend response after backend stop, and backend response after frontend stop.
Temporary processes were cleaned up. Existing dependencies/cache were used;
production build, fresh install and browser integration were not checked.
