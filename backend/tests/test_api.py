from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from flightdeck.generation import generate_all, generate_for_persona
from flightdeck.main import create_app
from flightdeck.store import get_blueprint


def test_generate_and_fetch_assignment(tmp_path: Path, monkeypatch) -> None:
    db_path = tmp_path / "flightdeck-test.db"
    monkeypatch.setenv("FLIGHTDECK_DB_PATH", str(db_path))
    monkeypatch.setattr("flightdeck.generation.append_persona_changelog", lambda *args: None)

    generated = generate_all()
    assert len(generated) == 4
    assert all(item["status"] == "active" for item in generated)

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

    first = generate_for_persona("comparer")
    second = generate_for_persona("comparer")

    first_blueprint = get_blueprint(first["blueprint_id"])
    second_blueprint = get_blueprint(second["blueprint_id"])

    assert first_blueprint is not None
    assert second_blueprint is not None
    assert first_blueprint.spec.layout != second_blueprint.spec.layout
    assert first_blueprint.spec.event_list.title != second_blueprint.spec.event_list.title
