"""Public HTTP contracts exercised through the complete ASGI application."""

from importlib.metadata import version

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.settings import Settings


@pytest.fixture
def client():
    with TestClient(create_app(Settings())) as test_client:
        yield test_client


def test_health_is_liveness_only(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {"status": "ok"}


def test_info_matches_installed_distribution(client):
    response = client.get("/api/v1/info")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {
        "name": "skillforge-backend",
        "version": version("skillforge-backend"),
        "api_version": "v1",
    }


@pytest.mark.parametrize("path,model,fields", [
    ("/health", "HealthResponse", {"status"}),
    ("/api/v1/info", "InfoResponse", {"name", "version", "api_version"}),
])
def test_openapi_declares_required_response_fields(client, path, model, fields):
    schema = client.get("/openapi.json").json()
    response = schema["paths"][path]["get"]["responses"]["200"]
    assert response["content"]["application/json"]["schema"] == {
        "$ref": f"#/components/schemas/{model}"
    }
    definition = schema["components"]["schemas"][model]
    assert set(definition["required"]) == fields
    assert set(definition["properties"]) == fields
    assert schema["info"]["version"] == version("skillforge-backend")


@pytest.mark.parametrize("path", ["/health", "/api/v1/info"])
def test_read_only_routes_reject_post(client, path):
    assert client.post(path).status_code == 405


def test_unknown_route_returns_404(client):
    assert client.get("/missing").status_code == 404


def test_environment_settings_reach_cors_middleware(monkeypatch):
    monkeypatch.setenv("SKILLFORGE_CORS_ORIGINS", '["https://frontend.example"]')
    with TestClient(create_app()) as configured_client:
        allowed = configured_client.get("/health", headers={"Origin": "https://frontend.example"})
        denied = configured_client.get("/health", headers={"Origin": "http://localhost:3000"})
    assert allowed.headers["access-control-allow-origin"] == "https://frontend.example"
    assert "access-control-allow-origin" not in denied.headers


@pytest.mark.parametrize("name,value", [
    ("SKILLFORGE_CORS_ORIGINS", '["*"]'),
    ("SKILLFORGE_PORT", "65536"),
    ("SKILLFORGE_LOG_LEVEL", "invalid"),
])
def test_invalid_environment_prevents_app_creation(monkeypatch, name, value):
    monkeypatch.setenv(name, value)
    with pytest.raises(ValueError, match=name):
        create_app()
