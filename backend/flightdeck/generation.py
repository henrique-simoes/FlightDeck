from __future__ import annotations

from datetime import datetime, timezone

from .agents.blueprint_agent import BlueprintAgentUnavailable, generate_blueprint_with_agent
from .blueprint_factory import build_blueprint
from .catalog import critique_blueprint
from .config import FRONTEND_DESIGN_PATH
from .db import run_migrations
from .models import PersonaId, VariantCreate
from .personas import PERSONA_SEEDS, append_persona_changelog, ensure_personas_seeded
from .personas import read_blueprint_config, read_persona_md
from .store import (
    aggregate_metrics,
    count_blueprints_for_persona,
    create_blueprint,
    create_variant,
    get_or_create_default_experiment,
)


def generate_for_persona(persona_id: PersonaId, allow_fallback: bool = False) -> dict[str, str]:
    run_migrations()
    ensure_personas_seeded()
    experiment = get_or_create_default_experiment()
    metrics = aggregate_metrics(experiment_id=experiment.id, persona_id=persona_id)
    generation_index = count_blueprints_for_persona(persona_id)
    persona_md = read_persona_md(persona_id)
    blueprint_config = read_blueprint_config(persona_id)

    source = "langgraph_copilotkit"
    try:
        spec = generate_blueprint_with_agent(
            persona_id=persona_id,
            persona_md=persona_md,
            blueprint_config=blueprint_config,
            metrics=metrics,
            generation_index=generation_index,
            design_md=FRONTEND_DESIGN_PATH.read_text(encoding="utf-8"),
        )
    except BlueprintAgentUnavailable:
        if not allow_fallback:
            raise
        source = "local_fallback"
        spec = build_blueprint(
            persona_id,
            metrics,
            generation_index=generation_index,
            blueprint_config=blueprint_config,
        )

    critique = critique_blueprint(spec)
    blueprint = create_blueprint(spec, critique)

    if critique.status != "passed":
        return {
            "persona_id": persona_id,
            "blueprint_id": blueprint.id,
            "status": "failed",
            "variant_id": "",
            "source": source,
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
            f"{metrics.get('total_events', 0)}. Generation index: {generation_index}. "
            f"Source: {source}."
        ),
    )

    return {
        "persona_id": persona_id,
        "blueprint_id": blueprint.id,
        "variant_id": variant.id,
        "experiment_id": experiment.id,
        "status": "active",
        "source": source,
    }


def generate_all(allow_fallback: bool = False) -> list[dict[str, str]]:
    return [generate_for_persona(seed.id, allow_fallback=allow_fallback) for seed in PERSONA_SEEDS]
