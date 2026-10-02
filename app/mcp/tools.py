from mcp.server.mcpserver import MCPServer

from app.clients.freshdesk_client import FreshdeskClient
from app.services.ticket_service import TicketService


mcp = MCPServer(
    "Freshdesk Agent Connector",
    instructions=(
        "Use these tools to list, retrieve, and search support tickets. "
        "The current implementation uses mock data."
    ),
)

client = FreshdeskClient()
ticket_service = TicketService(client)


@mcp.tool()
async def list_tickets(page: int = 1, limit: int = 10) -> dict:
    """List support tickets with pagination.

    Args:
        page: Page number, starting from 1.
        limit: Number of tickets per page, between 1 and 100.
    """
    if page < 1:
        raise ValueError("Page must be at least 1")

    if not 1 <= limit <= 100:
        raise ValueError("Limit must be between 1 and 100")

    return await ticket_service.get_tickets(page, limit)


@mcp.tool()
async def get_ticket(ticket_id: int) -> dict:
    """Retrieve a support ticket using its ID."""
    return await ticket_service.get_ticket(ticket_id)


@mcp.tool()
async def search_tickets(query: str) -> list[dict]:
    """Search support tickets by subject."""
    query = query.strip()

    if not query:
        raise ValueError("Search query cannot be blank")

    return await ticket_service.search_tickets(query)


if __name__ == "__main__":
    mcp.run()