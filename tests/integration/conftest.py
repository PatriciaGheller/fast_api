import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from src.config import settings

settings.database_url = f"sqlite:///tests.db" 


@pytest_asyncio.fixture
async def db(request):
    from src.database import database, engine, metadata  # noqa

    await database.connect()
    metadata.create_all(engine)

    def teardown():
        async def _teardown():
            await database.disconnect()
            metadata.drop_all(engine)

        asyncio.run(_teardown())

    request.addfinalizer(teardown)


@pytest_asyncio.fixture
async def client(db):
    from src.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://testserver",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    ) as client:
        yield client


@pytest_asyncio.fixture
async def access_token():
    from src.security import sign_jwt
    return sign_jwt(1)["access_token"]
