from fastapi import APIRouter, HTTPException, Query

from app.clients.freshdesk_client import FreshdeskClient
from app.models import PaginatedTickets, Ticket
from app.services.ticket_service import TicketService


router = APIRouter()

freshdesk_client = FreshdeskClient()
ticket_service = TicketService(freshdesk_client)


@router.get("/tickets", response_model=PaginatedTickets)
async def get_tickets(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
):
    return await ticket_service.get_tickets(page, limit)


@router.get("/tickets/search", response_model=list[Ticket])
async def search_tickets(
    query: str = Query(min_length=1, max_length=100),
):
    query = query.strip()

    if not query:
        raise HTTPException(
            status_code=422,
            detail="Search query cannot be blank",
        )

    return await ticket_service.search_tickets(query)


@router.get("/tickets/{ticket_id}", response_model=Ticket)
async def get_ticket(ticket_id: int):
    return await ticket_service.get_ticket(ticket_id)