# Local development

Last reviewed: **2026-10-07 (America/Sao_Paulo)**. Phase 01.05.

The current checkout contains a root Next.js application and a separate Python
backend. Use two terminals, both starting in the repository root. The frontend
currently shows the Next.js welcome page; it does not yet call the API or provide
the planned SkillForge dashboard.

## Prerequisites and setup

Use Node.js and npm compatible with the installed Next.js version, Python 3.14,
and uv. This workflow was verified with Node 24.14.0, npm 11.9.0, Python 3.14.7
and uv 0.12.17 on macOS. Other operating systems were not verified.

For a fresh checkout, install the locked dependencies from the repository root:

```bash
npm ci
uv sync --project backend --locked
```

`npm ci` replaces an existing `node_modules`; use it for initial setup or an
intentional reinstall. Skip dependency installation when the existing environments
are already synchronized. The Python environment is `backend/.venv`; no global
Python packages or manual activation are needed. Dependency downloads require
network access. Fresh installation was not repeated during the startup check.

## Start both services

Terminal 1, repository root:

```bash
npm run dev -- --hostname 127.0.0.1 --port 3000
```

Open <http://127.0.0.1:3000>. Next.js provides frontend hot reloading.

Terminal 2, repository root:

```bash
uv run --project backend --locked --offline python -m app
```

The backend binds to <http://127.0.0.1:8000>. `--offline` uses already installed
or cached dependencies; run the setup sync first if packages are missing.
The supported launcher configures JSON logging. It does not auto-reload: restart
it after Python code or environment changes. No model credentials are required.

Both services bind to loopback. Stop each with **Ctrl+C in its own terminal**.
Either service can run alone; stopping one does not stop the other.

## Verify the running services

In a third terminal:

```bash
curl --fail --silent --show-error http://127.0.0.1:3000/ -o /dev/null
curl --fail --silent --show-error http://127.0.0.1:8000/health
curl --fail --silent --show-error http://127.0.0.1:8000/api/v1/info
curl --fail --silent --show-error -i -H 'Origin: http://127.0.0.1:3000' http://127.0.0.1:8000/health
```

Expect HTTP 200 from all four requests, `{"status":"ok"}` for health, and
`{"name":"skillforge-backend","version":"0.1.0","api_version":"v1"}` for info.
The version follows the installed backend distribution. The last response should
include `access-control-allow-origin: http://127.0.0.1:3000`.
The API schema is at <http://127.0.0.1:8000/openapi.json>.

The CORS response header confirms server configuration; curl does not enforce
browser CORS rules. Health reports process liveness only, not provider readiness.

## Ports and troubleshooting

- **Port already in use:** stop your existing service in its terminal, or choose
  another port. Do not terminate an unrelated process. On macOS, inspect listeners
  with `lsof -nP -iTCP:3000 -iTCP:8000 -sTCP:LISTEN`.
- **Next.js lock error:** another dev server may already be using this checkout.
  Reuse it or stop it normally before restarting; do not delete a live lock file.
- **Changed frontend port:** the backend allowlist must match the frontend origin
  exactly, including scheme and port. For example:

  ```bash
  npm run dev -- --hostname 127.0.0.1 --port 3001
  ```

  In the other terminal:

  ```bash
  SKILLFORGE_PORT=8001 SKILLFORGE_CORS_ORIGINS='["http://127.0.0.1:3001"]' uv run --project backend --locked --offline python -m app
  ```

  Use port 8001 for API checks in this case. Alternate-port commands are documented
  configuration options; this startup check used the default ports.
- **Invalid SkillForge configuration:** check the names and formats in the
  [backend settings table](../../backend/README.md#settings-cors-and-logging-0103).
  Error output intentionally omits configuration values. Settings come from the
  process environment; the backend does not load `.env` files.
- **Missing Python package:** run the locked sync from setup; use `uv run` rather
  than a global Python interpreter. Python must be in the supported 3.14 line.
- **Font download errors:** the existing layout uses `next/font/google`; a cold
  compilation may need access to Google Fonts. This verification used the existing
  checkout/cache and does not establish offline behavior on a clean machine.

## Verification evidence

On 2026-10-07 (America/Sao_Paulo), the session-local harness
`python3 /private/tmp/skillforge-check-0105.py` exited **0**. It launched the two
commands above with existing dependencies and polled real HTTP responses:

1. Backend `/health` returned 200 and the expected JSON before frontend startup.
2. Next.js `/` returned 200 with welcome-page HTML while `/api/v1/info` returned
   the v1 JSON contract; the API returned the exact allowed frontend CORS origin.
3. After stopping the backend, the frontend still returned 200.
4. After restarting the backend and stopping the frontend, `/health` still
   returned 200 with the expected JSON.
5. The harness stopped only its own process groups in cleanup.

The harness set `NEXT_TELEMETRY_DISABLED=1`, used
`UV_CACHE_DIR=/private/tmp/skillforge-uv-cache`, and cleared inherited
`SKILLFORGE_*` overrides to check the documented defaults. Temporary diagnostic
logs were written to `/private/tmp/skillforge-0105-frontend.log`,
`/private/tmp/skillforge-0105-backend.log` and
`/private/tmp/skillforge-0105-backend-restart.log`; these are session-local evidence,
not files distributed with the repository.

This verifies development startup and independent service operation. It does not
verify a production build, clean dependency installation, browser interactions,
frontend/API integration, Docker or model execution.
