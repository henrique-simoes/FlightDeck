# Suggestions For Future Agents

Last updated: 2026-05-16

This file is the working suggestion board for Codex agents and contributors. Always read it after `README.md`, `CONTEXT.md`, and `frontend/design.md`, then update it when priorities change.

## Audit Snapshot

The repo is now beyond pure planning. It has a working proof of concept, but several docs still describe the north-star architecture rather than the implementation that exists today.

What is ready:

- Product language is defined in `CONTEXT.md`.
- Shared project context, system architecture, REST contract, agent loop, and Reasoning Bank rules are defined in `README.md`.
- UI rules, UX Laws, agentic-loop rules, metrics, reporting intent, and Design.md constraints are unified in `frontend/design.md`.
- `frontend/design.md` passes the Google `design.md` linter.
- `frontend/` is a working TanStack Start app using the event-discovery Surface as the first visible testbed.
- `frontend/src/gen-ui/GenUIRenderer.tsx` renders the current declarative Blueprint payload with trusted React Components.
- The frontend fetches the default Experiment assignment and posts telemetry for UI rendered, first action, task completed, and feedback events.
- `backend/` has a FastAPI + SQLite proof of concept for Experiments, Blueprints, Variants, assignments, telemetry Events, persona summaries, and manual generation.
- `backend/flightdeck/generation.py` can generate persona-specific Blueprints from `backend/personas/*.md` configuration and activate them as Variants.
- `backend/flightdeck/catalog.py` provides a first rule-based Critique Agent pass for schema/catalog/safety checks.
- Backend tests exist and cover generation, assignment fetch, telemetry write, and repeated generation drift.
- ADRs exist for Python/FastAPI, SQLite, and immutable Catalog JSON snapshots.

Current reality check:

- Agents are not truly agentic yet. The current backend generation loop is deterministic Python code plus persona MD configuration, not LangChain/LangGraph orchestration.
- AG-UI dependencies are installed in `frontend/package.json`, but the app currently uses plain REST fetches and a manual renderer.
- A2UI is present as an architectural target, but the current `BlueprintSpec` is a custom event-discovery schema, not the flat A2UI adjacency-list model described in `CONTEXT.md`.
- CopilotKit and `@copilotkit/a2ui-renderer` are installed, and `backend/reference.ipynb` sketches a direction, but no production CopilotKit provider/runtime or A2UI renderer integration is wired.
- The Reasoning Bank table exists in SQLite, but no store functions, API endpoints, report flow, or agent writes use it yet.

## How Agents, AG-UI, And A2UI Work Today

**Agents:** Today, the "agent" behavior is simulated by deterministic code. `flightdeck generate --all` reads persona configuration, uses telemetry counts, builds a Blueprint, critiques it, stores it, and activates it as a Variant. This is useful for proving the loop, but it is not yet LangChain/LangGraph.

**Critique Agent:** The current Critique Agent is a Python rule function. It checks Catalog version, allowed layout, event ordering, filter validity, allowed gradient prefixes, and basic HTML-payload safety. It does not yet validate against the full `frontend/design.md`, WCAG, UX Laws, experiment isolation, or A2UI JSON Schema.

**AG-UI:** AG-UI packages are installed, but AG-UI is not part of the runtime path yet. There is no bidirectional AG-UI event stream, LangGraph bridge, or CopilotKit runtime endpoint in the app. The current client-server link is REST.

**A2UI:** The repo talks about A2UI correctly as the target safety model: agents produce declarative UI intent and the client renders trusted Components. The current implementation is A2UI-like, but not A2UI-compliant. `CONTEXT.md` says Blueprints should be flat Component references with ID-based parent-child relationships; `backend/flightdeck/models.py` currently stores nested `filters`, `event_list`, and `events` fields.

**CopilotKit:** CopilotKit dependencies are installed and the reference notebook includes example imports, but the live frontend does not wrap the app in CopilotKit and the backend does not expose a CopilotKit runtime endpoint.

## Missing Work

1. **Choose the next schema truth.**
   - Either implement the A2UI adjacency-list Blueprint shape described in `CONTEXT.md`, or explicitly name the current nested schema as `flightdeck.blueprint.event_discovery.v1`.
   - Do this before deeper agent work so LangGraph, AG-UI, reports, and tests do not build on an ambiguous contract.

2. **Wire the Reasoning Bank.**
   - Add models, store functions, and APIs for `reasoning_bank_entries`.
   - Write entries when telemetry indicates a meaningful outcome, such as first-action mismatch, completion, backtracking, or feedback.
   - Store observable evidence only. Do not store hidden chain-of-thought.

3. **Implement the missing REST contract.**
   - Still missing from the README/design contract:

```http
POST /uxr/studies
POST /uxr/tasks
POST /uxr/personas
GET  /reports/designer/{experiment_id}
GET  /reports/pm/{experiment_id}
GET  /reports/dev/{experiment_id}
GET  /reports/qa/{experiment_id}
```

4. **Bring the Catalog ADR into the database.**
   - `docs/adr/0003-catalog-as-versioned-json-in-sqlite.md` says Catalog versions live in a `catalog_versions` table.
   - `backend/migrations/001_initial.sql` does not yet create `catalog_versions`.
   - Add immutable Catalog snapshots before agents start evolving the Catalog.

5. **Resolve Project scoping drift.**
   - `docs/adr/0002-sqlite-database.md` says every table should have `project_id TEXT DEFAULT 'default'`.
   - The current SQLite migration has no `project_id` columns.
   - Either add `project_id` now or update the ADR to make Project scoping a later migration.

6. **Upgrade the Critique Agent.**
   - Validate against the chosen Blueprint schema.
   - Validate against the active Catalog version.
   - Validate `frontend/design.md` tokens and component rules.
   - Add WCAG 2.1 AA minimum checks, reduced-motion checks, keyboard/focus checks, and tap-target checks.
   - Add UX Laws as heuristics, not as automatic proof of quality.
   - Add experiment isolation checks so Variants differ by intentional variables, not random drift.

7. **Make the frontend visibly FlightDeck.**
   - Eventinkerer is a good first Surface, but the UI still mostly looks like an event app.
   - Add FlightDeck shell panels for active Experiment, Variant, expected first action, Critique status, Catalog version, design hash, and Reasoning Bank preview.
   - Keep persona/archetype data internal unless the user has explicitly consented to seeing or editing it.

8. **Wire real LangChain/LangGraph orchestration.**
   - Backend dependencies currently do not include LangChain or LangGraph.
   - Start with a small graph: Intent -> Blueprint Generator -> Critique -> Store/Variant Assignment -> Reasoning Bank.
   - Keep all outputs structured with Pydantic models.

9. **Decide AG-UI/CopilotKit integration path.**
   - Option A: Wire CopilotKit + AG-UI now and make AG-UI the live runtime.
   - Option B: Keep REST for the hackathon and remove or isolate unused AG-UI/CopilotKit dependencies until needed.
   - Avoid letting installed-but-unused packages make contributors believe AG-UI is already working.

10. **Add reports.**
    - Designer/UXR: first actions, path clusters, screenshots later, archetype differences, design-rule proposals.
    - PM: metric direction, uncertainty, ship/iterate/hold/kill recommendation.
    - Dev: schema failures, renderer issues, Catalog mismatches, latency, endpoint errors.
    - QA: accessibility failures, broken actions, regression cases, WCAG checklist status.

11. **Add CI.**
    - Backend: `uv sync`, `uv run pytest -q`.
    - Frontend: `npm ci`, `npm run lint`, `npm run build`.
    - Design: `npm exec --yes --package=@google/design.md -- design.md lint frontend/design.md`.

## Conflicts And Drift

- `CONTEXT.md` describes Blueprints as A2UI-style flat adjacency lists, while the current backend uses a nested event-discovery `BlueprintSpec`.
- ADR 0003 describes `catalog_versions`, but the migration does not implement it.
- ADR 0002 describes `project_id`, but the migration does not implement it.
- `backend/draft.md` still reads like an earlier concept note and uses older language around components, queues, and agents.
- `frontend/readme.md` describes `design.md` mostly as brand/UI direction and should mention the unified FlightDeck design source.
- `frontend/package.json` includes AG-UI, CopilotKit, and A2UI dependencies that are not used by runtime code yet.
- `frontend/` has both `package-lock.json` and `bun.lock`; choose one package manager.
- `frontend/.vite/` is tracked in git. Generated Vite cache should usually be removed and ignored.
- `npm audit --omit=dev` reports moderate vulnerabilities through `prismjs` pulled by `@copilotkit/react-ui` and `react-syntax-highlighter`. Do not force-fix blindly if it downgrades CopilotKit or breaks the app.

## Recommended Build Order

1. Align the docs and implementation vocabulary around the current Blueprint schema.
2. Implement or intentionally defer `catalog_versions` and `project_id`.
3. Add Reasoning Bank store functions and endpoints.
4. Add the missing UXR endpoints.
5. Add role-specific report endpoints.
6. Upgrade Critique Agent checks.
7. Add visible FlightDeck shell panels to the frontend.
8. Wire a minimal LangGraph backend loop.
9. Choose and wire the AG-UI/CopilotKit runtime path, or remove unused dependencies for now.
10. Add CI and package-manager cleanup.

## Product Suggestions

- Treat Eventinkerer as the first experimental Surface, not the final product.
- Use the first visible demo to compare "filters-first", "recommendation-first", "quiz-first", and "compact-toolbar" event discovery.
- Make the first-click expectation visible in the FlightDeck shell so contributors can see what is being measured.
- Show a short "Why this Variant exists" rationale, but never hidden reasoning.
- Make the Reasoning Bank visible as evidence snippets: observation, metric, proposed rule, review status.
- Prefer fewer, controlled Variant differences over many flashy differences.
- Use behavior archetypes as reversible task-context labels, not demographic personas.

## Technical Guardrails

- Do not create JSON data files until explicitly asked.
- Keep generated UI declarative. Agents may reference Catalog Components, but may not create arbitrary executable frontend code.
- Keep all new domain terms aligned with `CONTEXT.md`.
- Keep `frontend/design.md` valid with:

```bash
npm exec --yes --package=@google/design.md -- design.md lint frontend/design.md
```

- Do not expose hidden chain-of-thought in UI, logs, reports, APIs, or Reasoning Bank entries.
- Do not infer sensitive demographic traits.
- Do not optimize only for clicks; protect comprehension, accessibility, reversibility, and consent.
- Do not treat 5-second tests as final proof. Use them as rapid research probes.
- Keep WCAG 2.1 AA as the minimum; target WCAG 2.2 where practical.
- Keep experiment variables isolated whenever possible.

## Open Questions

- Should the hackathon implementation fully adopt A2UI adjacency-list Blueprints now, or keep the current nested event-discovery schema for speed?
- Should AG-UI/CopilotKit be wired immediately, or should the project stabilize the REST PoC first?
- Should Catalog evolution be direct-write for the hackathon or proposal/review from day one?
- What is the first real user task to optimize after event discovery?
- Should reports be generated synchronously from telemetry or asynchronously by a Report Agent?
