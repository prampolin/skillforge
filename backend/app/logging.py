"""JSON logging that excludes free-form messages and request data by design."""

import json
import logging
from datetime import datetime, timezone
from time import perf_counter


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.fromtimestamp(record.created, timezone.utc).isoformat(),
            "level": record.levelname,
            "event": "server_error" if record.levelno >= logging.ERROR else "server_event",
        }
        if record.name == "skillforge.request" and record.msg == "request_completed":
            payload.update(event="request_completed", status=record.status,
                           duration_ms=record.duration_ms)
        # Never format message arguments, exception text, headers, URLs or bodies.
        return json.dumps(payload)


def configure_logging(level: str) -> None:
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(level)
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access", "skillforge.request"):
        logger = logging.getLogger(name)
        logger.handlers = []
        logger.propagate = True
        logger.setLevel(level)
    logging.getLogger("uvicorn.access").disabled = True


class RequestLoggingMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        started = perf_counter()
        status = 500

        async def capture_status(message):
            nonlocal status
            if message["type"] == "http.response.start":
                status = message["status"]
            await send(message)

        try:
            await self.app(scope, receive, capture_status)
        finally:
            logging.getLogger("skillforge.request").log(
                logging.ERROR if status >= 500 else logging.INFO,
                "request_completed",
                extra={"status": status, "duration_ms": round((perf_counter() - started) * 1000, 3)},
            )
