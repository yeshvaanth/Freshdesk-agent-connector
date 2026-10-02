import httpx

from app.config import settings
from app.exceptions import (
    FreshdeskAPIError,
    FreshdeskAuthenticationError,
    FreshdeskRateLimitError,
    TicketNotFoundError,
)
from app.mock_data import tickets


class FreshdeskClient:
    def __init__(
        self,
        transport: httpx.AsyncBaseTransport | None = None,
    ):
        self.use_mock = settings.app_mode == "mock"
        self._transport = transport

        if self.use_mock:
            return

        if not settings.freshdesk_domain:
            raise ValueError(
                "FRESHDESK_DOMAIN is required in freshdesk mode"
            )

        if not settings.freshdesk_api_key:
            raise ValueError(
                "FRESHDESK_API_KEY is required in freshdesk mode"
            )

        domain = settings.freshdesk_domain.strip().rstrip("/")

        if not domain.startswith(("https://", "http://")):
            domain = f"https://{domain}"

        self.base_url = f"{domain}/api/v2"
        self.auth = (settings.freshdesk_api_key, "X")

    async def _request(
        self,
        path: str,
        params: dict | None = None,
    ):
        async with httpx.AsyncClient(
            timeout=15.0,
            auth=self.auth,
            transport=self._transport,
        ) as client:
            try:
                response = await client.get(
                    f"{self.base_url}{path}",
                    params=params,
                )
                response.raise_for_status()
                return response.json()

            except httpx.HTTPStatusError as exc:
                status_code = exc.response.status_code

                if status_code in (401, 403):
                    raise FreshdeskAuthenticationError(
                        "Freshdesk authentication failed"
                    ) from exc

                if status_code == 404:
                    raise TicketNotFoundError(
                        "Ticket not found"
                    ) from exc

                if status_code == 429:
                    raise FreshdeskRateLimitError(
                        "Freshdesk rate limit exceeded"
                    ) from exc

                raise FreshdeskAPIError(
                    f"Freshdesk API returned status {status_code}"
                ) from exc

    @staticmethod
    def _normalize_ticket(ticket: dict) -> dict:
        status_map = {
            2: "open",
            3: "pending",
            4: "resolved",
            5: "closed",
        }

        priority_map = {
            1: "low",
            2: "medium",
            3: "high",
            4: "urgent",
        }

        requester = ticket.get("requester") or {}

        return {
            "id": ticket["id"],
            "subject": ticket.get("subject", ""),
            "status": status_map.get(
                ticket.get("status"),
                str(ticket.get("status", "unknown")),
            ),
            "priority": priority_map.get(
                ticket.get("priority"),
                str(ticket.get("priority", "unknown")),
            ),
            "email": requester.get("email", ""),
        }

    async def get_tickets(
        self,
        page: int = 1,
        limit: int = 10,
    ):
        if self.use_mock:
            total = len(tickets)
            start = (page - 1) * limit
            end = start + limit

            return {
                "items": tickets[start:end],
                "page": page,
                "limit": limit,
                "total": total,
                "has_next": end < total,
            }

        data = await self._request(
            "/tickets",
            params={
                "page": page,
                "per_page": limit,
                "include": "requester",
            },
        )

        items = [
            self._normalize_ticket(ticket)
            for ticket in data
        ]

        # Freshdesk's list response does not provide a total count.
        return {
            "items": items,
            "page": page,
            "limit": limit,
            "total": None,
            "has_next": len(items) == limit,
        }

    async def get_ticket(self, ticket_id: int):
        if self.use_mock:
            for ticket in tickets:
                if ticket["id"] == ticket_id:
                    return ticket

            return None

        data = await self._request(
            f"/tickets/{ticket_id}",
            params={"include": "requester"},
        )

        return self._normalize_ticket(data)

    async def search_tickets(self, query: str):
        if self.use_mock:
            return [
                ticket
                for ticket in tickets
                if query.lower() in ticket["subject"].lower()
            ]

        data = await self._request(
            "/search/tickets",
            params={
                "query": f'"subject:\'{query}\'"',
            },
        )

        return [
            self._normalize_ticket(ticket)
            for ticket in data.get("results", [])
        ]