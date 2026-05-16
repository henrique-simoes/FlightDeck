from __future__ import annotations

import json
import os
from textwrap import dedent
from typing import Any

from ..blueprint_factory import BASE_EVENTS, COMMON_FILTERS, design_hash
from ..models import BlueprintSpec, PersonaId


class BlueprintAgentUnavailable(RuntimeError):
    """Raised when the LangGraph/CopilotKit generator cannot be used."""


def _require_agent_environment() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise BlueprintAgentUnavailable(
            "OPENAI_API_KEY is required for LangGraph/CopilotKit Blueprint generation."
        )


def _build_prompt(
    persona_id: PersonaId,
    persona_md: str,
    blueprint_config: dict[str, Any],
    metrics: dict[str, Any],
    generation_index: int,
    design_md: str,
) -> str:
    design_excerpt = design_md[:8000]
    return dedent(
        f"""
        Generate one Declarative Gen-UI Blueprint for the Eventinkerer event discovery surface.

        This Blueprint is internal configuration for server-side rendering. It must match the
        provided schema exactly. Do not include markdown, comments, hidden reasoning, HTML, JSX,
        or arbitrary executable code.

        Internal persona id:
        {persona_id}

        Persona MD:
        {persona_md}

        Editable Blueprint Configuration JSON:
        {json.dumps(blueprint_config, indent=2)}

        Metrics observed for this persona:
        {json.dumps(metrics, indent=2)}

        Generation index:
        {generation_index}

        Design source excerpt:
        {design_excerpt}

        Allowed catalog:
        - surface_id: event_discovery
        - catalog_version: flightdeck-event-discovery-v1
        - layouts: filters_left, filters_top, compact_toolbar
        - densities: comfortable, compact, editorial
        - filter categories: {json.dumps(COMMON_FILTERS["categories"])}
        - areas: {json.dumps(COMMON_FILTERS["areas"])}
        - date options: {json.dumps(COMMON_FILTERS["date_options"])}
        - events: {json.dumps(BASE_EVENTS, indent=2)}

        Generation rules:
        - Return exactly one BlueprintSpec.
        - Set schema_version to flightdeck.blueprint.v1.
        - Set persona_id to {persona_id}; this remains internal and is not shown to users.
        - Set surface_id to event_discovery.
        - Set catalog_version to flightdeck-event-discovery-v1.
        - Set design_md_hash to {design_hash()}.
        - Pick event_order only from the allowed event ids.
        - Use only allowed categories, areas, date options, layouts, and densities.
        - Use the persona MD and metrics to adapt layout, copy, event order, filters, CTA, and hypothesis.
        - Use generation_index to intentionally produce a meaningfully different candidate than prior runs.
        - Preserve the Eventinkerer brand tone and visual constraints from design.md.
        - The user-facing copy must not mention personas, archetypes, variants, agents, or experiments.
        """
    ).strip()


def generate_blueprint_with_agent(
    *,
    persona_id: PersonaId,
    persona_md: str,
    blueprint_config: dict[str, Any],
    metrics: dict[str, Any],
    generation_index: int,
    design_md: str,
) -> BlueprintSpec:
    _require_agent_environment()

    try:
        from copilotkit import CopilotKitMiddleware
        from langchain.agents import create_agent
    except ImportError as exc:
        raise BlueprintAgentUnavailable(
            "Install backend agent dependencies with `uv sync` before generating with LangGraph/CopilotKit."
        ) from exc

    model = os.getenv("FLIGHTDECK_AGENT_MODEL", "openai:gpt-4.1")
    agent = create_agent(
        model=model,
        tools=[],
        middleware=[CopilotKitMiddleware()],
        response_format=BlueprintSpec,
        system_prompt=(
            "You are FlightDeck's Blueprint Generator Agent. You produce validated, "
            "declarative UI specs for a trusted React renderer. You never generate JSX, "
            "HTML, scripts, hidden reasoning, or user-visible experiment metadata."
        ),
    )
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": _build_prompt(
                        persona_id=persona_id,
                        persona_md=persona_md,
                        blueprint_config=blueprint_config,
                        metrics=metrics,
                        generation_index=generation_index,
                        design_md=design_md,
                    ),
                }
            ]
        }
    )
    structured = result.get("structured_response")
    if structured is None:
        raise BlueprintAgentUnavailable("LangGraph agent did not return a structured BlueprintSpec.")
    if isinstance(structured, BlueprintSpec):
        return structured
    return BlueprintSpec.model_validate(structured)
