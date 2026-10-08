"""Read-only service metadata and liveness endpoints."""

from importlib.metadata import version
from typing import Literal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.logging import RequestLoggingMiddleware
from app.settings import Settings
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: Literal["ok"]


class InfoResponse(BaseModel):
    name: Literal["skillforge-backend"]
    version: str
    api_version: Literal["v1"]


SERVICE_VERSION = version("skillforge-backend")



async def health() -> HealthResponse:
    """Report process liveness, without asserting provider or database readiness."""
    return HealthResponse(status="ok")


async def info() -> InfoResponse:
    """Return public service metadata from the installed distribution."""
    return InfoResponse(
        name="skillforge-backend", version=SERVICE_VERSION, api_version="v1"
    )


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings if settings is not None else Settings.from_env()
    application = FastAPI(title="SkillForge API", version=SERVICE_VERSION)
    application.state.settings = settings
    application.add_api_route("/health", health, methods=["GET"], response_model=HealthResponse)
    application.add_api_route("/api/v1/info", info, methods=["GET"], response_model=InfoResponse)
    application.add_middleware(
        CORSMiddleware, allow_origins=settings.cors_origins,
        allow_credentials=False, allow_methods=["GET"], allow_headers=[],
    )
    application.add_middleware(RequestLoggingMiddleware)
    return application


app = create_app()
