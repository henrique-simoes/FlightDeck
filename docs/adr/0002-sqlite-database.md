# SQLite as the primary database

The system needs persistent storage for the Catalog, Library (Blueprints), Experiments, Variants, telemetry events, and the Reasoning Bank. We chose SQLite because the hackathon scope is a single-client, single-project system running locally. SQLite requires zero infrastructure, starts instantly, and stores the entire database in one file — making development, debugging, and demo deployment trivial.

The schema is designed so that migrating to Postgres later is straightforward: standard SQL types, no SQLite-specific features, and a `project_id TEXT DEFAULT 'default'` column on every table to support future multi-tenancy without schema changes.

## Considered Options

- **Postgres** — production-grade, but requires a running server, connection management, and infrastructure that adds friction during a hackathon.
- **Document store (e.g., MongoDB)** — flexible schemas, but Blueprints already have a well-defined structure (A2UI JSON Schema), and the relational model (Experiment → Variant → Blueprint) maps naturally to SQL.
- **SQLite** — chosen. Zero-config, single-file, fast enough for the hackathon's single-user load, and the SQL schema translates directly to Postgres when the time comes.
