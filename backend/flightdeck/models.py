from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

PersonaId = Literal["scanner", "comparer", "explorer", "expert_operator"]
SurfaceId = Literal["event_discovery"]
BlueprintStatus = Literal["draft", "validated", "failed", "archived"]
VariantStatus = Literal["draft", "active", "archived", "failed"]
ExperimentStatus = Literal["draft", "active", "paused", "archived"]
GuardrailStatus = Literal["passed", "failed"]
EventType = Literal["ui-rendered", "first-action", "task-completed", "feedback"]


class EventItem(BaseModel):
    id: str
    title: str
    category: str
    date: str
    area: str
    venue: str
    price: str
    attending: str
    gradient: str
    emoji: str


class FilterConfig(BaseModel):
    type: Literal["filters"] = "filters"
    title: str
    search_label: str = "Search"
    search_placeholder: str
    categories: list[str] = Field(min_length=1, max_length=8)
    selected_categories: list[str] = Field(default_factory=list, max_length=8)
    areas: list[str] = Field(min_length=1, max_length=8)
    selected_area: str
    date_options: list[str] = Field(min_length=1, max_length=6)
    max_price: int = Field(ge=0, le=1000)
    primary_action_label: str


class EventListConfig(BaseModel):
    type: Literal["event_list"] = "event_list"
    title: str
    summary: str
    sort_options: list[str] = Field(min_length=1, max_length=6)
    default_sort: str
    density: Literal["comfortable", "compact", "editorial"]
    event_order: list[str] = Field(default_factory=list)
    primary_action_label: str


class BlueprintSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["flightdeck.blueprint.v1"] = "flightdeck.blueprint.v1"
    persona_id: PersonaId
    surface_id: SurfaceId = "event_discovery"
    catalog_version: Literal["flightdeck-event-discovery-v1"]
    design_md_hash: str
    hypothesis: str = Field(min_length=12)
    primary_metric: str = Field(min_length=3)
    layout: Literal["filters_left", "filters_top", "compact_toolbar"]
    expected_first_action: str = Field(min_length=3)
    filters: FilterConfig
    event_list: EventListConfig
    events: list[EventItem] = Field(min_length=1, max_length=12)

    @field_validator("design_md_hash")
    @classmethod
    def validate_design_hash(cls, value: str) -> str:
        if not value.startswith("sha256:"):
            raise ValueError("design_md_hash must start with sha256:")
        return value


class CritiqueResult(BaseModel):
    status: GuardrailStatus
    checks: dict[str, bool]
    summary: str


class BlueprintRecord(BaseModel):
    id: str
    persona_id: PersonaId
    surface_id: SurfaceId
    status: BlueprintStatus
    spec: BlueprintSpec
    critique: CritiqueResult
    catalog_version: str
    design_md_hash: str
    created_at: str


class ExperimentCreate(BaseModel):
    surface_id: SurfaceId = "event_discovery"
    name: str = Field(default="Event discovery PoC", min_length=3)
    hypothesis: str = Field(
        default="Persona-specific event discovery layouts improve first meaningful action."
    )
    primary_metric: str = "time_to_first_correct_action"
    status: ExperimentStatus = "active"


class ExperimentRecord(BaseModel):
    id: str
    surface_id: SurfaceId
    name: str
    hypothesis: str
    primary_metric: str
    status: ExperimentStatus
    created_at: str
    updated_at: str
    variants: list["VariantRecord"] = Field(default_factory=list)
    metrics: dict[str, Any] = Field(default_factory=dict)


class VariantCreate(BaseModel):
    blueprint_id: str
    persona_id: PersonaId
    status: VariantStatus = "active"
    expected_first_action: str | None = None


class VariantRecord(BaseModel):
    id: str
    experiment_id: str
    blueprint_id: str
    persona_id: PersonaId
    surface_id: SurfaceId
    status: VariantStatus
    expected_first_action: str
    guardrail_status: GuardrailStatus
    created_at: str
    activated_at: str | None = None


class AssignmentResponse(BaseModel):
    experiment: ExperimentRecord
    variant: VariantRecord
    blueprint: BlueprintRecord


class TelemetryEventCreate(BaseModel):
    event_type: EventType
    session_id: str = Field(min_length=3)
    experiment_id: str | None = None
    variant_id: str | None = None
    blueprint_id: str | None = None
    persona_id: PersonaId
    surface_id: SurfaceId = "event_discovery"
    target_component: str | None = None
    first_action_expected: str | None = None
    first_action_actual: str | None = None
    task_completed: bool | None = None
    latency_ms: int | None = Field(default=None, ge=0)
    metadata: dict[str, Any] = Field(default_factory=dict)


class TelemetryEventRecord(TelemetryEventCreate):
    id: str
    created_at: str


class PersonaRecord(BaseModel):
    id: PersonaId
    title: str
    md_path: str
    summary: str
    updated_at: str


ExperimentRecord.model_rebuild()

