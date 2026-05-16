# Catalog stored as immutable versioned JSON documents in SQLite

The Catalog defines which Components agents may reference in Blueprints. It must be versioned (Blueprints reference the Catalog version they were validated against), agent-modifiable (the Evolution Agent can add or change Components), and auditable (we need to know who changed what and why).

We store the Catalog as immutable JSON Schema snapshots in a `catalog_versions` table. Each row contains the full Catalog JSON, a version identifier, the parent version it was derived from, and metadata about who created it. Versions are never mutated — agents create new versions. During the hackathon, new versions become immediately active (direct evolution). The north-star design adds a proposal/review flow where versions start as "proposed" and require human approval before activation.

This approach keeps the Catalog as a proper A2UI JSON Schema (which is what the Critique Agent validates Blueprints against), while giving agents runtime write access without file I/O or git operations.

## Considered Options

- **Versioned JSON file on disk** — simple but agents can't modify it at runtime without file I/O, versioning requires git, and it doesn't scale to multi-project.
- **Relational tables** — more queryable, but the Catalog IS a JSON Schema by nature (A2UI spec), and reconstructing it from relational rows adds unnecessary complexity.
- **Immutable JSON documents in SQLite** — chosen. Preserves the JSON Schema format, supports agent modification via new versions, keeps full audit trail, and aligns with future multi-tenancy (each Project gets its own version history).

## Consequences

- Every Blueprint must record which `catalog_version` it was validated against.
- The Critique Agent must always validate against the currently active Catalog version.
- Old Catalog versions are never deleted — they're needed to understand historical Blueprints.
