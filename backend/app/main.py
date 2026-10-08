"""Read-only service metadata and liveness endpoints."""

from importlib.metadata import version
from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: Literal["ok"]


class InfoResponse(BaseModel):
    name: Literal["skillforge-backend"]
    version: str
    api_version: Literal["v1"]


SERVICE_VERSION = version("skillforge-backend")
app = FastAPI(title="SkillForge API", version=SERVICE_VERSION)


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Report process liveness, without asserting provider or database readiness."""
    return HealthResponse(status="ok")


@app.get("/api/v1/info", response_model=InfoResponse)
async def info() -> InfoResponse:
    """Return public service metadata from the installed distribution."""
    return InfoResponse(
        name="skillforge-backend", version=SERVICE_VERSION, api_version="v1"
    )
