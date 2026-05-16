from __future__ import annotations

from collections import Counter
import json
from typing import Any
from uuid import uuid4

from .db import session
from .models import (
    AssignmentResponse,
    BlueprintRecord,
    BlueprintSpec,
    CritiqueResult,
    ExperimentCreate,
    ExperimentRecord,
    PersonaId,
    PersonaRecord,
    TelemetryEventCreate,
    TelemetryEventRecord,
    VariantCreate,
    VariantRecord,
)


def _row_to_variant(row: Any) -> VariantRecord:
    return VariantRecord(
        id=row["id"],
        experiment_id=row["experiment_id"],
        blueprint_id=row["blueprint_id"],
        persona_id=row["persona_id"],
        surface_id=row["surface_id"],
        status=row["status"],
        expected_first_action=row["expected_first_action"],
        guardrail_status=row["guardrail_status"],
        created_at=row["created_at"],
        activated_at=row["activated_at"],
    )


def _row_to_blueprint(row: Any) -> BlueprintRecord:
    return BlueprintRecord(
        id=row["id"],
        persona_id=row["persona_id"],
        surface_id=row["surface_id"],
        status=row["status"],
        spec=BlueprintSpec.model_validate_json(row["spec_json"]),
        critique=CritiqueResult.model_validate_json(row["critique_json"]),
        catalog_version=row["catalog_version"],
        design_md_hash=row["design_md_hash"],
        created_at=row["created_at"],
    )


def upsert_persona(persona_id: PersonaId, title: str, md_path: str, summary: str) -> None:
    with session() as conn:
        conn.execute(
            """
            INSERT INTO personas (id, title, md_path, summary, updated_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(id) DO UPDATE SET
              title = excluded.title,
              md_path = excluded.md_path,
              summary = excluded.summary,
              updated_at = CURRENT_TIMESTAMP
            """,
            (persona_id, title, md_path, summary),
        )


def list_personas() -> list[PersonaRecord]:
    with session() as conn:
        rows = conn.execute("SELECT * FROM personas ORDER BY id").fetchall()
    return [PersonaRecord.model_validate(dict(row)) for row in rows]


def create_blueprint(spec: BlueprintSpec, critique: CritiqueResult) -> BlueprintRecord:
    blueprint_id = f"bp_{uuid4().hex[:12]}"
    status = "validated" if critique.status == "passed" else "failed"
    with session() as conn:
        conn.execute(
            """
            INSERT INTO blueprints (
              id, persona_id, surface_id, status, spec_json, critique_json,
              catalog_version, design_md_hash
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                blueprint_id,
                spec.persona_id,
                spec.surface_id,
                status,
                spec.model_dump_json(),
                critique.model_dump_json(),
                spec.catalog_version,
                spec.design_md_hash,
            ),
        )
        row = conn.execute("SELECT * FROM blueprints WHERE id = ?", (blueprint_id,)).fetchone()
    return _row_to_blueprint(row)


def get_blueprint(blueprint_id: str) -> BlueprintRecord | None:
    with session() as conn:
        row = conn.execute("SELECT * FROM blueprints WHERE id = ?", (blueprint_id,)).fetchone()
    return _row_to_blueprint(row) if row else None


def create_experiment(payload: ExperimentCreate) -> ExperimentRecord:
    experiment_id = f"exp_{uuid4().hex[:12]}"
    with session() as conn:
        conn.execute(
            """
            INSERT INTO experiments (id, surface_id, name, hypothesis, primary_metric, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                experiment_id,
                payload.surface_id,
                payload.name,
                payload.hypothesis,
                payload.primary_metric,
                payload.status,
            ),
        )
    return get_experiment(experiment_id)  # type: ignore[return-value]


def get_or_create_default_experiment() -> ExperimentRecord:
    with session() as conn:
        row = conn.execute(
            """
            SELECT id FROM experiments
            WHERE surface_id = 'event_discovery' AND status = 'active'
            ORDER BY created_at ASC
            LIMIT 1
            """
        ).fetchone()
    if row:
        return get_experiment(row["id"])  # type: ignore[return-value]
    return create_experiment(ExperimentCreate())


def list_variants(experiment_id: str) -> list[VariantRecord]:
    with session() as conn:
        rows = conn.execute(
            "SELECT * FROM variants WHERE experiment_id = ? ORDER BY created_at DESC",
            (experiment_id,),
        ).fetchall()
    return [_row_to_variant(row) for row in rows]


def aggregate_metrics(experiment_id: str | None = None, persona_id: PersonaId | None = None) -> dict[str, Any]:
    clauses: list[str] = []
    params: list[str] = []
    if experiment_id:
        clauses.append("experiment_id = ?")
        params.append(experiment_id)
    if persona_id:
        clauses.append("persona_id = ?")
        params.append(persona_id)

    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    with session() as conn:
        rows = conn.execute(
            f"SELECT event_type, target_component FROM telemetry_events {where}",
            params,
        ).fetchall()

    event_counts = Counter(row["event_type"] for row in rows)
    target_counts = Counter(row["target_component"] for row in rows if row["target_component"])
    return {
        "event_counts": dict(event_counts),
        "top_targets": dict(target_counts.most_common(5)),
        "total_events": len(rows),
    }


def get_experiment(experiment_id: str) -> ExperimentRecord | None:
    with session() as conn:
        row = conn.execute("SELECT * FROM experiments WHERE id = ?", (experiment_id,)).fetchone()
    if not row:
        return None
    return ExperimentRecord(
        id=row["id"],
        surface_id=row["surface_id"],
        name=row["name"],
        hypothesis=row["hypothesis"],
        primary_metric=row["primary_metric"],
        status=row["status"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        variants=list_variants(experiment_id),
        metrics=aggregate_metrics(experiment_id=experiment_id),
    )


def create_variant(experiment_id: str, payload: VariantCreate) -> VariantRecord:
    blueprint = get_blueprint(payload.blueprint_id)
    if blueprint is None:
        raise ValueError("Blueprint not found")
    if blueprint.status != "validated":
        raise ValueError("Only validated blueprints can be assigned as variants")
    if blueprint.persona_id != payload.persona_id:
        raise ValueError("Blueprint persona does not match requested variant persona")

    variant_id = f"var_{uuid4().hex[:12]}"
    expected_first_action = payload.expected_first_action or blueprint.spec.expected_first_action
    with session() as conn:
        if payload.status == "active":
            conn.execute(
                """
                UPDATE variants
                SET status = 'archived'
                WHERE experiment_id = ? AND persona_id = ? AND status = 'active'
                """,
                (experiment_id, payload.persona_id),
            )
        conn.execute(
            """
            INSERT INTO variants (
              id, experiment_id, blueprint_id, persona_id, surface_id, status,
              expected_first_action, guardrail_status, activated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, CASE WHEN ? = 'active' THEN CURRENT_TIMESTAMP ELSE NULL END)
            """,
            (
                variant_id,
                experiment_id,
                blueprint.id,
                payload.persona_id,
                blueprint.surface_id,
                payload.status,
                expected_first_action,
                blueprint.critique.status,
                payload.status,
            ),
        )
        row = conn.execute("SELECT * FROM variants WHERE id = ?", (variant_id,)).fetchone()
    return _row_to_variant(row)


def get_assignment(experiment_id: str, persona_id: PersonaId) -> AssignmentResponse | None:
    with session() as conn:
        row = conn.execute(
            """
            SELECT * FROM variants
            WHERE experiment_id = ? AND persona_id = ? AND status = 'active'
            ORDER BY activated_at DESC, created_at DESC
            LIMIT 1
            """,
            (experiment_id, persona_id),
        ).fetchone()
    if not row:
        return None
    variant = _row_to_variant(row)
    blueprint = get_blueprint(variant.blueprint_id)
    experiment = get_experiment(experiment_id)
    if not blueprint or not experiment:
        return None
    return AssignmentResponse(experiment=experiment, variant=variant, blueprint=blueprint)


def record_event(payload: TelemetryEventCreate) -> TelemetryEventRecord:
    event_id = f"evt_{uuid4().hex[:12]}"
    with session() as conn:
        conn.execute(
            """
            INSERT INTO telemetry_events (
              id, event_type, session_id, experiment_id, variant_id, blueprint_id,
              persona_id, surface_id, target_component, first_action_expected,
              first_action_actual, task_completed, latency_ms, metadata_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                event_id,
                payload.event_type,
                payload.session_id,
                payload.experiment_id,
                payload.variant_id,
                payload.blueprint_id,
                payload.persona_id,
                payload.surface_id,
                payload.target_component,
                payload.first_action_expected,
                payload.first_action_actual,
                None if payload.task_completed is None else int(payload.task_completed),
                payload.latency_ms,
                json.dumps(payload.metadata),
            ),
        )
        row = conn.execute("SELECT * FROM telemetry_events WHERE id = ?", (event_id,)).fetchone()

    return TelemetryEventRecord(
        id=row["id"],
        event_type=row["event_type"],
        session_id=row["session_id"],
        experiment_id=row["experiment_id"],
        variant_id=row["variant_id"],
        blueprint_id=row["blueprint_id"],
        persona_id=row["persona_id"],
        surface_id=row["surface_id"],
        target_component=row["target_component"],
        first_action_expected=row["first_action_expected"],
        first_action_actual=row["first_action_actual"],
        task_completed=None if row["task_completed"] is None else bool(row["task_completed"]),
        latency_ms=row["latency_ms"],
        metadata=json.loads(row["metadata_json"]),
        created_at=row["created_at"],
    )

