from pydantic import BaseModel


class Ticket(BaseModel):
    id: int
    subject: str
    status: str
    priority: str
    email: str


class PaginatedTickets(BaseModel):
    items: list[Ticket]
    page: int
    limit: int
    total: int | None
    has_next: bool