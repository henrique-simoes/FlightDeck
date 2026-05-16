This monorepo is a an experimentation on gen UI. 
The idea is to build a service that can generate and manage multiple UI components and present them to the user, collect stats and have an angent to critique it and propose changes in a continuous improvement loop.

We have three basic fluxes:
1. generate UI components
    1.1. Generate component from context (the input is the system prompt, DESIGN.md, optimally the old component(s) and stats if any, component critique, if any)
    1.2. Critique agent (the input is the system prompt, DESIGN.md, the component). If the component passes, it goes to the components library, if not it loops back to 1.1 
2. Manage UI components
    2.1. Agent that selects from the components library to build the user interface
    2.2 It can add new component requests in a queueu, it can signal components to be retired
3. collect stats from usage

