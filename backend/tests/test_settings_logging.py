"""Safety regression checks runnable with the standard library."""

import asyncio
import io
import json
import logging
import os
import unittest
from unittest.mock import patch

from app.logging import JsonFormatter, configure_logging
from app.main import create_app
from app.settings import Settings


async def request(app, method="GET", path="/health", headers=()):
    messages = []
    async def receive():
        return {"type": "http.request", "body": b"secret-body", "more_body": False}
    async def send(message):
        messages.append(message)
    scope = {"type": "http", "asgi": {"version": "3.0"}, "http_version": "1.1",
             "method": method, "scheme": "http", "path": path, "raw_path": path.encode(),
             "query_string": b"token=secret-query", "root_path": "", "headers": list(headers),
             "server": ("localhost", 8000), "client": ("127.0.0.1", 1234)}
    try:
        await app(scope, receive, send)
    except RuntimeError:
        if not any(m.get("status") == 500 for m in messages):
            raise
    start = next(m for m in messages if m["type"] == "http.response.start")
    return start["status"], dict(start["headers"]), b"".join(m.get("body", b"") for m in messages)


class SettingsChecks(unittest.TestCase):
    def test_defaults_and_overrides(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(Settings.from_env(), Settings())
        with patch.dict(os.environ, {"SKILLFORGE_CORS_ORIGINS": '["https://example.com"]',
                                    "SKILLFORGE_PORT": "8123", "SKILLFORGE_LOG_LEVEL": "WARNING"}, clear=True):
            self.assertEqual(Settings.from_env(), Settings(("https://example.com",), "WARNING", 8123))

    def test_invalid_configuration_does_not_echo_values(self):
        for value in ['*', '["*"]', '["https://*.example.com"]', '["null"]', '["https://user:secret@example.com"]',
                      '["https://example.com/secret"]', '["https://example.com?secret"]', '["https://example.com#secret"]',
                      '["https://example.com:99999"]', '[1]', '{}', '["http://example.com\\n"]']:
            with self.subTest(value=value), patch.dict(os.environ, {"SKILLFORGE_CORS_ORIGINS": value}, clear=True):
                with self.assertRaises(ValueError) as error:
                    Settings.from_env()
                self.assertNotIn("secret", str(error.exception))
        for name, value in [("SKILLFORGE_PORT", "secret"), ("SKILLFORGE_PORT", "0"),
                            ("SKILLFORGE_LOG_LEVEL", "secret")]:
            with patch.dict(os.environ, {name: value}, clear=True), self.assertRaises(ValueError):
                Settings.from_env()


class MiddlewareChecks(unittest.TestCase):
    def test_cors_allowlist_and_preflight(self):
        app = create_app(Settings())
        for origin, allowed in [(b"http://localhost:3000", True), (b"http://127.0.0.1:3000", True),
                                (b"https://evil.example", False), (b"http://localhost:3001", False), (b"null", False)]:
            with self.subTest(origin=origin):
                status, headers, body = asyncio.run(request(app, headers=[(b"origin", origin)]))
                self.assertEqual(status, 200)
                self.assertEqual(json.loads(body), {"status": "ok"})
                self.assertEqual(headers.get(b"access-control-allow-origin"), origin if allowed else None)
                self.assertNotIn(b"access-control-allow-credentials", headers)
                status, headers, _ = asyncio.run(request(app, "OPTIONS", headers=[
                    (b"origin", origin), (b"access-control-request-method", b"GET")]))
                self.assertEqual(status, 200 if allowed else 400)
        for extra in [(b"access-control-request-method", b"POST"), (b"access-control-request-headers", b"authorization")]:
            headers = dict([(b"origin", b"http://localhost:3000"), (b"access-control-request-method", b"GET"), extra])
            self.assertEqual(asyncio.run(request(app, "OPTIONS", headers=headers.items()))[0], 400)
        self.assertNotIn(b"access-control-allow-origin", asyncio.run(request(create_app(Settings(())), headers=[(b"origin", b"http://localhost:3000")]))[1])

    def test_json_logs_exclude_sensitive_inputs_and_exceptions(self):
        root = logging.getLogger()
        old_handlers, old_level = root.handlers[:], root.level
        try:
            configure_logging("INFO")
            stream = io.StringIO()
            root.handlers[0].setStream(stream)
            app = create_app(Settings())
            @app.get("/failure")
            async def failure():
                raise RuntimeError("secret-exception")
            for path in ("/health", "/secret-path", "/failure"):
                asyncio.run(request(app, path=path, headers=[(b"authorization", b"Bearer secret-auth"),
                                                            (b"cookie", b"secret-cookie")]))
            logging.getLogger("uvicorn.error").error("secret-server", exc_info=RuntimeError("secret-trace"))
            logging.getLogger("uvicorn.access").info("secret-access")
            raw = stream.getvalue()
            self.assertNotIn("secret", raw)
            rows = [json.loads(line) for line in raw.splitlines()]
            self.assertEqual([row["status"] for row in rows if row["event"] == "request_completed"], [200, 404, 500])
            self.assertTrue(all("timestamp" in row and "level" in row for row in rows))
            self.assertEqual(rows[-1]["event"], "server_error")
            record = logging.LogRecord("other", logging.ERROR, "", 0, "secret", (), None)
            self.assertNotIn("secret", JsonFormatter().format(record))
        finally:
            root.handlers, root.level = old_handlers, old_level


if __name__ == "__main__":
    unittest.main()
