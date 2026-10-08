"""Versioned domain contracts; validation does not execute or discover providers."""

from typing import Annotated, Literal, Self

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, StringConstraints, model_validator

Identifier = Annotated[str, StringConstraints(strict=True, min_length=1, max_length=200,
                                             pattern=r"^[A-Za-z0-9][A-Za-z0-9._:/-]*$")]
Revision = Annotated[str, StringConstraints(strict=True, min_length=1, max_length=200,
                                           pattern=r"^\S+$")]
Text = Annotated[str, StringConstraints(strict=True, min_length=1, pattern=r"\S")]
Count = Annotated[int, Field(strict=True, ge=0)]
ExecutionType = Literal["cli_agent", "api_model", "local_model"]


class Contract(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, hide_input_in_errors=True)


class EntityRef(Contract):
    id: Identifier
    version: Revision


class Entity(EntityRef):
    schema_version: Literal["1"] = "1"


class Capabilities(Contract):
    """Null means unknown, not supported or unsupported."""

    tools: bool | None = Field(default=None, strict=True)
    streaming: bool | None = Field(default=None, strict=True)
    usage: bool | None = Field(default=None, strict=True)


class Provider(Entity):
    name: Text
    execution_type: ExecutionType
    availability: Literal["unknown", "available", "unavailable"] = "unknown"
    capabilities: Capabilities = Field(default_factory=Capabilities)


class Model(Entity):
    name: Text
    provider: EntityRef
    capabilities: Capabilities = Field(default_factory=Capabilities)


class Skill(Entity):
    name: Text
    description: Text


class Evaluation(Entity):
    name: Text
    description: Text
    prompt: Text


class TokenUsage(Contract):
    input_tokens: Count | None = None
    cached_input_tokens: Count | None = None
    output_tokens: Count | None = None


class Run(Entity):
    """One evaluation arm, not an aggregate comparison or a quality score."""

    provider: EntityRef
    model: EntityRef
    evaluation: EntityRef
    execution_type: ExecutionType
    variant: Literal["baseline", "with_skill"]
    skill: EntityRef | None = None
    status: Literal["pending", "running", "completed", "failed", "cancelled"] = "pending"
    created_at: AwareDatetime
    started_at: AwareDatetime | None = None
    finished_at: AwareDatetime | None = None
    usage: TokenUsage | None = None

    @model_validator(mode="after")
    def validate_consistency(self) -> Self:
        if (self.variant == "with_skill") != (self.skill is not None):
            raise ValueError("Only with_skill runs must include a skill reference")
        if self.started_at is not None and self.started_at < self.created_at:
            raise ValueError("started_at must not precede created_at")
        if self.finished_at is not None and self.finished_at < (self.started_at or self.created_at):
            raise ValueError("finished_at must not precede the run's creation or start")
        if self.status == "pending" and (self.started_at is not None or self.finished_at is not None):
            raise ValueError("Pending runs must not have execution timestamps")
        if self.status == "running" and (self.started_at is None or self.finished_at is not None):
            raise ValueError("Running runs require started_at and no finished_at")
        if self.status in {"completed", "failed", "cancelled"} and self.finished_at is None:
            raise ValueError("Terminal runs require finished_at")
        if self.status == "completed" and self.started_at is None:
            raise ValueError("Completed runs require started_at")
        return self
