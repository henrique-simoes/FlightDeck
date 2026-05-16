from __future__ import annotations

from fastapi import APIRouter, HTTPException

from .models import (
    AssignmentResponse,
    ExperimentCreate,
    ExperimentRecord,
    PersonaId,
    TelemetryEventCreate,
    TelemetryEventRecord,
    VariantCreate,
    VariantRecord,
)
from .store import (
    create_experiment,
    create_variant,
    get_assignment,
    get_experiment,
    get_or_create_default_experiment,
    list_personas,
    record_event,
)

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/personas")
def personas():
    return list_personas()


@router.post("/experiments", response_model=ExperimentRecord)
def post_experiment(payload: ExperimentCreate) -> ExperimentRecord:
    return create_experiment(payload)


@router.get("/experiments/default", response_model=ExperimentRecord)
def get_default_experiment() -> ExperimentRecord:
    return get_or_create_default_experiment()


@router.get("/experiments/{experiment_id}", response_model=ExperimentRecord)
def get_experiment_route(experiment_id: str) -> ExperimentRecord:
    experiment = get_experiment(experiment_id)
    if experiment is None:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return experiment


@router.post("/experiments/{experiment_id}/variants", response_model=VariantRecord)
def post_variant(experiment_id: str, payload: VariantCreate) -> VariantRecord:
    if get_experiment(experiment_id) is None:
        raise HTTPException(status_code=404, detail="Experiment not found")
    try:
        return create_variant(experiment_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/experiments/{experiment_id}/assignment", response_model=AssignmentResponse)
def get_assignment_route(experiment_id: str, persona: PersonaId = "scanner") -> AssignmentResponse:
    assignment = get_assignment(experiment_id, persona)
    if assignment is None:
        raise HTTPException(status_code=404, detail="Active assignment not found")
    return assignment


def _event_with_type(event_type: str, payload: TelemetryEventCreate) -> TelemetryEventRecord:
    normalized = payload.model_copy(update={"event_type": event_type})
    return record_event(normalized)


@router.post("/events/ui-rendered", response_model=TelemetryEventRecord)
def ui_rendered(payload: TelemetryEventCreate) -> TelemetryEventRecord:
    return _event_with_type("ui-rendered", payload)


@router.post("/events/first-action", response_model=TelemetryEventRecord)
def first_action(payload: TelemetryEventCreate) -> TelemetryEventRecord:
    return _event_with_type("first-action", payload)


@router.post("/events/task-completed", response_model=TelemetryEventRecord)
def task_completed(payload: TelemetryEventCreate) -> TelemetryEventRecord:
    return _event_with_type("task-completed", payload)


@router.post("/events/feedback", response_model=TelemetryEventRecord)
def feedback(payload: TelemetryEventCreate) -> TelemetryEventRecord:
    return _event_with_type("feedback", payload)

