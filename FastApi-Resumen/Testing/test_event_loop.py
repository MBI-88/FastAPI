import pytest , asyncio, main
from asgi_lifespan import LifespanManager
from main import app 


@pytest.fixture(scope='session')
def event_loop() -> None:
    loop = asyncio.get_event_loop()
    yield loop 
    loop.close()

@pytest.fixture
async def test_client() -> None:
    async with LifespanManager(main):
        async with main.AsyncClient(app=main,base_url='http://app.io') as test_client:
            yield test_client
            