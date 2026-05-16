# FlightDeck

An agentic system that generates, critiques, manages, and continuously improves declarative user interfaces through structured experimentation and evidence.

## Language

**Blueprint**:
A declarative payload that an agent generates describing what UI to render for a Surface. It contains a flat list of Component references with ID-based parent-child relationships (following the A2UI adjacency-list model), carries a hypothesis, and is the unit stored in the Library. A single Blueprint is self-contained — it describes a complete experience for one Surface.
_Avoid_: component (when referring to the generated artifact), layout, spec, view, composition

**Component**:
A trusted, pre-built frontend element in the Catalog (e.g., `EventCard`, `FilterCard`). Components are hand-coded and approved — agents never create them, only reference them in Blueprints.
_Avoid_: widget, element, block

**Catalog**:
The approved set of Components that agents may reference when generating Blueprints, expressed as an A2UI JSON Schema. Stored as immutable versioned snapshots — agents create new versions, never mutate existing ones. Each Blueprint records which Catalog version it was validated against.
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

### North-star terms

**Project**:
A self-contained experimentation scope that owns its own Catalog, Library, Surfaces, Experiments, and Reasoning Bank. In the hackathon, there is one implicit Project (`default`). In the future, each Project is independent.
_Avoid_: workspace, tenant, app

**Client**:
An organization or individual that owns one or more Projects. Not implemented in the hackathon — all work belongs to a single implicit Client.
_Avoid_: customer, user, account

## Relationships

- A **Client** owns one or more **Projects** (north star; hackathon uses one implicit Project)
- A **Project** owns a **Catalog**, a **Library**, **Surfaces**, **Experiments**, and a **Reasoning Bank**
- An agent generates a **Blueprint** — a flat list of **Component** references targeting a **Surface**
- A **Blueprint** records which **Catalog** version it was validated against
- The **Critique Agent** validates a **Blueprint** against the active **Catalog** version before it enters the **Library**
- When an **Experiment** runs, a **Blueprint** from the **Library** becomes a **Variant**
- A **Variant** is served on a **Surface** to collect evidence
- Evidence from a **Variant** is stored in the **Reasoning Bank**
- The **Reasoning Bank** informs future **Blueprint** generation and **Catalog** evolution

## Example dialogue

> **Dev:** "When an agent generates a new **Blueprint**, does it go directly to the **Library**?"
> **Domain expert:** "No — a **Blueprint** must pass the **Critique Agent** first. Only validated Blueprints enter the **Library**."
>
> **Dev:** "So when does a **Blueprint** become a **Variant**?"
> **Domain expert:** "When it's assigned to an **Experiment** and deployed on a **Surface** to collect real user evidence."
>
> **Dev:** "What's inside a Blueprint? Is it one Component or many?"
> **Domain expert:** "It's a flat list of **Component** references — each with an ID. Parent Components reference their children by ID. The whole list targets one **Surface**."

## Flagged ambiguities

- "component" was used to mean both the generated artifact and the trusted frontend element — resolved: the generated artifact is a **Blueprint**, the trusted frontend element is a **Component**.
- "component library" was used to mean both the approved set of renderable elements and the store of generated artifacts — resolved: the approved set is the **Catalog**, the store of generated artifacts is the **Library**.
