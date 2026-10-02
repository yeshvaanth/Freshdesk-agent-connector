import asyncio

import httpx
import pytest

from app.clients.freshdesk_client import FreshdeskClient
from app.exceptions import FreshdeskAuthenticationError
from app.config import settings


def test_live_client_get_tickets(monkeypatch):
    monkeypatch.setattr(settings, "app_mode", "freshdesk")
    monkeypatch.setattr(
        settings, "freshdesk_domain", "example.freshdesk.com"
    )
    monkeypatch.setattr(
        settings, "freshdesk_api_key", "test-api-key"
    )

    def handler(request: httpx.Request):
        assert request.url.path == "/api/v2/tickets"
        assert request.url.params["page"] == "1"
        assert request.url.params["per_page"] == "2"

        # Verify HTTP Basic Authentication.
        assert request.headers["Authorization"].startswith("Basic ")

        return httpx.Response(
            200,
            json=[
                {
                    "id": 101,
                    "subject": "Test ticket",
                    "status": 2,
                    "priority": 3,
                    "requester": {
                        "email": "test@example.com"
                    },
                }
            ],
            request=request,
        )

    async def run_test():
        transport = httpx.MockTransport(handler)
        client = FreshdeskClient(transport=transport)

        result = await client.get_tickets(page=1, limit=2)

        assert result["items"][0] == {
            "id": 101,
            "subject": "Test ticket",
            "status": "open",
            "priority": "high",
            "email": "test@example.com",
        }

        assert result["page"] == 1
        assert result["limit"] == 2
        assert result["total"] is None

    asyncio.run(run_test())


def test_live_client_get_ticket(monkeypatch):
    monkeypatch.setattr(settings, "app_mode", "freshdesk")
    monkeypatch.setattr(
        settings, "freshdesk_domain", "example.freshdesk.com"
    )
    monkeypatch.setattr(
        settings, "freshdesk_api_key", "test-api-key"
    )

    def handler(request: httpx.Request):
        assert request.url.path == "/api/v2/tickets/101"

        return httpx.Response(
            200,
            json={
                "id": 101,
                "subject": "Login issue",
                "status": 2,
                "priority": 3,
                "requester": {
                    "email": "user@example.com"
                },
            },
            request=request,
        )

    async def run_test():
        transport = httpx.MockTransport(handler)
        client = FreshdeskClient(transport=transport)

        result = await client.get_ticket(101)

        assert result["id"] == 101
        assert result["subject"] == "Login issue"
        assert result["status"] == "open"
        assert result["priority"] == "high"
        assert result["email"] == "user@example.com"

    asyncio.run(run_test())


def test_live_client_handles_401(monkeypatch):
    monkeypatch.setattr(settings, "app_mode", "freshdesk")
    monkeypatch.setattr(
        settings, "freshdesk_domain", "example.freshdesk.com"
    )
    monkeypatch.setattr(
        settings, "freshdesk_api_key", "invalid-api-key"
    )

    def handler(request: httpx.Request):
        return httpx.Response(
            401,
            json={"code": "invalid_credentials"},
            request=request,
        )

    async def run_test():
        transport = httpx.MockTransport(handler)
        client = FreshdeskClient(transport=transport)

        # The client converts HTTP 401 into this custom exception
        with pytest.raises(FreshdeskAuthenticationError):
            await client.get_tickets()

    asyncio.run(run_test())