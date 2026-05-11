import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_item(client: AsyncClient):
    response = await client.post(
        "/api/v1/items/", json={"name": "Test", "description": "desc"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test"
    assert "id" in data


@pytest.mark.asyncio
async def test_get_item_not_found(client: AsyncClient):
    response = await client.get("/api/v1/items/9999")
    assert response.status_code == 404
