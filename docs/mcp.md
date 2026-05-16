# FlightDeck MCP Server

FlightDeck ships a Manufact `mcp-use` server so other agents can inspect the project context, read the design source, query the experiment state, critique Blueprint payloads, and intentionally generate new persona Blueprints through MCP.

The server lives in `backend/flightdeck/mcp_server.py` and is exposed through:

```bash
cd backend
uv run flightdeck mcp
```

or:

```bash
cd backend
uv run flightdeck-mcp
```

## Transports

Run the server over stdio for local coding agents:

```bash
cd backend
uv run flightdeck mcp --transport stdio
```

Example client configuration from the repo root:

```json
{
  "mcpServers": {
    "flightdeck": {
      "command": "uv",
      "args": ["--directory", "backend", "run", "flightdeck", "mcp", "--transport", "stdio"]
    }
  }
}
```

Run the server over streamable HTTP for browser clients, hosted agents, or the Manufact Inspector:

```bash
cd backend
uv run flightdeck mcp --transport streamable-http --host 127.0.0.1 --port 8010 --debug
```

Debug mode enables the mcp-use development endpoints:

- MCP endpoint: `http://127.0.0.1:8010/mcp`
- Inspector: `http://127.0.0.1:8010/inspector`
- OpenMCP discovery: `http://127.0.0.1:8010/openmcp.json`
- Docs: `http://127.0.0.1:8010/docs`

You can also inspect the server with:

```bash
npx @mcp-use/inspector --url http://127.0.0.1:8010/mcp
```

## Resources

Resources are read-only source-of-truth documents for contributor agents:

- `flightdeck://readme`
- `flightdeck://context`
- `flightdeck://design`
- `flightdeck://suggestions`
- `flightdeck://backend_readme`
- `flightdeck://persona/{persona_id}`

Agents should read `flightdeck://readme`, `flightdeck://context`, `flightdeck://design`, and `flightdeck://suggestions` before making repo changes.

## Prompts

- `flightdeck_contributor_brief`: Minimal pre-work brief for contributors.
- `flightdeck_mcp_usage`: Guidance for using the MCP server safely.

## Tools

- `get_project_snapshot`: Returns docs, personas, active Experiment, recent Blueprints, telemetry, and Reasoning Bank status.
- `get_experiment_assignment`: Returns the active Variant and Blueprint assignment for a persona/archetype.
- `list_blueprint_library`: Lists recent stored Blueprints and critique results.
- `summarize_telemetry`: Aggregates telemetry counts and top interaction targets.
- `critique_blueprint_payload`: Validates and critiques a BlueprintSpec-shaped payload without storing it.
- `generate_persona_blueprint`: Generates, critiques, stores, and activates a new Blueprint Variant.

`generate_persona_blueprint` writes to SQLite and may call the LangGraph/CopilotKit generation path when `OPENAI_API_KEY` is configured. If `allow_fallback` is true, it uses the deterministic local generator when the agent path is unavailable.

## Environment

- `FLIGHTDECK_DB_PATH`: Optional SQLite path. Defaults to `backend/data/flightdeck.db`.
- `OPENAI_API_KEY`: Required for LangGraph/CopilotKit Blueprint generation.
- `FLIGHTDECK_AGENT_MODEL`: Optional model name for the Blueprint Generator Agent.
- `FLIGHTDECK_MCP_TRANSPORT`: Optional default transport for `flightdeck-mcp`.
- `FLIGHTDECK_MCP_HOST`: Optional default host for `flightdeck-mcp`.
- `FLIGHTDECK_MCP_PORT`: Optional default port for `flightdeck-mcp`.
- `FLIGHTDECK_MCP_DEBUG=1`: Enables debug mode for `flightdeck-mcp`.

## Safety Rules

- Treat resources as source of truth.
- Prefer read-only tools before mutation.
- Run `critique_blueprint_payload` before storing externally generated Blueprints.
- Call `generate_persona_blueprint` only when the user wants a new activated Variant.
- Do not expose hidden chain-of-thought in tool results, prompts, reports, or Reasoning Bank entries.
- Do not infer sensitive demographic traits from persona/archetype data.
