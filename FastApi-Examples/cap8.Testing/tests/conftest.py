import asyncio
import httpx
import pytest
from manage import app
from database.connection import Settings
from models.events import Event
from models.users import User


@pytest.fixture(scope="session")
def event_loop() -> None:
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

async def init_db() -> None:
    test_settings = Settings()
    test_settings.DATABASE_URL = 'mongodb://localhost:27017/testdb'
    await test_settings.initialize_database()

@pytest.fixture(scope="session")
async def default_client() -> None:
    await init_db()
    async with httpx.AsyncClient(app=app,base_url="http://app") as client:
        yield client
        await Event.find_all().delete()
        await User.find_all().delete()