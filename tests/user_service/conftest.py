import httpx
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from tests.db import create_test_session_factory, reset_schema
from tests.user_service.seed import seed_users
from user_service.app.database import Base, get_db
from user_service.app.main import app
from user_service.app.models.users import User

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5436/user_test"

test_engine, TestSessionLocal = create_test_session_factory(TEST_DATABASE_URL)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def manage_engine():
    yield
    await test_engine.dispose()


@pytest_asyncio.fixture(autouse=True)
async def reset_database():
    await reset_schema(test_engine, Base)


@pytest_asyncio.fixture
async def db_session():
    async with TestSessionLocal() as session:
        yield session


async def override_get_db():
    async with TestSessionLocal() as session:
        yield session


@pytest.fixture(scope="session", autouse=True)
def override_dependencies():
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


@pytest_asyncio.fixture
async def seeded_users(db_session) -> list[User]:
    return await seed_users(db_session, count=3)
