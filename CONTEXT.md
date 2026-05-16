# FlightDeck

An agentic system that generates, critiques, manages, and continuously improves declarative user interfaces through structured experimentation and evidence.

## Language

**Blueprint**:
A declarative payload that an agent generates describing what UI to render. It references Components from the Catalog, carries a hypothesis, and is the atomic unit stored in the Library.
_Avoid_: component (when referring to the generated artifact), layout, spec, view

**Component**:
A trusted, pre-built frontend element in the Catalog (e.g., `EventCard`, `FilterCard`). Components are hand-coded and approved — agents never create them, only reference them in Blueprints.
_Avoid_: widget, element, block

**Catalog**:
The approved set of Components that agents may reference when generating Blueprints. Nothing outside the Catalog can appear in a Blueprint.
_Avoid_: component library (when referring to the approved set of renderable elements)

**Surface**:
A named zone of the UI where generated content can appear (e.g., "event discovery", "checkout flow"). A Surface is a slot, not content.
_Avoid_: page, screen, view

**Library**:
The collection of validated Blueprints available for selection and deployment. A Blueprint enters the Library only after passing the Critique Agent.
_Avoid_: component library (when referring to the store of generated artifacts), registry

**Variant**:
A Blueprint that has been assigned to an Experiment and is being served on a Surface to collect evidence. Not all Blueprints are Variants — some may be drafts or rejected by critique.
_Avoid_: version, option, alternative

**Experiment**:
A structured test that serves one or more Variants on a Surface to measure which Blueprint better serves a hypothesis.
_Avoid_: test, A/B test (as a noun for the container)

**Critique Agent**:
The agent that validates a Blueprint against schema, Catalog, design rules, accessibility, UX heuristics, and experiment isolation before it enters the Library.
_Avoid_: validator, reviewer, linter

**Reasoning Bank**:
A structured evidence store that captures experiment outcomes, observed metrics, proposed design rules, and learnings. It stores observable evidence, never hidden chain-of-thought.
_Avoid_: knowledge base, memory, reasoning log

## Relationships

- An agent generates a **Blueprint** that composes **Components** from the **Catalog**
- The **Critique Agent** validates a **Blueprint** before it enters the **Library**
- When an **Experiment** runs, a **Blueprint** from the **Library** becomes a **Variant**
- A **Variant** is served on a **Surface** to collect evidence
- Evidence from a **Variant** is stored in the **Reasoning Bank**
- The **Reasoning Bank** informs future **Blueprint** generation

## Example dialogue

> **Dev:** "When an agent generates a new **Blueprint**, does it go directly to the **Library**?"
> **Domain expert:** "No — a **Blueprint** must pass the **Critique Agent** first. Only validated Blueprints enter the **Library**."
>
> **Dev:** "So when does a **Blueprint** become a **Variant**?"
> **Domain expert:** "When it's assigned to an **Experiment** and deployed on a **Surface** to collect real user evidence."

## Flagged ambiguities

- "component" was used to mean both the generated artifact and the trusted frontend element — resolved: the generated artifact is a **Blueprint**, the trusted frontend element is a **Component**.
- "component library" was used to mean both the approved set of renderable elements and the store of generated artifacts — resolved: the approved set is the **Catalog**, the store of generated artifacts is the **Library**.
