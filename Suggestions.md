# Suggestions For Future Agents

Last updated: 2026-05-16

This file is the working suggestion board for Codex agents and contributors. Always read it after `README.md`, `CONTEXT.md`, and `frontend/design.md`, then update it when priorities change.

## Current Status

The repo is in a good early-stage shape:

- Product language is defined in `CONTEXT.md`.
- Shared project context and system architecture are defined in `README.md`.
- UI rules, UX Laws, agentic loop rules, Reasoning Bank expectations, metrics, and REST endpoints are unified in `frontend/design.md`.
- `frontend/` is a working TanStack Start app using the event-discovery surface as the first testbed.
- `backend/draft.md` describes the three core backend fluxes: generate Blueprints, critique/manage the Library, and collect usage stats.

Current gap: docs are ahead of implementation. The next useful work is to make the app and backend reflect the language already defined in the docs.

## Immediate Fixes

1. **Fix frontend lint.**
   - Current build passes, but `npm run lint` fails on Prettier formatting.
   - Known files from last inspection:
     - `frontend/src/components/EventFilters.tsx`
     - `frontend/src/components/EventList.tsx`
     - `frontend/src/server.ts`
   - Running `npm run format` inside `frontend/` should likely fix the blocking errors.

2. **Decide on one package manager.**
   - `frontend/` currently has both `package-lock.json` and `bun.lock`.
   - Pick npm or Bun for the project and update docs/scripts accordingly.

3. **Make the frontend reflect FlightDeck, not only Eventinkerer.**
   - Keep Eventinkerer as the first Surface.
   - Add FlightDeck UI around it: active Experiment, assigned Variant, Critique Agent status, first-action expectation, and Reasoning Bank preview.

## Recommended Build Order

### Phase 1: Stabilize Frontend

- Fix formatting/lint.
- Keep `npm run build` passing.
- Add a visible FlightDeck shell around the event-discovery Surface.
- Add static mock panels for:
  - active Experiment,
  - current Variant,
  - expected first action,
  - critique status,
  - Reasoning Bank preview.

### Phase 2: Define Core Types

Add shared TypeScript schemas/types for:

- Blueprint
- Component
- Catalog
- Surface
- Library entry
- Variant
- Experiment
- Telemetry event
- Critique result
- Reasoning Bank entry
- Report summary

Prefer Zod schemas so runtime validation and TypeScript types stay aligned.

### Phase 3: Implement Backend Skeleton

Create a minimal server that implements the REST contract from `README.md` and `frontend/design.md`:

```http
POST /uxr/studies
POST /uxr/tasks
POST /uxr/personas
POST /experiments
POST /experiments/{id}/variants
POST /events/ui-rendered
POST /events/first-action
POST /events/task-completed
POST /events/feedback
GET  /reports/designer/{experiment_id}
GET  /reports/pm/{experiment_id}
GET  /reports/dev/{experiment_id}
GET  /reports/qa/{experiment_id}
```

Start with in-memory storage if needed, then move to a database once schemas settle.

### Phase 4: Implement The Three Hackathon Fluxes

From `backend/draft.md`, implement:

1. **Generate Blueprints**
   - Inputs: system prompt, `frontend/design.md`, Catalog, old Blueprints, stats, and critique results.
   - Output: one or more Blueprint drafts.

2. **Critique and manage Library**
   - Critique Agent validates Blueprint schema, Catalog usage, design rules, accessibility, UX Laws, and experiment isolation.
   - Passing Blueprints enter the Library.
   - Failed Blueprints loop back for regeneration.
   - Library manager can retire Blueprints or queue new Blueprint requests.

3. **Collect usage stats**
   - Capture telemetry events.
   - Aggregate by Experiment, Variant, Surface, task, and archetype.
   - Feed structured evidence into the Reasoning Bank.

### Phase 5: Add LangChain/LangGraph Agents

Implement agents in this order:

1. Intent Agent
2. Blueprint Generator Agent
3. Critique Agent
4. Experiment Agent
5. Telemetry/Reasoning Bank Agent
6. Report Agent
7. Evolution Agent

Keep agent output structured. Do not store or display hidden chain-of-thought.

### Phase 6: Reports And Evaluation

Add role-specific report views:

- Designer/UXR report
- Developer report
- PM report
- QA report

Use the same evidence, but tailor summary, risks, and next actions to each role.

## Product Suggestions

- Treat Eventinkerer as the first experimental Surface, not the final product.
- Use the first visible demo to compare "filters-first" versus "recommendation-first" versus "quiz-first" event discovery.
- Make the first-click expectation visible in the FlightDeck shell so users understand what is being measured.
- Show a simple "Why this Variant exists" rationale, but never hidden reasoning.
- Make the Reasoning Bank visible as evidence snippets: observation, metric, proposed rule, review status.
- Prefer fewer, controlled Variant differences over many flashy differences.

## Technical Suggestions

- Add CI early:
  - install dependencies,
  - lint,
  - build,
  - `design.md` lint.
- Keep `frontend/design.md` valid with:

```bash
npm exec --yes --package=@google/design.md -- design.md lint frontend/design.md
```

- Keep all new domain terms aligned with `CONTEXT.md`.
- If introducing JSON files, do it intentionally with schemas and version fields.
- Keep generated UI declarative. Agents can reference Catalog Components but cannot create arbitrary executable frontend code.

## Guardrails

- Do not create JSON data files until explicitly asked.
- Do not expose hidden chain-of-thought in UI, logs, reports, APIs, or Reasoning Bank entries.
- Do not infer sensitive demographic traits.
- Do not optimize only for clicks; protect comprehension, accessibility, reversibility, and consent.
- Do not treat 5-second tests as final proof. Use them as rapid research probes.
- Keep WCAG 2.1 AA as the minimum; target WCAG 2.2 where practical.
- Keep experiment variables isolated whenever possible.

## Open Questions

- Which backend runtime should the repo use first: TanStack server functions, a separate Node/Hono API, or Python/FastAPI for LangChain alignment?
- Which database should be used first: SQLite for local speed, Postgres for production shape, or a document store for flexible Blueprints?
- Should the Catalog live as TypeScript metadata, database rows, or a versioned JSON schema later?
- Should the first LangChain implementation run locally, through hosted APIs, or through a queue/worker pattern?
- What is the first real user task to optimize: event discovery, checkout, plan comparison, or onboarding?
