"""Run the local API with validated settings and safe JSON logging."""

import logging

import uvicorn

from app.logging import configure_logging
from app.settings import Settings


def main() -> None:
    configure_logging("INFO")
    try:
        settings = Settings.from_env()
    except ValueError:
        logging.getLogger(__name__).error("Invalid server configuration")
        raise SystemExit("Invalid SkillForge configuration; check documented environment variables") from None
    configure_logging(settings.log_level)
    from app.main import create_app

    uvicorn.run(create_app(settings), host="127.0.0.1", port=settings.port,
                log_config=None, access_log=False)


if __name__ == "__main__":
    main()
