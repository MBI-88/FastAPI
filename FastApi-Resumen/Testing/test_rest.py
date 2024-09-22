import pytest, main
from fastapi import status
from test_event_loop import test_client

# Haciendo test a las endpoint

@pytest.mark.asyncio
async def test_hello_world(test_client: main.AsyncClient) -> None:
    response  = await test_client.get("/")
    
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json == {"hello": "world"}