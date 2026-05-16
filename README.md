# GenUI FlightDeck Sessions Context

Last updated: 2026-05-16

This README is the shared session context for Codex agents and contributors working on **GenUI FlightDeck**. Read this before changing the repo. The goal is for every contributor session to start from the same product intent, design rules, and collaboration protocol.

## What This Project Is

GenUI FlightDeck is a website and agentic system for generating, validating, live-testing, and improving generated user interfaces.

The core idea is **live experimentation for GenUIs**:

1. A user prompt arrives.
2. Agents infer the user's goal and highest-leverage first action.
3. Agents generate multiple interface variants from an approved catalog.
4. A critique agent checks schema, catalog, accessibility, UX heuristics, and design compliance.
5. The website shows one or more variants and logs interaction signals.
6. The system writes structured experiment learnings into a Reasoning Bank.
7. Future UIs improve from those learnings.
8. Agents may propose improvements to `frontend/design.md` and possibly the system prompt, but changes must be reviewable and auditable.

This is not meant to become a generic GenUI demo. It is an experimentation cockpit for generated interfaces: every generated UI should carry a hypothesis, pass guardrails, produce measurable evidence, and improve future UI decisions.

## Source Of Truth

Use this hierarchy:

1. **`frontend/design.md`** is the single source of truth for the frontend UI, FlightDeck UX Laws, agentic loop, live testing model, Reasoning Bank, and reporting rules.
2. **`README.md`** is the shared session context for agents and contributors.
3. **`frontend/readme.md`** is the technical README for running and understanding the current frontend app.

The current `frontend/design.md` merges two layers:

- **UI layer:** Eventinkerer-style frontend identity with violet-to-cyan gradient, soft rounded controls, clear metadata hierarchy, event filters, and responsive event cards.
- **FlightDeck layer:** UX-law critique, A/B/N testing, behavior archetypes, LangChain/LangGraph agent loop, Reasoning Bank, UXR endpoints, accessibility gates, and role-specific reports.

Whenever the product direction changes, update this README. Whenever the design system, UI rules, or agentic testing rules change, update `frontend/design.md`.

## Current Main Branch State

The public repo is:

`https://github.com/henrique-simoes/FlightDeck`

Current main branch contains:

- `frontend/`: TanStack Start frontend app.
- `frontend/design.md`: unified DESIGN.md-style source for UI plus FlightDeck agentic UX rules.
- `frontend/readme.md`: frontend setup and structure notes.
- `README.md`: this shared contributor and agent context.

Historical context:

- The broader idea came from exploring the Generative UI Global Hackathon starter kit.
- Do not assume starter-kit files exist on `main` unless they are present in this repo.
- Earlier local-only work created design/session context files in another checkout, but `frontend/design.md` is now the main branch design source.

## Product Direction

The website should demonstrate the process of creating generated interfaces, testing them live, and improving future UIs from evidence.

The ideal visible product flow:

1. User gives a task or prompt.
2. System generates 2 to 4 UI variants.
3. System highlights the primary action point it believes the user wants.
4. User interacts with one variant.
5. System captures first click, first meaningful action, task completion, backtracks, switches, feedback, latency, and accessibility status.
6. System updates a Reasoning Bank with structured evidence.
7. System generates reports for Designers/UXRs, Developers, PMs, and QA.

The first product surface can use the current event-discovery app as the testbed. For example, FlightDeck can test whether a user should see filters first, recommendation cards first, a quiz first, a map/list first, or a comparison table first.

## Agent Loop

Use LangChain/LangGraph agents for the future improvement loop.

Recommended agents:

- **Intent Agent:** Reads the user prompt, task context, and future data sources. Infers goal, risk, and highest-leverage first action.
- **Variant Generator Agent:** Generates 2 to 4 controlled UI variants from an approved catalog.
- **DESIGN.md Validator Agent:** Checks generated UI against `frontend/design.md`.
- **Critique Agent:** Audits schema, catalog, WCAG, UX Laws, copy clarity, motion, dark-pattern risk, and experiment isolation.
- **Experiment Agent:** Assigns A/A, A/B/N, contextual bandit, holdout, or manual-review modes.
- **Telemetry Agent:** Logs first click, first meaningful action, completion, backtracks, variant switches, latency, accessibility signals, and feedback.
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
- Component catalog.
- UI variant registry.
- Experiment definitions.
- Telemetry events.
- Persona/archetype profiles.
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

Generated UIs should be declarative and rendered through trusted frontend components.

## Contributor Workflow

Before making changes:

1. Read this README.
2. Read `frontend/design.md`.
3. Read `frontend/readme.md` if working on the frontend app.
4. Inspect current git status and recent commits.
5. Keep changes scoped and update this README if the session context changes.

Recommended checks:

```bash
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

## Links

- Main repo: `https://github.com/henrique-simoes/FlightDeck`
- Frontend design source: `frontend/design.md`
- Frontend technical README: `frontend/readme.md`
- Google DESIGN.md spec: `https://stitch.withgoogle.com/docs/design-md/specification`
- Google DESIGN.md repo: `https://github.com/google-labs-code/design.md`
