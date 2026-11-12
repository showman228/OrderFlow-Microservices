import httpx
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from order_service.app.database import Base, get_db
from order_service.app.main import app
from order_service.app.models import Order
from tests.db import create_test_session_factory, reset_schema
from tests.order_service.seed import seed_orders

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5437/order_test"

test_engine, TestSessionLocal = create_test_session_factory(TEST_DATABASE_URL)


class FakeCache:
    """Заглушка RedisCache: внешний сервис мокаем, сам Redis не поднимаем."""

    async def get_value(self, key: str) -> dict | list | None:
        return None

    async def set_value(self, key: str, value: dict | list) -> None:
        return None

    async def delete(self, key: str) -> None:
        return None

    async def close(self) -> None:
        return None


async def _catalog_handler(request: httpx.Request) -> httpx.Response:
    """Заглушка каталога: отвечает фиксированным товаром на любой запрос."""
    return httpx.Response(200, json={"id": 1, "name": "Product-1", "price": 1001.0})


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
    """HTTP-клиент + заглушки внешних зависимостей (каталог, кеш).

    Эндпоинты order_service читают app.state.catalog_client и app.state.cache,
    которые в обычном режиме создаются только в lifespan. ASGITransport lifespan
    не выполняет, поэтому заполняем app.state вручную.
    """
    app.state.catalog_client = httpx.AsyncClient(
        transport=httpx.MockTransport(_catalog_handler), base_url="http://test"
    )
    app.state.cache = FakeCache()

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c

    await app.state.catalog_client.aclose()


@pytest_asyncio.fixture
async def seeded_orders(db_session) -> list[Order]:
    return await seed_orders(db_session, count=3)
