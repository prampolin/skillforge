"""Contract validation tests without provider calls or registry fixtures."""

import json

import pytest
from pydantic import ValidationError

from app.schemas import Capabilities, Evaluation, Model, Provider, Run, Skill, TokenUsage

REF = {"id": "example", "version": "revision-1"}
RUN = dict(id="run-1", version="1", provider=REF, model=REF,
           evaluation={"id": "EVAL-001", "version": "revision-1"},
           execution_type="cli_agent", variant="baseline",
           created_at="2026-10-07T12:00:00Z")
CASES = [
    (Provider, dict(**REF, name="Example", execution_type="cli_agent")),
    (Model, dict(**REF, name="Example", provider=REF)),
    (Skill, dict(**REF, name="Example", description="Example instructions")),
    (Evaluation, dict(**REF, name="Example", description="Example task", prompt="Build a card")),
    (Run, RUN),
]


@pytest.mark.parametrize("model,payload", CASES)
def test_round_trip_and_json_schema(model, payload):
    value = model.model_validate(payload)
    assert model.model_validate_json(value.model_dump_json()) == value
    assert value.schema_version == "1"
    schema = model.model_json_schema()
    assert {"id", "version"} <= set(schema["required"])
    assert schema["additionalProperties"] is False
    json.dumps(schema)


@pytest.mark.parametrize("model,payload", CASES)
@pytest.mark.parametrize("change", [{"id": ""}, {"version": " "}, {"schema_version": "2"}, {"api_key": "secret"}])
def test_invalid_identity_version_or_extra_fields(model, payload, change):
    with pytest.raises(ValidationError):
        model.model_validate({**payload, **change})


@pytest.mark.parametrize("model,payload", CASES)
def test_version_is_required(model, payload):
    with pytest.raises(ValidationError):
        model.model_validate({k: v for k, v in payload.items() if k != "version"})


def test_unknown_is_not_zero_or_supported():
    assert Capabilities().model_dump() == {"tools": None, "streaming": None, "usage": None}
    run = Run.model_validate(RUN)
    assert run.usage is None
    assert TokenUsage().input_tokens is None
    assert TokenUsage(input_tokens=0).input_tokens == 0
    assert Provider(**REF, name="Example", execution_type="api_model").availability == "unknown"


@pytest.mark.parametrize("value", [-1, True, "12", 1.5])
def test_token_counts_require_nonnegative_integers(value):
    with pytest.raises(ValidationError):
        TokenUsage(input_tokens=value)


@pytest.mark.parametrize("change", [
    {"variant": "with_skill"}, {"skill": REF},
    {"created_at": "2026-10-07T12:00:00"},
    {"status": "running"}, {"status": "completed"},
    {"started_at": "2026-10-07T11:00:00Z"},
    {"status": "failed", "finished_at": "2026-10-07T11:00:00Z"},
    {"model": {"id": "unversioned"}},
])
def test_inconsistent_runs_are_rejected(change):
    with pytest.raises(ValidationError):
        Run.model_validate({**RUN, **change})


def test_completed_skill_run_and_preflight_failure():
    run = Run.model_validate({**RUN, "variant": "with_skill", "skill": REF,
                              "status": "completed", "started_at": "2026-10-07T12:01:00Z",
                              "finished_at": "2026-10-07T12:02:00Z"})
    assert run.skill.version == "revision-1"
    failed = Run.model_validate({**RUN, "status": "failed", "finished_at": "2026-10-07T12:00:01Z"})
    assert failed.started_at is None
