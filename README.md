# GenUI FlightDeck Sessions Context

## Project Concept

**GenUI FlightDeck** is a website and agentic experimentation system for building trustworthy generated interfaces. It turns every generated UI into a measurable experiment: agents create declarative UI **Blueprints**, validate them against an approved **Catalog** of trusted Components and `frontend/design.md`, deploy them as **Variants** on a product **Surface**, and learn from real interaction evidence.

The first visible Surface is an event-discovery experience, but the product is not just an events app. The event UI is the testbed for the larger FlightDeck loop: generate multiple interface approaches, choose the most relevant first action for a user task, test which approach works better for different behavior archetypes, and feed those results into a structured **Reasoning Bank**.

FlightDeck is designed around a controlled GenUI safety model. Agents should not invent executable frontend code at runtime. They produce declarative Blueprints that reference pre-approved Components, while the client renders those Components through a trusted renderer. The system should eventually align this model with A2UI-style payloads, AG-UI/CopilotKit runtime interaction, and LangChain/LangGraph orchestration.

The project does four things:

1. **Generate UI Blueprints:** Given a task, persona/archetype, prior telemetry, and design rules, the system creates controlled interface candidates for the highest-leverage action point.
2. **Critique and validate them:** A Critique Agent checks schema, Catalog usage, `frontend/design.md`, UX Laws, accessibility, copy clarity, motion, and experiment isolation before a Blueprint enters the Library.
3. **Run live experiments:** Experiments assign validated Blueprints as Variants, serve them on a Surface, and collect signals such as first action, task completion, backtracks, variant switches, latency, accessibility status, and feedback.
4. **Turn evidence into improvement:** The Reasoning Bank stores structured outcomes and proposed design rules, then future agents use that evidence to improve new Blueprints, reports, `frontend/design.md`, and possibly system prompts.

The north-star product is an experimentation cockpit for generated interfaces. Designers and UXRs should get first-click evidence and design-rule recommendations. Developers should get schema, renderer, Catalog, latency, and replay information. PMs should get experiment status, uncertainty, and ship/iterate/hold recommendations. QA should get accessibility, regression, and broken-action evidence.

The hackathon implementation currently proves the loop with a FastAPI + SQLite backend, deterministic Blueprint generation, a rule-based critique pass, a TanStack Start frontend, a manual GenUI renderer, and REST telemetry. The next evolution is to make the loop truly agentic with LangChain/LangGraph, wire AG-UI/CopilotKit where useful, align Blueprints with the chosen A2UI contract, and activate the Reasoning Bank and report endpoints.

Last updated: 2026-05-16

This README is the shared session context for Codex agents and contributors working on **GenUI FlightDeck**. Read this before changing the repo. The goal is for every contributor session to start from the same product intent, design rules, and collaboration protocol.

## What This Project Is

GenUI FlightDeck is a website and agentic system for generating, validating, live-testing, and improving generated user interfaces.

The core idea is **live experimentation for GenUIs**:

1. A user prompt arrives.
2. Agents infer the user's goal and highest-leverage first action.
3. Agents generate multiple **Blueprints** — declarative UI payloads that reference **Components** from the approved **Catalog**.
4. The **Critique Agent** validates each Blueprint against schema, Catalog, accessibility, UX heuristics, and design compliance.
5. Validated Blueprints enter the **Library**.
6. An **Experiment** assigns Blueprints as **Variants** and serves them on a **Surface**. The website logs interaction signals.
7. The system writes structured experiment learnings into the **Reasoning Bank**.
8. Future Blueprints improve from those learnings.
9. Agents may propose improvements to `frontend/design.md` and possibly the system prompt, but changes must be reviewable and auditable.

This is not meant to become a generic GenUI demo. It is an experimentation cockpit for generated interfaces: every Blueprint should carry a hypothesis, pass guardrails, produce measurable evidence, and improve future UI decisions.

See `CONTEXT.md` for the full glossary of ubiquitous language used throughout this project.

## Source Of Truth

Use this hierarchy:

1. **`CONTEXT.md`** is the ubiquitous language glossary. Every domain term used across the codebase is defined here.
2. **`frontend/design.md`** is the single source of truth for the frontend UI, FlightDeck UX Laws, agentic loop, live testing model, Reasoning Bank, and reporting rules.
3. **`Suggestions.md`** is the shared suggestion board. Agents should consult it before planning work and update it when priorities change.
4. **`README.md`** is the shared session context for agents and contributors.
5. **`docs/mcp.md`** explains the FlightDeck Manufact MCP server for contributor agents.
6. **`frontend/readme.md`** is the technical README for running and understanding the current frontend app.

The current `frontend/design.md` merges two layers:

- **UI layer:** Eventinkerer-style frontend identity with violet-to-cyan gradient, soft rounded controls, clear metadata hierarchy, event filters, and responsive event cards.
- **FlightDeck layer:** UX-law critique, A/B/N testing, behavior archetypes, LangChain/LangGraph agent loop, Reasoning Bank, UXR endpoints, accessibility gates, and role-specific reports.

Whenever the product direction changes, update this README. Whenever the design system, UI rules, or agentic testing rules change, update `frontend/design.md`. Whenever domain terminology is added or clarified, update `CONTEXT.md`. Whenever priorities, next steps, or implementation recommendations change, update `Suggestions.md`.

## Current Main Branch State

The public repo is:

`https://github.com/henrique-simoes/FlightDeck`

Current main branch contains:
- `backend/`: FastAPI PoC backend for Experiments, Blueprint Library, Variants, telemetry Events, persona MD summaries, and manual generation.
- `CONTEXT.md`: ubiquitous language glossary — defines Blueprint, Component, Catalog, Surface, Library, Variant, Experiment, and other domain terms.
- `docs/mcp.md`: Manufact `mcp-use` server guide for agents that need FlightDeck context, resources, prompts, and safe tools.
- `Suggestions.md`: shared suggestion board for agents and contributors.
- `frontend/`: TanStack Start frontend app.
- `frontend/design.md`: unified DESIGN.md-style source for UI plus FlightDeck agentic UX rules.
- `frontend/readme.md`: frontend setup and structure notes.
- `README.md`: this shared contributor and agent context.

Historical context:

- The broader idea came from exploring the Generative UI Global Hackathon starter kit.
- Do not assume starter-kit files exist on `main` unless they are present in this repo.
- Earlier local-only work created design/session context files in another checkout, but `frontend/design.md` is now the main branch design source.

## Scope

The project has two layers of ambition:

- **Hackathon scope (what we're building now):** The three core fluxes from the backend draft — generate Blueprints, critique and manage a Library of Blueprints, and collect usage stats. The frontend event-discovery app (Eventinkerer) is the first product Surface, used as a visible testbed.
- **North star (where this can go):** A full experimentation cockpit with 9+ agents, behavior archetypes, holdout groups, a Reasoning Bank, and role-specific reports.

## Product Direction

The website should demonstrate the process of creating generated interfaces, testing them live, and improving future UIs from evidence.

The ideal visible product flow:

1. User gives a task or prompt.
2. System generates 2 to 4 **Blueprints**, each composing **Components** from the **Catalog**.
3. The **Critique Agent** validates each Blueprint. Passing Blueprints enter the **Library**.
4. An **Experiment** assigns Blueprints as **Variants** on a **Surface**. The system highlights the primary action point it believes the user wants.
5. User interacts with one Variant.
6. System captures first click, first meaningful action, task completion, backtracks, switches, feedback, latency, and accessibility status.
7. System updates the **Reasoning Bank** with structured evidence.
8. System generates reports for Designers/UXRs, Developers, PMs, and QA.

The first **Surface** is the current event-discovery app. For example, FlightDeck can test whether a user should see filters first, recommendation cards first, a quiz first, a map/list first, or a comparison table first.

## System Architecture

FlightDeck should be built as a client/server experimentation system with a persistent database and explicit REST APIs. The architecture must keep Blueprints declarative, measurable, and reviewable.

### Client

The client is the `frontend/` TanStack Start app. It is responsible for rendering trusted **Components**, not arbitrary agent-generated code.

Client responsibilities:

- Render the current event-discovery **Surface**.
- Render **Variants** (Blueprints assigned to an Experiment) using **Components** from the **Catalog**.
- Read and apply `frontend/design.md` for UI tokens, UX rules, accessibility constraints, and experiment behavior.
- Show the active Experiment, assigned Variant, critique status, first-action expectation, and Reasoning Bank preview.
- Capture first-click, first meaningful action, task completion, backtracks, Variant switches, feedback, latency, and accessibility status.
- Respect reduced-motion, keyboard navigation, focus order, and WCAG requirements.
- Send telemetry events to the server through REST endpoints.
- Display role-specific reports for Designers/UXRs, Developers, PMs, and QA.

The client treats **Blueprints** as declarative instructions. Agents may reference Components, props, content, states, and actions from the **Catalog**, but the client owns rendering and safety.

### Server

The server is the orchestration and API layer for FlightDeck. It should expose REST APIs to the frontend and coordinate the future LangChain/LangGraph agent loop.

Server responsibilities:

- Accept UXR studies, tasks, personas/archetypes, Experiments, Blueprints, and telemetry events.
- Run or call the Intent, Variant Generator, DESIGN.md Validator, Critique, Experiment, Telemetry, Reasoning Bank, Report, and Evolution agents.
- Validate generated **Blueprints** against schema, **Catalog**, `frontend/design.md`, accessibility constraints, and experiment isolation rules.
- Manage the **Library** of validated Blueprints.
- Assign Blueprints as **Variants** through A/A, A/B/N, contextual bandit, holdout, or manual-review modes.
- Persist all Experiment definitions, Variant metadata, telemetry events, reports, and Reasoning Bank entries.
- Produce role-specific report payloads.
- Propose reviewable changes to `frontend/design.md` or system prompts when repeated evidence supports a change.

The server should never return hidden chain-of-thought. It may return concise rationale, hypothesis, evidence, and accepted or rejected design rules.

### Database

The database is the system of record for the Library, Experiments, telemetry, reports, and the Reasoning Bank. Use a relational database or document database, but keep schemas explicit and versioned.

Suggested logical collections or tables:

- `blueprints`: the **Library** — validated Blueprints with their Component references, Catalog version, design hash, and critique status.
- `uxr_studies`: research studies, goals, consent scope, owners, and status.
- `uxr_tasks`: task prompts, expected outcomes, target Surfaces, and success criteria.
- `archetypes`: behavior archetypes such as Scanner, Comparer, Explorer, Expert Operator, Uncertain Novice, and Risk-Sensitive User.
- `experiments`: Experiment metadata, hypothesis, assignment strategy, guardrails, and status.
- `variants`: Variant metadata — links a Blueprint to an Experiment and Surface, with expected first action and guardrail result.
- `telemetry_events`: UI rendered, first action, task completion, feedback, backtracks, latency, accessibility status, and Variant switches.
- `reasoning_bank_entries`: structured evidence, observed metrics, proposed design rules, proposed prompt changes, and review status.
- `reports`: role-specific report snapshots for Designer/UXR, Developer, PM, and QA views.
- `design_rule_proposals`: proposed updates to `frontend/design.md`, linked evidence, authoring agent, and approval state.
- `prompt_versions`: system prompt versions, agent prompt versions, linked outcomes, and rollback metadata.

Do not create JSON data files yet unless explicitly requested. When JSON sources are introduced, they should mirror these database concepts with clear schemas and version fields.

### REST APIs

Use these REST endpoints as the initial API contract. They are already part of the FlightDeck design source in `frontend/design.md` and should stay aligned with it.

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

Endpoint intent:

- `POST /uxr/studies`: Create or update a UXR study container with goals, consent scope, and target Surfaces.
- `POST /uxr/tasks`: Register research or product tasks that generated Blueprints should support.
- `POST /uxr/personas`: Register behavior archetypes or task-scoped persona assumptions. Prefer archetypes over demographic personas.
- `POST /experiments`: Create an Experiment with hypothesis, primary metric, guardrails, assignment strategy, and target task.
- `POST /experiments/{id}/variants`: Assign Blueprints from the Library as Variants, with expected first action, Catalog version, design hash, and critique status.
- `POST /events/ui-rendered`: Log that a Surface rendered a Variant, including latency and accessibility status.
- `POST /events/first-action`: Log the user's first click or first meaningful action against the expected action.
- `POST /events/task-completed`: Log task outcome, completion time, backtracks, Variant switches, and success state.
- `POST /events/feedback`: Capture explicit preference, comments, UXR notes, and qualitative feedback.
- `GET /reports/designer/{experiment_id}`: Return first-click maps, path clusters, screenshots, archetype differences, and design-rule recommendations.
- `GET /reports/pm/{experiment_id}`: Return Experiment status, metric direction, uncertainty, risks, and ship/iterate/hold/kill recommendation.
- `GET /reports/dev/{experiment_id}`: Return schema failures, renderer bugs, Catalog mismatches, latency, endpoint failures, and replay links.
- `GET /reports/qa/{experiment_id}`: Return accessibility failures, regression screenshots, broken actions, cross-renderer differences, and WCAG checklist status.

Core telemetry payloads should include:

- `session_id` or consented user identifier.
- `study_id`, `task_id`, `experiment_id`, `variant_id`, and `surface_id`.
- `primary_intent` and `persona_archetype` estimate.
- `first_action_expected` and `first_action_actual`.
- `task_completed`, `backtrack_count`, `variant_switch_count`, and `latency_ms`.
- `a11y_status`, `renderer_version`, `catalog_version`, and `design_md_hash`.
- `consent_scope`.

### Request Flow

The intended request flow:

1. Client submits or receives a user task.
2. Server creates or selects an **Experiment**.
3. LangChain/LangGraph agents generate **Blueprints** and the **Critique Agent** validates them.
4. Validated Blueprints enter the **Library**. The Experiment assigns them as **Variants**.
5. Client renders the assigned Variant on a **Surface** using trusted **Components**.
6. Client posts telemetry events as the user interacts.
7. Server updates metrics and **Reasoning Bank** entries.
8. Reports are generated from stored Experiment evidence.
9. Evolution agent proposes reviewable updates to `frontend/design.md` or prompt versions.

## Agent Loop

Use LangChain/LangGraph agents for the future improvement loop.

Recommended agents:

- **Intent Agent:** Reads the user prompt, task context, and future data sources. Infers goal, risk, and highest-leverage first action.
- **Blueprint Generator Agent:** Generates 2 to 4 controlled **Blueprints** from the **Catalog**.
- **DESIGN.md Validator Agent:** Checks generated Blueprints against `frontend/design.md`.
- **Critique Agent:** Audits schema, Catalog, WCAG, UX Laws, copy clarity, motion, dark-pattern risk, and experiment isolation. Blueprints that pass enter the **Library**.
- **Experiment Agent:** Assigns Blueprints as **Variants** through A/A, A/B/N, contextual bandit, holdout, or manual-review modes.
- **Telemetry Agent:** Logs first click, first meaningful action, completion, backtracks, Variant switches, latency, accessibility signals, and feedback.
- **Reasoning Bank Agent:** Stores structured evidence and proposes reusable learnings. Do not store hidden chain-of-thought.
- **Archetype Agent:** Maps interaction behavior to reversible archetypes such as Scanner, Comparer, Explorer, Expert Operator, Uncertain Novice, and Risk-Sensitive User.
- **Report Agent:** Produces reports tailored to Designers/UXRs, Developers, PMs, and QA.
- **Evolution Agent:** Proposes reviewable changes to `frontend/design.md` and system prompts.

## Reasoning Bank Rules

The Reasoning Bank is a structured evidence store, not hidden chain-of-thought.

It should capture:

- Experiment ID.
- Variant ID.
- Surface ID.
- User task.
- Inferred archetype and confidence.
- Hypothesis.
- Expected first action.
- Actual first action.
- Metrics observed.
- Accessibility findings.
- User preference.
- Outcome summary.
- Proposed design rule.
- Proposed prompt change.
- Accepted, rejected, or needs-review status.

Good evidence entry:

`Comparer users in event-discovery tasks opened filters before recommendation cards in most observed sessions. Next variant should test filter-first with a compact recommendation summary.`

Bad evidence entry:

`The model thought the user wanted filters because...`

Do not expose hidden reasoning in UI, logs, reports, or generated payloads.

## Metrics To Track

Use metrics that indicate whether certain UIs are better for certain behavior archetypes and task contexts.

Core metrics:

- 5-second impression result.
- First click.
- First meaningful action.
- Time to first correct action.
- Task completion.
- Backtrack count.
- Variant switch.
- Clarification request.
- Explicit user preference.
- Rage click or repeated failed action.
- Accessibility status.
- Latency.
- Layout shift.
- User feedback.

Use 5-second tests as fast research probes, not as final proof. Stronger production decisions should use completion, backtracks, holdouts, and guardrail metrics.

## Experiment Variables

Test one or a few controlled variables at a time:

- More animation vs less animation.
- Voice/audio vs no voice/audio.
- Hotter palette vs cooler palette.
- More text vs less text.
- Quiz-first vs table-first.
- Chart-first vs explanation-first.
- Summary card vs form.
- Recommendation-first vs filters-first.
- Progressive disclosure vs dense controls.
- CTA wording.
- Step order.

Use UX Laws as heuristics and hypothesis generators:

- Fitts's Law for target size and proximity.
- Hick's Law for choice complexity.
- Jakob's Law for familiar patterns.
- Miller's Law for grouping.
- Doherty Threshold for responsiveness.
- Goal-Gradient Effect for progress.
- Von Restorff Effect for salience.
- Tesler's Law for irreducible complexity.
- Aesthetic-Usability Effect as a trust signal, not a substitute for success.
- Peak-End Rule for report interpretation.

## Behavior Archetypes

Prefer behavior archetypes over demographic personas.

Initial archetypes:

- **Scanner:** Wants summaries, fast comparison, and clear CTAs.
- **Comparer:** Wants tables, filters, evidence, and tradeoffs.
- **Explorer:** Wants suggestions, branching paths, and discovery.
- **Expert Operator:** Wants dense controls, shortcuts, and minimal explanation.
- **Uncertain Novice:** Wants guided steps, reversible choices, and plain-language help.
- **Risk-Sensitive User:** Wants confirmations, evidence, audit trail, and low-risk defaults.

Archetypes must be probabilistic, reversible, and task-scoped. Do not infer sensitive traits.

## Future Data Sources

Agents will eventually gather information from JSON files, but **do not create those JSON files yet** unless the user explicitly asks.

Likely future JSON sources:

- Design token exports.
- **Catalog** definition (approved Components).
- **Library** index (validated Blueprints).
- Experiment definitions.
- Telemetry events.
- Archetype profiles.
- Reasoning Bank entries.
- Report templates.
- Agent prompt/version registry.

When these files are introduced, keep schemas explicit and versioned.

## Accessibility And Safety

Minimum bar:

- WCAG 2.1 AA.
- Target WCAG 2.2 where practical.
- Keyboard navigation.
- Logical focus order.
- 44px minimum interactive targets.
- Reduced-motion behavior.
- No manipulative urgency or dark patterns.
- No generated arbitrary executable UI code at runtime.
- No sensitive demographic inference.
- No hidden chain-of-thought storage or display.

**Blueprints** must be declarative and rendered through trusted **Components** from the **Catalog**.

## Contributor Workflow

Before making changes:

1. Read `CONTEXT.md` for the ubiquitous language.
2. Read this README.
3. Read `frontend/design.md`.
4. Read `frontend/readme.md` if working on the frontend app.
5. Inspect current git status and recent commits.
6. Keep changes scoped and update this README if the session context changes.

Recommended checks:

```bash
cd backend
uv run pytest

cd frontend
npm install
npm run lint
npm run build
```

Validate the design source:

```bash
npm exec --yes --package=@google/design.md -- design.md lint frontend/design.md
```

If a change updates tokens, experiment rules, UX Laws, agent-loop behavior, or reporting expectations, update `frontend/design.md` and run the design.md linter.

## Session Log

### 2026-05-16

- Created public repo `henrique-simoes/FlightDeck`.
- Made the repo public.
- Existing `frontend/design.md` began as an Eventinkerer brand document.
- Unified `frontend/design.md` into one DESIGN.md-style source containing:
  - frontend UI tokens and brand direction,
  - FlightDeck UX Laws,
  - live A/B/N testing rules,
  - LangChain/LangGraph agent loop,
  - Reasoning Bank rules,
  - behavior archetypes,
  - accessibility constraints,
  - UXR/reporting expectations.
- Validated `frontend/design.md` with `@google/design.md` lint: 0 errors, 0 warnings.
- Added this root README as the shared context for future Codex agents and contributors.
- Established ubiquitous language in `CONTEXT.md`: Blueprint, Component, Catalog, Surface, Library, Variant, Experiment, Critique Agent, Reasoning Bank.
- Updated README to use the resolved terminology consistently.

## Links

- Main repo: `https://github.com/henrique-simoes/FlightDeck`
- Frontend design source: `frontend/design.md`
- Frontend technical README: `frontend/readme.md`
- Google DESIGN.md spec: `https://stitch.withgoogle.com/docs/design-md/specification`
- Google DESIGN.md repo: `https://github.com/google-labs-code/design.md`
