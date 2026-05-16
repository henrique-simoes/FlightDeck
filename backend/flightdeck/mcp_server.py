from __future__ import annotations

import os
from pathlib import Path
from typing import Annotated, Any, Literal

from pydantic import Field

os.environ.setdefault("MCP_USE_ANONYMIZED_TELEMETRY", "false")

from mcp.types import ToolAnnotations
from mcp_use.server import MCPServer

from .catalog import critique_blueprint
from .config import FRONTEND_DESIGN_PATH, REPO_ROOT
from .db import run_migrations, session
from .generation import generate_for_persona
from .models import BlueprintSpec, PersonaId
from .personas import ensure_personas_seeded, read_persona_md
from .store import aggregate_metrics, get_assignment, get_blueprint, get_experiment, list_personas

ProjectDoc = Literal["readme", "context", "design", "suggestions", "backend_readme"]
DOC_PATHS: dict[ProjectDoc, Path] = {
    "readme": REPO_ROOT / "README.md",
    "context": REPO_ROOT / "CONTEXT.md",
    "design": FRONTEND_DESIGN_PATH,
    "suggestions": REPO_ROOT / "Suggestions.md",
    "backend_readme": REPO_ROOT / "backend" / "README.md",
}

SERVER_INSTRUCTIONS = """
FlightDeck exposes project context, Blueprint inspection, telemetry summaries, and guarded
generation tools for agents working on GenUI FlightDeck. Treat README.md, CONTEXT.md,
frontend/design.md, and Suggestions.md as the collaboration source of truth. Never expose hidden
chain-of-thought; return concise rationale, observable evidence, and structured outcomes.
""".strip()


def _read_doc(doc: ProjectDoc) -> str:
    return DOC_PATHS[doc].read_text(encoding="utf-8")


def _dump_model(model: Any) -> dict[str, Any]:
    return model.model_dump(mode="json")


def _ensure_state() -> None:
    run_migrations()
    ensure_personas_seeded()


def _active_experiment_id() -> str | None:
    with session() as conn:
        row = conn.execute(
            """
            SELECT id FROM experiments
            WHERE surface_id = 'event_discovery' AND status = 'active'
            ORDER BY created_at ASC
            LIMIT 1
            """
        ).fetchone()
    return row["id"] if row else None


def _recent_blueprints(limit: int, persona_id: PersonaId | None = None) -> list[dict[str, Any]]:
    clauses: list[str] = []
    params: list[Any] = []
    if persona_id:
        clauses.append("persona_id = ?")
        params.append(persona_id)

    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    params.append(limit)
    with session() as conn:
        rows = conn.execute(
            f"""
            SELECT id
            FROM blueprints
            {where}
            ORDER BY created_at DESC
            LIMIT ?
            """,
            params,
        ).fetchall()

    blueprints = []
    for row in rows:
        blueprint = get_blueprint(row["id"])
        if blueprint:
            blueprints.append(_dump_model(blueprint))
    return blueprints


def _reasoning_bank_summary() -> dict[str, Any]:
    with session() as conn:
        total = conn.execute("SELECT COUNT(*) AS total FROM reasoning_bank_entries").fetchone()
        by_status = conn.execute(
            """
            SELECT status, COUNT(*) AS total
            FROM reasoning_bank_entries
            GROUP BY status
            ORDER BY status
            """
        ).fetchall()
    return {
        "total_entries": int(total["total"]),
        "status_counts": {row["status"]: int(row["total"]) for row in by_status},
        "implemented": False,
        "note": (
            "The SQLite table exists, but current backend code does not yet write "
            "Reasoning Bank entries from telemetry or reports."
        ),
    }


def create_mcp_server(debug: bool = False) -> MCPServer:
    server = MCPServer(
        name="flightdeck-mcp",
        version="0.1.0",
        instructions=SERVER_INSTRUCTIONS,
        debug=debug,
        mcp_path="/mcp",
        openmcp_path="/openmcp.json",
    )

    @server.resource(
        uri="flightdeck://readme",
        name="flightdeck_readme",
        title="FlightDeck README",
        description="Shared session context, project concept, architecture, and collaboration rules.",
        mime_type="text/markdown",
    )
    def readme() -> str:
        return _read_doc("readme")

    @server.resource(
        uri="flightdeck://context",
        name="flightdeck_context",
        title="FlightDeck Domain Context",
        description="Ubiquitous language for Blueprints, Components, Catalogs, Surfaces, and Experiments.",
        mime_type="text/markdown",
    )
    def context() -> str:
        return _read_doc("context")

    @server.resource(
        uri="flightdeck://design",
        name="flightdeck_design_md",
        title="FlightDeck DESIGN.md",
        description="Frontend UI, UX Laws, live testing, Reasoning Bank, and agentic loop rules.",
        mime_type="text/markdown",
    )
    def design() -> str:
        return _read_doc("design")

    @server.resource(
        uri="flightdeck://suggestions",
        name="flightdeck_suggestions",
        title="FlightDeck Suggestions",
        description="Current implementation gaps and recommended next steps for contributor agents.",
        mime_type="text/markdown",
    )
    def suggestions() -> str:
        return _read_doc("suggestions")

    @server.resource(
        uri="flightdeck://backend_readme",
        name="flightdeck_backend_readme",
        title="FlightDeck Backend README",
        description="Backend setup, API, MCP server, and local data documentation.",
        mime_type="text/markdown",
    )
    def backend_readme() -> str:
        return _read_doc("backend_readme")

    @server.resource(
        uri="flightdeck://persona/{persona_id}",
        name="flightdeck_persona",
        title="FlightDeck Persona Markdown",
        description="Persona/archetype configuration markdown used by the Blueprint generation loop.",
        mime_type="text/markdown",
    )
    def persona(persona_id: str) -> str:
        if persona_id not in {"scanner", "comparer", "explorer", "expert_operator"}:
            raise ValueError("Unknown persona_id")
        return read_persona_md(persona_id)  # type: ignore[arg-type]

    @server.prompt(
        name="flightdeck_contributor_brief",
        title="FlightDeck Contributor Brief",
        description="Give an agent the minimal context needed before changing FlightDeck.",
    )
    def contributor_brief() -> str:
        return (
            "You are contributing to GenUI FlightDeck. Read flightdeck://readme, "
            "flightdeck://context, flightdeck://design, and flightdeck://suggestions first. "
            "Keep generated UI declarative, preserve the Catalog/Blueprint/Variant language, "
            "do not expose hidden chain-of-thought, and update Suggestions.md when priorities change."
        )

    @server.prompt(
        name="flightdeck_mcp_usage",
        title="FlightDeck MCP Usage",
        description="Explain how an agent should use this MCP server safely.",
    )
    def mcp_usage() -> str:
        return (
            "Use resources for source-of-truth docs, read-only tools for snapshots and telemetry, "
            "critique_blueprint_payload before storing generated UI, and call generate_persona_blueprint "
            "only when the user wants a new activated Blueprint because it writes to SQLite."
        )

    @server.tool(
        name="get_project_snapshot",
        title="Get FlightDeck Project Snapshot",
        description="Return current project docs, personas, active Experiment, telemetry, and Reasoning Bank status.",
        annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True, openWorldHint=False),
        structured_output=True,
    )
    def get_project_snapshot(
        include_docs: Annotated[
            bool,
            Field(description="Include short excerpts from README.md, CONTEXT.md, design.md, and Suggestions.md."),
        ] = False,
    ) -> dict[str, Any]:
        _ensure_state()
        experiment_id = _active_experiment_id()
        experiment = get_experiment(experiment_id) if experiment_id else None
        docs = {
            name: {
                "path": str(path.relative_to(REPO_ROOT)),
                "resource_uri": f"flightdeck://{name}",
                "exists": path.exists(),
            }
            for name, path in DOC_PATHS.items()
        }
        if include_docs:
            for name in docs:
                text = _read_doc(name)  # type: ignore[arg-type]
                docs[name]["excerpt"] = text[:1200]

        return {
            "project": "GenUI FlightDeck",
            "docs": docs,
            "personas": [_dump_model(persona) for persona in list_personas()],
            "active_experiment": _dump_model(experiment) if experiment else None,
            "metrics": aggregate_metrics(experiment_id=experiment_id) if experiment_id else aggregate_metrics(),
            "recent_blueprints": _recent_blueprints(limit=5),
            "reasoning_bank": _reasoning_bank_summary(),
        }

    @server.tool(
        name="get_experiment_assignment",
        title="Get Experiment Assignment",
        description="Return the active Variant and Blueprint assignment for a persona/archetype.",
        annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True, openWorldHint=False),
        structured_output=True,
    )
    def get_experiment_assignment(
        persona_id: Annotated[PersonaId, Field(description="Persona/archetype to inspect.")],
        experiment_id: Annotated[
            str | None,
            Field(description="Experiment id. If omitted, the active event_discovery Experiment is used."),
        ] = None,
    ) -> dict[str, Any]:
        _ensure_state()
        resolved_experiment_id = experiment_id or _active_experiment_id()
        if not resolved_experiment_id:
            return {
                "found": False,
                "message": "No active Experiment exists yet. Generate a Blueprint first.",
            }
        assignment = get_assignment(resolved_experiment_id, persona_id)
        if assignment is None:
            return {
                "found": False,
                "experiment_id": resolved_experiment_id,
                "persona_id": persona_id,
                "message": "No active Variant assignment exists for this persona.",
            }
        return {"found": True, "assignment": _dump_model(assignment)}

    @server.tool(
        name="list_blueprint_library",
        title="List Blueprint Library",
        description="List recent stored Blueprints with critique results and specs.",
        annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True, openWorldHint=False),
        structured_output=True,
    )
    def list_blueprint_library(
        limit: Annotated[int, Field(description="Maximum number of Blueprints to return.", ge=1, le=25)] = 10,
        persona_id: Annotated[PersonaId | None, Field(description="Optional persona/archetype filter.")] = None,
    ) -> dict[str, Any]:
        _ensure_state()
        return {"blueprints": _recent_blueprints(limit=limit, persona_id=persona_id)}

    @server.tool(
        name="summarize_telemetry",
        title="Summarize Telemetry",
        description="Aggregate FlightDeck telemetry by Experiment and optional persona/archetype.",
        annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True, openWorldHint=False),
        structured_output=True,
    )
    def summarize_telemetry(
        experiment_id: Annotated[
            str | None,
            Field(description="Experiment id. If omitted, the active event_discovery Experiment is used."),
        ] = None,
        persona_id: Annotated[PersonaId | None, Field(description="Optional persona/archetype filter.")] = None,
    ) -> dict[str, Any]:
        _ensure_state()
        resolved_experiment_id = experiment_id or _active_experiment_id()
        return {
            "experiment_id": resolved_experiment_id,
            "persona_id": persona_id,
            "metrics": aggregate_metrics(experiment_id=resolved_experiment_id, persona_id=persona_id),
            "reasoning_bank": _reasoning_bank_summary(),
        }

    @server.tool(
        name="critique_blueprint_payload",
        title="Critique Blueprint Payload",
        description="Validate and critique a BlueprintSpec-shaped payload without storing it.",
        annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True, openWorldHint=False),
        structured_output=True,
    )
    def critique_blueprint_payload(
        blueprint: Annotated[
            dict[str, Any],
            Field(description="BlueprintSpec JSON payload to validate against the current event-discovery schema."),
        ],
    ) -> dict[str, Any]:
        spec = BlueprintSpec.model_validate(blueprint)
        critique = critique_blueprint(spec)
        return {"valid_schema": True, "critique": _dump_model(critique), "spec": _dump_model(spec)}

    @server.tool(
        name="generate_persona_blueprint",
        title="Generate Persona Blueprint",
        description="Generate, critique, store, and activate a new Blueprint Variant for one persona/archetype.",
        annotations=ToolAnnotations(destructiveHint=True, idempotentHint=False, openWorldHint=True),
        structured_output=True,
    )
    def generate_persona_blueprint(
        persona_id: Annotated[PersonaId, Field(description="Persona/archetype to generate for.")],
        allow_fallback: Annotated[
            bool,
            Field(description="Use deterministic local generation when LangGraph/CopilotKit is unavailable."),
        ] = True,
    ) -> dict[str, Any]:
        return generate_for_persona(persona_id, allow_fallback=allow_fallback)

    return server


def main() -> None:
    server = create_mcp_server(debug=os.getenv("FLIGHTDECK_MCP_DEBUG") == "1")
    server.run(
        transport=os.getenv("FLIGHTDECK_MCP_TRANSPORT", "streamable-http"),
        host=os.getenv("FLIGHTDECK_MCP_HOST", "0.0.0.0"),
        port=int(os.getenv("FLIGHTDECK_MCP_PORT", "8010")),
        debug=os.getenv("FLIGHTDECK_MCP_DEBUG") == "1",
    )
