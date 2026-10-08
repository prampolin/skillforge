# SkillForge backend

Phase 01.01 introduces an installable Python package. HTTP endpoints, settings,
CORS, logging and tests belong to subsequent phase 01 tasks.

## Environment and dependencies

Supported Python line: **3.14** (`>=3.14,<3.15`); local verification uses 3.14.7.
Other Python lines are not yet part of the supported baseline. `.python-version`
selects the minor line; it does not pin an interpreter patch release.

Direct dependencies are FastAPI 0.142.4 and Uvicorn 0.54.0; the build backend is
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
package is `app`; it does not yet expose an ASGI application. Startup instructions
will be added with the service implementation. No paid model call is involved.

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
No HTTP service, runtime endpoint, test suite, cross-platform compatibility or
other Python version was verified. Next.js source and dependencies were unchanged.
