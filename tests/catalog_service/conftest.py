import httpx
import pytest
import pytest_asyncio

from catalog_service.app.database import Base, get_db
from catalog_service.app.main import app
from catalog_service.app.models import Product
from tests.catalog_service.seed import seed_products
from tests.db import create_test_session_factory, reset_schema

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5435/catalog_test"

test_engine, TestSessionLocal = create_test_session_factory(TEST_DATABASE_URL)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def manage_engine():
    """Закрывает пул соединений один раз в конце тестовой сессии."""
    yield
    await test_engine.dispose()


@pytest_asyncio.fixture(autouse=True)
async def reset_database():
    """Перед каждым тестом сбрасывает схему (drop_all + create_all).

    Гарантирует чистую БД и то, что таблицы всегда существуют.
    """
    await reset_schema(test_engine, Base)


@pytest_asyncio.fixture
async def db_session():
    """Сессия напрямую к тестовой БД — для сидирования/репозиторий-тестов."""
    async with TestSessionLocal() as session:
        yield session


async def override_get_db():
    """Подмена get_db: сессия из тестовой фабрики вместо продовой."""
    async with TestSessionLocal() as session:
        yield session


@pytest.fixture(scope="session", autouse=True)
def override_dependencies():
    """Регистрирует override get_db на время тестов и очищает после."""
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client():
    """HTTP-клиент: запросы идут прямо в приложение без реального сервера."""
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


@pytest_asyncio.fixture
async def seeded_products(db_session) -> list[Product]:
    return await seed_products(db_session, count=3)
