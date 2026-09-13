# notes-mcp

A minimal MCP (Model Context Protocol) server and client, built to learn the protocol from the ground up.

Manages plain-text notes on disk and exposes them via MCP's three core primitives: **resources**, **tools**, and **prompts**. Includes an interactive CLI agent that uses Gemini's function calling to decide which MCP tools to invoke based on natural language.

## Why

Built as a hands-on exercise to understand MCP architecture before reaching for higher-level agent frameworks. Every piece — server, transport, client, LLM integration — is implemented manually(with a built of help from Claude).

## Architecture

```
┌──────────────────┐         stdio           ┌──────────────────┐
│  agent_client.py │◄──────────────────────► │ notes_server.py  │
│                  │   JSON-RPC (MCP)        │                  │
│  - discovers     │                         │  Resources:      │
│    capabilities  │                         │  - notes://list  │
│  - sends to      │                         │                  │
│    Gemini        │                         │  Tools:          │
│  - executes      │                         │  - create_note   │
│    tool calls    │                         │  - read_note     │
└────────┬─────────┘                         │  - delete_note   │
         │                                   │  - search_notes  │
         ▼                                   │                  │
  ┌─────────────┐                            │  Prompts:        │
  │  Gemini API │                            │  - summarize_note│
  └─────────────┘                            └──────────────────┘
```

## Setup

```bash
git clone https://github.com/suhail1060/notes-mcp.git
cd notes-mcp
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
export GEMINI_API_KEY="your-key-here"
```

## Usage

**Inspect the server directly** (no LLM needed):
```bash
mcp dev server/notes_server.py
```
Opens a browser UI to explore resources, tools, and prompts manually.

**Run the interactive agent**:
```bash
python client/agent_client.py
```
Type natural language requests; Gemini picks the right tool and the client executes it via MCP.

```
You: create a note called groceries with eggs and milk
[calling tool: create_note({'title': 'groceries', 'content': 'eggs and milk'})]
[tool result: Created note: groceries.md]

Assistant: I've created the note "groceries.md" with your list.
```

**Run tests**:
```bash
pytest tests/ -v
```

## MCP concepts covered

- **Resources** — read-only data (`notes://list`) the client can fetch
- **Tools** — actions with side effects (`create_note`, `read_note`, `delete_note`, `search_notes`)
- **Prompts** — reusable prompt templates (`summarize_note`)
- **Transport** — stdio-based JSON-RPC between client and server
- **Client discovery** — capability negotiation via `session.initialize()` and `list_tools()`/`list_resources()`/`list_prompts()`
- **LLM tool-calling loop** — converting MCP tool schemas to Gemini function declarations, executing the chosen tool, and feeding results back for a final response

## Project structure

```
notes-mcp/
├── server/
│   └── notes_server.py    # MCP server: resources, tools, prompts
├── client/
│   ├── agent_client.py    # Interactive CLI using Gemini + MCP
│   └── llm_agent.py       # Gemini <-> MCP tool schema conversion
├── tests/
│   └── test_notes_server.py
├── data/notes/             # Notes storage (gitignored)
└── pyproject.toml
```

## License

MIT License — see [LICENSE](LICENSE) for details.