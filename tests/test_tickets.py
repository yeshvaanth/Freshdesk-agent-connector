from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_list_tickets_returns_paginated_response():
    response = client.get("/tickets?page=1&limit=2")

    assert response.status_code == 200

    data = response.json()

    assert len(data["items"]) == 2
    assert data["page"] == 1
    assert data["limit"] == 2
    assert data["total"] == 3
    assert data["has_next"] is True


def test_get_existing_ticket():
    response = client.get("/tickets/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_missing_ticket_returns_404():
    response = client.get("/tickets/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Ticket 999 not found"


def test_search_tickets():
    response = client.get(
        "/tickets/search",
        params={"query": "payment"}
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["id"] == 2


def test_blank_search_rejected():
    response = client.get(
        "/tickets/search",
        params={"query": "   "}
    )

    assert response.status_code == 422