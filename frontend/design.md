---
version: alpha
name: GenUI FlightDeck
description: Unified design source for the FlightDeck frontend UI, adaptive GenUI experiments, UX-law critique, Reasoning Bank learning, and LangChain agent loops.
colors:
  primary: "#8851EB"
  primary-hover: "#7330D4"
  accent: "#00D6E2"
  accent-hover: "#00BDCA"
  background: "#F9FAFD"
  foreground: "#0E0F23"
  surface: "#FFFFFF"
  surface-muted: "#F0F1FC"
  secondary: "#EEECFF"
  border: "#D5D6E8"
  muted-foreground: "#54566C"
  on-primary: "#FFFFFF"
  success: "#007A33"
  warning: "#D78D00"
  error: "#D73337"
  hot-variant: "#EC4F27"
  cool-variant: "#0083D8"
  data-blue: "#0076C1"
  data-orange: "#D46600"
  focus: "#8851EB"
typography:
  display:
    fontFamily: system-ui
    fontSize: 3rem
    fontWeight: 800
    lineHeight: 1.05
    letterSpacing: 0px
  headline-lg:
    fontFamily: system-ui
    fontSize: 2rem
    fontWeight: 750
    lineHeight: 1.15
    letterSpacing: 0px
  headline-md:
    fontFamily: system-ui
    fontSize: 1.5rem
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: 0px
  title-md:
    fontFamily: system-ui
    fontSize: 1.125rem
    fontWeight: 700
    lineHeight: 1.3
    letterSpacing: 0px
  body-lg:
    fontFamily: system-ui
    fontSize: 1.125rem
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: 0px
  body-md:
    fontFamily: system-ui
    fontSize: 1rem
    fontWeight: 400
    lineHeight: 1.55
    letterSpacing: 0px
  body-sm:
    fontFamily: system-ui
    fontSize: 0.875rem
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: 0px
  label-lg:
    fontFamily: system-ui
    fontSize: 0.875rem
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: 0px
  label-sm:
    fontFamily: system-ui
    fontSize: 0.75rem
    fontWeight: 650
    lineHeight: 1.2
    letterSpacing: 0px
  telemetry:
    fontFamily: ui-monospace
    fontSize: 0.75rem
    fontWeight: 500
    lineHeight: 1.35
    letterSpacing: 0px
rounded:
  none: 0px
  sm: 0.5rem
  md: 0.875rem
  lg: 1.25rem
  xl: 1.75rem
  2xl: 2rem
  full: 9999px
spacing:
  xs: 0.25rem
  sm: 0.5rem
  md: 1rem
  lg: 1.5rem
  xl: 2rem
  2xl: 3rem
  3xl: 4rem
  gutter: 1.5rem
components:
  app-shell:
    backgroundColor: "{colors.background}"
    textColor: "{colors.foreground}"
    typography: "{typography.body-md}"
    rounded: "{rounded.none}"
    padding: 1.5rem
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label-lg}"
    rounded: "{rounded.lg}"
    padding: 0.875rem
    height: 44px
  button-primary-hover:
    backgroundColor: "{colors.primary-hover}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label-lg}"
    rounded: "{rounded.lg}"
    padding: 0.875rem
    height: 44px
  button-gradient:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.foreground}"
    typography: "{typography.label-lg}"
    rounded: "{rounded.xl}"
    padding: 0.875rem
    height: 44px
  button-gradient-hover:
    backgroundColor: "{colors.accent-hover}"
    textColor: "{colors.foreground}"
    typography: "{typography.label-lg}"
    rounded: "{rounded.xl}"
    padding: 0.875rem
    height: 44px
  navbar:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.foreground}"
    typography: "{typography.body-md}"
    rounded: "{rounded.none}"
    padding: 1rem
  event-card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.foreground}"
    typography: "{typography.body-md}"
    rounded: "{rounded.2xl}"
    padding: 1rem
  filter-card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.foreground}"
    typography: "{typography.body-md}"
    rounded: "{rounded.2xl}"
    padding: 1.25rem
  badge:
    backgroundColor: "{colors.secondary}"
    textColor: "{colors.foreground}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.full}"
    padding: 0.5rem
  telemetry-pill:
    backgroundColor: "{colors.data-blue}"
    textColor: "{colors.on-primary}"
    typography: "{typography.telemetry}"
    rounded: "{rounded.full}"
    padding: 0.5rem
  insight-pill:
    backgroundColor: "{colors.data-orange}"
    textColor: "{colors.foreground}"
    typography: "{typography.telemetry}"
    rounded: "{rounded.full}"
    padding: 0.5rem
  experiment-card:
    backgroundColor: "{colors.surface-muted}"
    textColor: "{colors.foreground}"
    typography: "{typography.body-md}"
    rounded: "{rounded.lg}"
    padding: 1rem
  variant-card-hot:
    backgroundColor: "{colors.hot-variant}"
    textColor: "{colors.foreground}"
    typography: "{typography.body-md}"
    rounded: "{rounded.lg}"
    padding: 1rem
  variant-card-cool:
    backgroundColor: "{colors.cool-variant}"
    textColor: "{colors.foreground}"
    typography: "{typography.body-md}"
    rounded: "{rounded.lg}"
    padding: 1rem
  critique-panel:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.foreground}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.lg}"
    padding: 1rem
  success-banner:
    backgroundColor: "{colors.success}"
    textColor: "{colors.on-primary}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: 0.875rem
  warning-banner:
    backgroundColor: "{colors.warning}"
    textColor: "{colors.foreground}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: 0.875rem
  error-banner:
    backgroundColor: "{colors.error}"
    textColor: "{colors.on-primary}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: 0.875rem
  divider-line:
    backgroundColor: "{colors.border}"
    textColor: "{colors.foreground}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.none}"
    height: 1px
  muted-metadata:
    backgroundColor: "{colors.surface-muted}"
    textColor: "{colors.muted-foreground}"
    typography: "{typography.telemetry}"
    rounded: "{rounded.sm}"
    padding: 0.5rem
  focus-target:
    backgroundColor: "{colors.focus}"
    textColor: "{colors.on-primary}"
    typography: "{typography.label-lg}"
    rounded: "{rounded.lg}"
    padding: 0.875rem
---

# GenUI FlightDeck Design Source

## Overview

This file is the single `design.md` source for the frontend on `main`.

The frontend UI rules come from the existing Eventinkerer design direction: a modern, vibrant event-discovery interface with generous spacing, soft curves, a violet to cyan signature gradient, strong title hierarchy, muted metadata, and clear purchase or filter actions.

The product and experimentation rules come from GenUI FlightDeck: a system for generating, validating, live-testing, and improving generated user interfaces through a LangChain/LangGraph agent loop, a Reasoning Bank, UX-law critique, accessibility gates, and role-specific reports.

Treat this file as a two-layer contract:

1. **UI contract:** The frontend renders with these tokens, layout principles, component rules, tone, and interaction patterns.
2. **Agentic UX contract:** Agents generate and critique UIs according to the experiment loop, UX laws, metrics, accessibility requirements, and Reasoning Bank rules in this file.

The current event UI is the first product surface and testbed. It should still feel close, energetic, trustworthy, and clear. FlightDeck adds an evidence layer above it: every generated variant should explain what it is testing, which user action it expects, how it performed, and what future UI rule should change.

## Colors

Use the frontend palette as the UI source of truth.

- **Primary:** Vibrant violet for CTAs, logo emphasis, active controls, selected filters, and primary agent actions.
- **Accent:** Electric cyan for highlights, notifications, comparison emphasis, and the end of the signature gradient.
- **Background:** Near-white with a slight violet tint for the app shell.
- **Foreground:** Near-black with a violet undertone for main content.
- **Muted and Secondary:** Soft violet-tinted surfaces for chips, badges, filters, skeletons, metadata containers, and inactive controls.
- **Hot Variant:** Used only when an experiment intentionally tests warmer energy, urgency, animation, or expressive copy.
- **Cool Variant:** Used only when an experiment intentionally tests calmer clarity, reduced motion, analytical comparison, or low-pressure guidance.
- **Data Blue and Data Orange:** Reserved for telemetry and UXR insights. Do not use them as decorative brand colors.

The signature gradient is violet to cyan. Use it for the logo tile, primary CTA emphasis, event covers, and selected experiment highlights. Do not use gradient styling to bias an A/B test unless color or emotional intensity is the explicit tested variable.

When testing UI variants, isolate variables:

- If color temperature is under test, keep copy, layout, and motion stable.
- If motion is under test, keep color, copy, and layout stable.
- If text density is under test, keep action order and component hierarchy stable.

## Typography

Use system sans-serif typography for the frontend. It should feel fast, native, and legible.

Weights:

- 400 for body text and helper copy.
- 600 to 700 for section titles, subtitles, event names, and cards.
- 750 to 800 for dashboard-level or hero-level titles only.

Use telemetry typography for experiment IDs, event names, variant IDs, A2UI versions, DESIGN.md hashes, timestamps, and replay traces.

Copy tone:

- For the event UI, use clear neutral Spanish or English depending on the product locale. Existing Spanish CTA style may use concise imperatives such as "Comprar entradas" and "Aplicar filtros".
- For FlightDeck surfaces, use precise operational language: "First action", "Variant", "Critique passed", "Holdout", "Reasoning Bank", "Replay trace".
- Do not expose hidden chain-of-thought. Store and show structured rationale and evidence only.

## Layout

The current frontend layout pattern remains valid:

- Sticky top navbar with brand on the left and user/account controls on the right.
- Main page grid with filters on the left and event or generated surfaces on the right.
- On mobile, filters move above the list or into a controlled sheet.
- Cards use generous spacing, soft curves, clear badges, icon metadata, and direct CTAs.

FlightDeck adds these operational zones:

1. **Generated Surface:** The user-facing UI being tested.
2. **Variant Rail:** The available UI variants, assignment mode, and active hypothesis.
3. **Critique Panel:** Schema, catalog, DESIGN.md, accessibility, UX-law, and policy findings.
4. **Reasoning Bank Preview:** Structured learnings and accepted/rejected design rules.
5. **Report Workspace:** Designer/UXR, Developer, PM, and QA report views.

The experiment unit is the smallest meaningful decision point, not the whole page. Prefer testing:

- Quiz-first vs table-first.
- Recommendation-first vs filters-first.
- Summary card vs form.
- Chart-first vs explanation-first.
- CTA wording.
- Step order.
- Progressive disclosure vs dense controls.
- More animation vs less animation.
- Voice/audio vs no voice/audio.
- Hotter palette vs cooler palette.
- More text vs less text.

Every generated variant must declare:

- `experiment_id`
- `variant_id`
- `surface_id`
- `primary_intent`
- `highest_leverage_action`
- `first_action_expected`
- `hypothesis`
- `persona_archetype`
- `catalog_version`
- `design_md_hash`
- `guardrail_status`

## Elevation & Depth

The frontend can use soft shadows and translucent blur for the navbar, filter cards, event cards, and active overlays. Elevation should support hierarchy without making the page feel heavy.

Use depth for:

- Sticky navigation and filters.
- Active selected variants.
- Expanded critique or report panels.
- Current replay step.
- Human approval gates.

Avoid nested card stacks. A repeated item may be a card; a whole section should not be a floating card inside another floating card. Keep the UI energetic but operationally clear.

## Shapes

Use soft curves as a core UI signature.

- Base cards and filters should use large radii.
- Buttons and badges should feel friendly and rounded.
- Pills are reserved for filters, tags, telemetry, and insight labels.
- Interactive targets must be at least 44px tall.

Motion should be purposeful:

- Default transitions should be subtle and under 200ms.
- Motion-heavy variants must be explicitly marked as experiment variants.
- Always respect reduced-motion preferences.
- Never use motion to pressure action, hide latency, or obscure important information.

## Components

### Frontend UI Components

The following components are source-of-truth UI patterns for the current frontend:

- **Navbar:** Sticky, translucent blur, brand mark with violet to cyan treatment, user avatar or account control on the right.
- **Filters:** Sticky card with rounded chips, checkboxes, range/price slider, and a clear apply action.
- **Event Card:** Gradient cover, clear event title, category badge, metadata with icons, and primary CTA.
- **Badge/Chip:** Rounded, compact, readable, and useful for categories, state, or filters.
- **Primary CTA:** High-contrast, direct, action-oriented, and placed near the strongest user intent.

### FlightDeck Components

Agents may generate only declarative UI payloads that reference trusted components. Do not allow arbitrary executable frontend code at runtime.

Approved FlightDeck surface patterns:

- `intent-summary`: Inferred user goal, confidence, and first-action hypothesis.
- `variant-switcher`: User-visible choice among generated variants when allowed.
- `primary-action-surface`: The highest-leverage action point the AI believes the user wants.
- `first-click-zone`: Instrumented region for first-click and first-action tests.
- `experiment-card`: Hypothesis, variant ID, assignment method, and guardrail state.
- `a2ui-surface-frame`: Trusted renderer boundary for A2UI-style payloads.
- `critique-panel`: Schema, catalog, accessibility, UX-law, security, and ethics findings.
- `reasoning-bank-panel`: Structured evidence, design rules, rejected hypotheses, and learned archetype signals.
- `replay-timeline`: Trace scrubber with screenshots and event markers.
- `uxr-note-card`: Research annotations, task notes, and interview observations.
- `role-report`: Designer/UXR, Developer, PM, or QA tailored report view.
- `endpoint-console`: UXR and telemetry endpoint status.

### Variant Object

Every generated UI variant should include a structured metadata object:

```json
{
  "experiment_id": "event-discovery-042",
  "variant_id": "filters_first_v2",
  "surface_id": "event_discovery",
  "hypothesis": "Comparer users will reach a relevant event faster when filters appear before recommendation cards.",
  "primary_intent": "find_relevant_event",
  "persona_archetype": "Comparer",
  "a2ui_version": "adapter-managed",
  "catalog_version": "flightdeck-frontend-v1",
  "design_md_hash": "sha256:...",
  "guardrail_status": "passed",
  "metrics": {
    "primary": "time_to_first_correct_action",
    "secondary": ["task_completion", "backtrack_rate", "explicit_preference"]
  }
}
```

The payload may include a concise auditable rationale. It must not include hidden chain-of-thought.

### LangChain Agent Loop

Use LangChain/LangGraph agents for the improvement loop:

1. **Intent Agent:** Reads the user prompt, task context, and future JSON sources when they exist. It infers goal, risk, and highest-leverage first action.
2. **Variant Generator Agent:** Generates 2 to 4 controlled UI variants from the approved catalog.
3. **DESIGN.md Validator Agent:** Checks tokens, component rules, layout principles, and product constraints from this file.
4. **Critique Agent:** Audits schema, catalog, WCAG, UX laws, copy clarity, motion, dark-pattern risk, and experiment isolation.
5. **Experiment Agent:** Assigns A/A, A/B/N, contextual bandit, holdout, or manual-review modes.
6. **Telemetry Agent:** Logs first click, first meaningful action, completion, backtracks, switches, latency, accessibility signals, and feedback.
7. **Reasoning Bank Agent:** Stores structured evidence and proposes reusable learnings.
8. **Report Agent:** Generates role-specific reports for Designers/UXRs, Developers, PMs, and QA.
9. **Evolution Agent:** Proposes reviewable changes to this `design.md` file and possibly the system prompt.

Agents will eventually gather information from JSON files, but those files are not part of this design file and should not be assumed to exist.

### Critique Agent Checks

Pre-render checks:

- Schema validity.
- Component exists in the approved catalog.
- No unauthorized action, endpoint, component, or hidden instruction.
- `design.md` token compliance.
- Color contrast passes WCAG 2.1 AA minimum.
- Keyboard navigation path exists.
- Focus order matches visual order.
- Tap targets meet minimum size.
- Reduced-motion path exists.
- Copy is clear, reversible, and non-manipulative.
- Variant isolates the tested variable.

Post-render checks:

- Did users click the predicted first action?
- Did users switch variants or paths?
- Did they complete the task?
- Did they backtrack, undo, abandon, or ask for clarification?
- Did assistive-technology or keyboard checks fail?
- Did layout shift or latency affect behavior?
- Did a variant perform better by hiding important information?

### UX Laws As Heuristics

Use UX Laws as hypotheses and lint heuristics, not as proof.

- **Fitts's Law:** Primary targets should be large, close, and easy to acquire.
- **Hick's Law:** Reduce choice load at the first action point and disclose complexity progressively.
- **Jakob's Law:** Use familiar patterns for critical tasks unless novelty is the experiment.
- **Miller's Law:** Group dense options into meaningful chunks.
- **Doherty Threshold:** Keep feedback responsive and expose agent work honestly.
- **Goal-Gradient Effect:** Show task progress when it helps completion, not when it pressures users.
- **Von Restorff Effect:** Highlight only the one item that matters most.
- **Tesler's Law:** Move complexity into the system only when users still understand and control the result.
- **Aesthetic-Usability Effect:** Visual polish can support trust but cannot override accessibility or task success.
- **Peak-End Rule:** Reports should capture the hardest moment and final outcome of each flow.

### Behavior Archetypes

Use behavior archetypes, not sensitive demographic personas.

- **Scanner:** Wants summaries and clear CTAs.
- **Comparer:** Wants filters, tables, evidence, and tradeoffs.
- **Explorer:** Wants suggestions and branching paths.
- **Expert Operator:** Wants dense controls and shortcuts.
- **Uncertain Novice:** Wants guided steps and reversible choices.
- **Risk-Sensitive User:** Wants confirmations, evidence, and auditability.

Archetypes are probabilistic, reversible, and task-scoped. A user may be a Scanner in one task and a Comparer in another.

### Reasoning Bank

The Reasoning Bank stores structured evidence, not hidden chain-of-thought.

Capture:

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

Good entry:

`Comparer users in event-discovery tasks opened filters before recommendation cards in most observed sessions. Next variant should test filter-first with a compact recommendation summary.`

Bad entry:

`The model thought the user wanted filters because...`

### Metrics

Track:

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

Use 5-second tests as rapid research probes, not final proof. Production decisions need completion, backtracks, holdouts, and guardrail metrics.

### Reports

Designer and UXR reports show first-click maps, path clusters, screenshots, qualitative notes, archetype differences, and recommended design-rule changes.

Developer reports show schema failures, renderer bugs, catalog mismatches, state-sync issues, latency by component, endpoint failures, and replay links.

PM reports show experiment status, metric direction, uncertainty, guardrail risks, adoption impact, cost per generated surface, and recommendation to ship, iterate, hold, or kill.

QA reports show accessibility failures, regression screenshots, broken actions, cross-renderer differences, replayable traces, and WCAG checklist status.

### Future UXR Endpoints

The product may later expose:

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

## Do's and Don'ts

- Do keep this file as the single design source for frontend UI plus FlightDeck experimentation rules.
- Do preserve the violet to cyan frontend identity unless a deliberate experiment tests another palette.
- Do validate generated UI against this file, schema rules, catalog rules, and WCAG 2.1 AA minimum.
- Do target WCAG 2.2 when practical.
- Do isolate experiment variables whenever possible.
- Do run A/A tests before trusting A/B/N tests.
- Do keep holdout groups for production adaptation.
- Do connect learnings to reversible behavior archetypes.
- Do make prompt and design-rule evolution reviewable.
- Do keep JSON data sources explicit and versioned when they are introduced later.
- Don't create arbitrary executable UI code at runtime.
- Don't expose hidden chain-of-thought.
- Don't infer sensitive demographic traits.
- Don't declare winners from a 5-second impression probe alone.
- Don't optimize clicks at the expense of comprehension, consent, reversibility, or accessibility.
- Don't bury accessibility failures in developer-only reports.
- Don't combine motion, color, copy, layout, and voice changes in a single test unless the combined interaction is the explicit hypothesis.
