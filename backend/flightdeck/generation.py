from __future__ import annotations

from datetime import datetime, timezone

from .blueprint_factory import build_blueprint
from .catalog import critique_blueprint
from .db import run_migrations
from .models import PersonaId, VariantCreate
from .personas import PERSONA_SEEDS, append_persona_changelog, ensure_personas_seeded
from .store import (
    aggregate_metrics,
    create_blueprint,
    create_variant,
    get_or_create_default_experiment,
)


def generate_for_persona(persona_id: PersonaId) -> dict[str, str]:
    run_migrations()
    ensure_personas_seeded()
    experiment = get_or_create_default_experiment()
    metrics = aggregate_metrics(experiment_id=experiment.id, persona_id=persona_id)
    spec = build_blueprint(persona_id, metrics)
    critique = critique_blueprint(spec)
    blueprint = create_blueprint(spec, critique)

    if critique.status != "passed":
        return {
            "persona_id": persona_id,
            "blueprint_id": blueprint.id,
            "status": "failed",
            "variant_id": "",
        }

    variant = create_variant(
        experiment.id,
        VariantCreate(
            blueprint_id=blueprint.id,
            persona_id=persona_id,
            status="active",
            expected_first_action=spec.expected_first_action,
        ),
    )
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    append_persona_changelog(
        persona_id,
        (
            f"- {timestamp}: Activated `{blueprint.id}` as `{variant.id}` for "
            f"`{experiment.id}`. Total telemetry events considered: "
            f"{metrics.get('total_events', 0)}."
        ),
    )

    return {
        "persona_id": persona_id,
        "blueprint_id": blueprint.id,
        "variant_id": variant.id,
        "experiment_id": experiment.id,
        "status": "active",
    }


def generate_all() -> list[dict[str, str]]:
    return [generate_for_persona(seed.id) for seed in PERSONA_SEEDS]

