import pytest
import httpx
from fastapi import status


@pytest.mark.asyncio
class TestCreatePerson:
    async def test_invalid(self, test_client: httpx.AsyncClient):
        payload = {
            "first_name": "John", "last_name": "Doe"
        }
        response = await test_client.post("/persons",
                                          json=payload)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_valid(self, test_client: httpx.AsyncClient):
        payload = {"first_name": "John", "last_name": "Doe",
                   "age": 30}
        response = await test_client.post("/persons",
                                          json=payload)
        assert response.status_code == status.HTTP_201_CREATED
        json = response.json()
        assert json == payload
