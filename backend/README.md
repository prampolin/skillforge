# SkillForge backend

Phase 01.01 introduces an installable Python package; 01.02 adds read-only
health and service-info endpoints. Settings, CORS, logging and pytest coverage
belong to subsequent phase 01 tasks.

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

From `backend/`, run `uv run --no-sync uvicorn app.main:app --host 127.0.0.1 --port 8000`.

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
The joint frontend/backend startup guide remains task 01.05.

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
At 01.01, no HTTP service or runtime endpoint was verified. No pytest suite,
cross-platform compatibility or other Python version has been verified.
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
