import httpx
import pytest_asyncio, pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from catalog_service.app.database import Base, get_db
from catalog_service.app.main import app
from catalog_service.app.models import Category, Product

# URL отдельной тестовой БД (поднимается через docker-compose.test.yml на порту 5435).
# Не пересекается с продовой catalog_db, чтобы тесты не трогали реальные данные.
TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5435/catalog_test"

# Асинхронный движок SQLAlchemy, указывающий на тестовую БД.
# Создаётся один раз при импорте модуля (движок ленивый — соединение не открывается сразу).
test_engine = create_async_engine(TEST_DATABASE_URL)

# Фабрика сессий (аналог SessionLocal из app/database.py), но привязана к тестовому движку.
# expire_on_commit=False — чтобы объекты оставались доступными после commit без доп. запросов.
TestSessionLocal = async_sessionmaker(
    bind=test_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest_asyncio.fixture(scope="function", autouse=True)
async def prepare_database():
    """Подготовка тестовой БД (выполняется автоматически для всех тестов).

    scope="session" — запускается один раз на всю тестовую сессию.
    autouse=True  — применяется ко всем тестам без явного запроса фикстуры.

    Перед тестами: create_all создаёт их заново
    (схему берёт из Base.metadata — её заполняют импортированные модели Category/Product).
    После тестов: таблицы снова удаляются, а пул соединений закрывается (dispose).
    """
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()


@pytest_asyncio.fixture
async def db_session():
    """Сессия напрямую к тестовой БД — для сидирования/репозиторий-тестов."""
    async with TestSessionLocal() as session:
        yield session


async def override_get_db():
    """Подмена зависимости get_db: отдаёт сессию из тестовой фабрики вместо продовой.

    Имеет ту же сигнатуру (async-генератор), что и оригинальный get_db,
    поэтому FastAPI может подставить его через dependency_overrides.
    """
    async with TestSessionLocal() as session:
        yield session


@pytest.fixture(scope="session", autouse=True)
def override_dependencies():
    """Регистрация подмены get_db в приложении FastAPI на время тестов.

    До yield: app.dependency_overrides[get_db] = override_get_db — теперь все эндпоинты,
    использующие Depends(get_db), получат сессию от тестовой БД.
    После yield (teardown): overrides очищаются, чтобы не влиять на другие тесты/запуски.
    """
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client():
    """HTTP-клиент для API-тестов.

    ASGITransport позволяет отправлять запросы прямо в FastAPI-приложение,
    не поднимая реальный сервер (без сети, uvicorn и lifespan).
    base_url="http://test" — условный базовый адрес, нужен httpx для формирования URL;
    реального HTTP-соединения при этом не происходит.
    """
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
