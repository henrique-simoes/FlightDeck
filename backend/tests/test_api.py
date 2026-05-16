from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient
import pytest

from flightdeck.agents.blueprint_agent import BlueprintAgentUnavailable
from flightdeck.blueprint_factory import build_blueprint
from flightdeck.generation import generate_all, generate_for_persona
from flightdeck.main import create_app
from flightdeck.store import get_blueprint


def _fake_agent(
    *,
    persona_id,
    blueprint_config,
    metrics,
    generation_index,
    **_,
):
    return build_blueprint(
        persona_id,
        metrics,
        generation_index=generation_index,
        blueprint_config=blueprint_config,
    )


def test_generate_and_fetch_assignment(tmp_path: Path, monkeypatch) -> None:
    db_path = tmp_path / "flightdeck-test.db"
    monkeypatch.setenv("FLIGHTDECK_DB_PATH", str(db_path))
    monkeypatch.setattr("flightdeck.generation.append_persona_changelog", lambda *args: None)
    monkeypatch.setattr("flightdeck.generation.generate_blueprint_with_agent", _fake_agent)

    generated = generate_all()
    assert len(generated) == 4
    assert all(item["status"] == "active" for item in generated)
    assert all(item["source"] == "langgraph_copilotkit" for item in generated)

    client = TestClient(create_app())
    experiment = client.get("/experiments/default").json()
    response = client.get(f"/experiments/{experiment['id']}/assignment?persona=comparer")

    assert response.status_code == 200
    payload = response.json()
    assert payload["blueprint"]["persona_id"] == "comparer"
    assert payload["blueprint"]["spec"]["surface_id"] == "event_discovery"


def test_telemetry_event_is_recorded(tmp_path: Path, monkeypatch) -> None:
    db_path = tmp_path / "flightdeck-test.db"
    monkeypatch.setenv("FLIGHTDECK_DB_PATH", str(db_path))
    monkeypatch.setattr("flightdeck.generation.append_persona_changelog", lambda *args: None)
    monkeypatch.setattr("flightdeck.generation.generate_blueprint_with_agent", _fake_agent)
    generated = generate_all()
    scanner = next(item for item in generated if item["persona_id"] == "scanner")

    client = TestClient(create_app())
    response = client.post(
        "/events/first-action",
        json={
            "event_type": "first-action",
            "session_id": "test-session",
            "experiment_id": scanner["experiment_id"],
            "variant_id": scanner["variant_id"],
            "blueprint_id": scanner["blueprint_id"],
            "persona_id": "scanner",
            "surface_id": "event_discovery",
            "target_component": "event-card",
            "first_action_expected": "buy_tickets",
            "first_action_actual": "open_event",
            "metadata": {"source": "test"},
        },
    )

    assert response.status_code == 200
    assert response.json()["event_type"] == "first-action"
    assert response.json()["metadata"]["source"] == "test"


def test_repeated_generation_changes_persona_blueprint(tmp_path: Path, monkeypatch) -> None:
    db_path = tmp_path / "flightdeck-test.db"
    monkeypatch.setenv("FLIGHTDECK_DB_PATH", str(db_path))
    monkeypatch.setattr("flightdeck.generation.append_persona_changelog", lambda *args: None)
    monkeypatch.setattr("flightdeck.generation.generate_blueprint_with_agent", _fake_agent)

    first = generate_for_persona("comparer")
    second = generate_for_persona("comparer")

    first_blueprint = get_blueprint(first["blueprint_id"])
    second_blueprint = get_blueprint(second["blueprint_id"])

    assert first_blueprint is not None
    assert second_blueprint is not None
    assert first_blueprint.spec.layout != second_blueprint.spec.layout
    assert first_blueprint.spec.event_list.title != second_blueprint.spec.event_list.title


def test_generation_requires_agent_unless_fallback_is_explicit(tmp_path: Path, monkeypatch) -> None:
    db_path = tmp_path / "flightdeck-test.db"
    monkeypatch.setenv("FLIGHTDECK_DB_PATH", str(db_path))
    monkeypatch.setattr("flightdeck.generation.append_persona_changelog", lambda *args: None)

    def unavailable_agent(**_):
        raise BlueprintAgentUnavailable("agent unavailable")

    monkeypatch.setattr("flightdeck.generation.generate_blueprint_with_agent", unavailable_agent)

    with pytest.raises(BlueprintAgentUnavailable):
        generate_for_persona("scanner")

    generated = generate_for_persona("scanner", allow_fallback=True)
    assert generated["status"] == "active"
    assert generated["source"] == "local_fallback"
