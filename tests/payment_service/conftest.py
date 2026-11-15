import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from payment_service.app.config import settings
from payment_service.app.database import Base, get_db
from payment_service.app.main import app
from payment_service.app.models import Payment
from tests.db import create_test_session_factory, reset_schema
from tests.payment_service.seed import seed_payments

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5439/payment_test"

test_engine, TestSessionLocal = create_test_session_factory(TEST_DATABASE_URL)


class FakeProducer:
    """Заглушка PaymentProducer: RabbitMQ не поднимаем."""

    async def connect(self) -> None:
        return None

    async def publish(self, routing_key: str, data: dict) -> None:
        return None

    async def close(self) -> None:
        return None


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


@pytest.fixture(autouse=True)
def fast_payment_delay(monkeypatch):
    monkeypatch.setattr(settings, "PAYMENT_DELAY_SECONDS", 0.0)


@pytest_asyncio.fixture
async def client():
    """HTTP-клиент + заглушка RabbitMQ-продюсера.

    Эндпоинты payment_service читают app.state.payment_producer, который
    в обычном режиме создаётся только в lifespan. ASGITransport lifespan
    не выполняет, поэтому заполняем app.state вручную.
    """
    app.state.payment_producer = FakeProducer()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


@pytest_asyncio.fixture
async def seeded_payments(db_session) -> list[Payment]:
    return await seed_payments(db_session, count=3)
