# Python FastAPI for the backend runtime

The backend needs to host LangChain/LangGraph agents, serve REST APIs to the frontend, and coordinate the Blueprint generation/critique/management loop. We chose Python with FastAPI because LangChain and LangGraph are Python-native — running agents in-process avoids the latency and complexity of cross-language RPC. FastAPI gives us async support, automatic OpenAPI docs, and Pydantic validation that aligns naturally with the structured Blueprint payloads the system produces.

## Considered Options

- **TanStack server functions** — would keep frontend and backend in the same TypeScript codebase, but LangChain/LangGraph are Python-first. Bridging via HTTP to a Python agent service adds a hop we can avoid.
- **Node/Hono API** — same TypeScript-alignment benefit, same Python-bridging drawback.
- **Python/FastAPI** — chosen. Agents run in-process, Pydantic models double as API schemas, and the async runtime handles concurrent Blueprint generation and telemetry ingestion well.
