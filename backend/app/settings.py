"""Validated environment configuration without dotenv or credential discovery."""

import json
import os
from dataclasses import dataclass
from urllib.parse import urlsplit


@dataclass(frozen=True)
class Settings:
    cors_origins: tuple[str, ...] = ("http://localhost:3000", "http://127.0.0.1:3000")
    log_level: str = "INFO"
    port: int = 8000

    def __post_init__(self) -> None:
        if self.log_level not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
            raise ValueError("SKILLFORGE_LOG_LEVEL must be a supported uppercase log level")
        if type(self.port) is not int or not 1 <= self.port <= 65535:
            raise ValueError("SKILLFORGE_PORT must be an integer between 1 and 65535")
        for origin in self.cors_origins:
            try:
                if not isinstance(origin, str) or any(c.isspace() for c in origin):
                    raise ValueError
                parsed = urlsplit(origin)
                if (parsed.scheme not in {"http", "https"} or not parsed.hostname
                        or parsed.username is not None or parsed.password is not None
                        or parsed.path or parsed.query or parsed.fragment
                        or "*" in origin or "?" in origin or "#" in origin
                        or "\\" in origin or parsed.port == 0):
                    raise ValueError
            except (ValueError, TypeError):
                raise ValueError("SKILLFORGE_CORS_ORIGINS must contain explicit HTTP(S) origins without credentials, paths or wildcards") from None

    @classmethod
    def from_env(cls) -> "Settings":
        try:
            origins = json.loads(os.environ.get("SKILLFORGE_CORS_ORIGINS", json.dumps(cls.cors_origins)))
            if not isinstance(origins, list) or not all(isinstance(v, str) for v in origins):
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError("SKILLFORGE_CORS_ORIGINS must be a JSON array of origins") from None
        try:
            port = int(os.environ.get("SKILLFORGE_PORT", "8000"))
        except ValueError:
            raise ValueError("SKILLFORGE_PORT must be an integer between 1 and 65535") from None
        return cls(tuple(origins), os.environ.get("SKILLFORGE_LOG_LEVEL", "INFO"), port)
