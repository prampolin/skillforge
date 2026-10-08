"""Keep environment and logging mutations local to each test."""

import logging
import os

import pytest


@pytest.fixture(autouse=True)
def isolated_process_state(monkeypatch):
    for name in tuple(os.environ):
        if name.startswith("SKILLFORGE_"):
            monkeypatch.delenv(name)
    loggers = [logging.getLogger(name) for name in
               ("", "uvicorn", "uvicorn.error", "uvicorn.access", "skillforge.request")]
    states = [(logger, logger.handlers[:], logger.level, logger.propagate, logger.disabled)
              for logger in loggers]
    yield
    for logger, handlers, level, propagate, disabled in states:
        logger.handlers = handlers
        logger.setLevel(level)
        logger.propagate = propagate
        logger.disabled = disabled
