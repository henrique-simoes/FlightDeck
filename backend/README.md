# FlightDeck Backend

FastAPI backend for the Declarative Gen-UI PoC. It owns Experiments, Blueprint Library, Variants, telemetry Events, persona MD summaries, and manual Blueprint generation.

## Setup

```bash
uv sync
```

## Run API

```bash
uv run uvicorn flightdeck.main:app --reload
```

The API runs on `http://localhost:8000` by default.

## Generate Blueprints

Generate all persona assignments:

```bash
uv run flightdeck generate --all
```

Generate one persona:

```bash
uv run flightdeck generate --persona scanner
```

Supported personas are `scanner`, `comparer`, `explorer`, and `expert_operator`.

## Core Endpoints

- `POST /experiments`
- `GET /experiments/default`
- `GET /experiments/{experiment_id}`
- `POST /experiments/{experiment_id}/variants`
- `GET /experiments/{experiment_id}/assignment?persona=scanner`
- `POST /events/ui-rendered`
- `POST /events/first-action`
- `POST /events/task-completed`
- `POST /events/feedback`

## Local Data

SQLite data is stored at `backend/data/flightdeck.db` unless `FLIGHTDECK_DB_PATH` is set. The database is ignored by git; migrations are versioned in `backend/migrations`.
