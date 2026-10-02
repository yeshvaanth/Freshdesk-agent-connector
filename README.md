# Freshdesk Agent Connector

A Python-based connector that enables an AI agent to read Freshdesk support tickets using FastAPI and the Model Context Protocol (MCP).

Features

* List tickets with pagination
* Retrieve tickets by ID
* Search tickets by subject
* Expose ticket operations as MCP tools
* Support mock data and Freshdesk API-key authentication
* Handle API errors, including rate limits

 Tech Stack

Python, FastAPI, HTTPX, Pydantic, MCP, Pytest

 Setup

```bash
git clone <your-repository-url>
cd freshdesk-agent-connector

python -m venv .venv
```

Activate the virtual environment on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```dotenv
APP_MODE=mock
FRESHDESK_DOMAIN=
FRESHDESK_API_KEY=
```

Mock mode works without Freshdesk credentials. For live mode, set `APP_MODE=freshdesk` and provide your Freshdesk domain and API key.

Run the Application

Start the REST API:

```bash
uvicorn app.main:app --reload
```

API documentation: http://127.0.0.1:8000/docs

Start the MCP server:

```bash
python -m app.mcp.tools
```

## API Endpoints

| Method | Endpoint                        | Description    |
| ------ | ------------------------------- | -------------- |
| GET    | `/tickets`                      | List tickets   |
| GET    | `/tickets/{ticket_id}`          | Get a ticket   |
| GET    | `/tickets/search?query=payment` | Search tickets |
| GET    | `/health`                       | Health check   |

 MCP Tools

* `list_tickets` — List tickets with pagination
* `get_ticket` — Retrieve a ticket by ID
* `search_tickets` — Search tickets by subject

## Agent Capabilities and Limitations

The agent can list, retrieve, and search tickets. The connector is read-only; it cannot create, update, reply to, or delete tickets.

API-key authentication is supported in Freshdesk mode. HTTP 429 responses are handled, but automatic retries are not implemented.

 Testing

```bash
python -m pytest -v
python -m app.mcp.check_client
```

The mock implementation and MCP tools have been tested locally. Live Freshdesk integration has not been verified against a real account.

 License

Created as part of a technical assignment.
