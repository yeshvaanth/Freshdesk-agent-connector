from app.clients.freshdesk_client import FreshdeskClient
from app.exceptions import TicketNotFoundError


class TicketService:

    def __init__(self, client: FreshdeskClient):
        self.client = client

    async def get_tickets(self, page: int = 1, limit: int = 10):
        return await self.client.get_tickets(page, limit)

    async def get_ticket(self, ticket_id: int):
        ticket = await self.client.get_ticket(ticket_id)

        if ticket is None:
            raise TicketNotFoundError(
                f"Ticket {ticket_id} not found"
            )

        return ticket

    async def search_tickets(self, query: str):
        return await self.client.search_tickets(query)