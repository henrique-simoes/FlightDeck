from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any

from flightdeck.mcp_server import create_mcp_server


def run(coro):
    return asyncio.run(coro)


async def call_structured(server, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    result = await server.call_tool(name, arguments)
    if isinstance(result, tuple) and len(result) == 2:
        return result[1]
    if isinstance(result, dict):
        return result
    raise AssertionError(f"Unexpected tool result for {name}: {result!r}")


def test_mcp_server_advertises_tools_resources_and_prompts() -> None:
    server = create_mcp_server()

    tools = run(server.list_tools())
    assert {tool.name for tool in tools} == {
        "get_project_snapshot",
        "get_experiment_assignment",
        "list_blueprint_library",
        "summarize_telemetry",
        "critique_blueprint_payload",
        "generate_persona_blueprint",
    }

    resources = run(server.list_resources())
    assert {str(resource.uri) for resource in resources} == {
        "flightdeck://readme",
        "flightdeck://context",
        "flightdeck://design",
        "flightdeck://suggestions",
        "flightdeck://backend_readme",
    }

    templates = run(server.list_resource_templates())
    assert [template.uriTemplate for template in templates] == ["flightdeck://persona/{persona_id}"]

    prompts = run(server.list_prompts())
    assert {prompt.name for prompt in prompts} == {
        "flightdeck_contributor_brief",
        "flightdeck_mcp_usage",
    }

    readme = run(server.read_resource("flightdeck://readme"))
    assert "GenUI FlightDeck" in readme[0].content


def test_mcp_tools_generate_and_read_assignment(tmp_path: Path, monkeypatch) -> None:
    db_path = tmp_path / "flightdeck-mcp-test.db"
    monkeypatch.setenv("FLIGHTDECK_DB_PATH", str(db_path))
    monkeypatch.setattr("flightdeck.generation.append_persona_changelog", lambda *args: None)

    server = create_mcp_server()

    snapshot = run(call_structured(server, "get_project_snapshot", {"include_docs": False}))
    assert snapshot["project"] == "GenUI FlightDeck"
    assert len(snapshot["personas"]) == 4
    assert snapshot["reasoning_bank"]["implemented"] is False

    generated = run(
        call_structured(
            server,
            "generate_persona_blueprint",
            {"persona_id": "scanner", "allow_fallback": True},
        )
    )
    assert generated["status"] == "active"
    assert generated["persona_id"] == "scanner"

    assignment = run(
        call_structured(
            server,
            "get_experiment_assignment",
            {"persona_id": "scanner", "experiment_id": generated["experiment_id"]},
        )
    )
    assert assignment["found"] is True
    assert assignment["assignment"]["blueprint"]["persona_id"] == "scanner"

    library = run(call_structured(server, "list_blueprint_library", {"limit": 5}))
    assert library["blueprints"][0]["id"] == generated["blueprint_id"]

    telemetry = run(
        call_structured(
            server,
            "summarize_telemetry",
            {"experiment_id": generated["experiment_id"], "persona_id": "scanner"},
        )
    )
    assert telemetry["metrics"]["total_events"] == 0

    critique = run(
        call_structured(
            server,
            "critique_blueprint_payload",
            {"blueprint": assignment["assignment"]["blueprint"]["spec"]},
        )
    )
    assert critique["valid_schema"] is True
    assert critique["critique"]["status"] == "passed"
