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

## Customize Blueprint Output

Each persona file in `backend/personas/` includes an internal `Blueprint Configuration` JSON block. Edit that block to guide future generated Blueprints.

Useful fields:

- `layouts`: cycles through `filters_left`, `filters_top`, and `compact_toolbar`.
- `list_titles` and `summaries`: public copy for the generated surface.
- `selected_categories`, `selected_areas`, and `max_prices`: initial filter state.
- `event_orders`: event IDs in the order they should appear.
- `list_ctas`: card CTA copy.

Every run uses the next value in each list based on how many Blueprints already exist for that persona. For example, running this repeatedly will cycle through the configured variants:

```bash
uv run flightdeck generate --persona comparer
```

The persona/archetype metadata is internal. It is stored for assignment and telemetry, but the frontend does not display the user's assigned persona.

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
