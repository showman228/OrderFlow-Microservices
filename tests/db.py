from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase


def create_test_session_factory(
    url: str,
) -> tuple[AsyncEngine, async_sessionmaker[AsyncSession]]:
    """Создаёт асинхронный движок и фабрику сессий для тестовой БД.

    expire_on_commit=False — чтобы объекты оставались доступными после commit
    без дополнительных запросов к БД.
    """
    engine = create_async_engine(url)
    factory = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    return engine, factory


async def reset_schema(engine: AsyncEngine, base: type[DeclarativeBase]) -> None:
    """Полностью сбрасывает схему: drop_all, затем create_all.

    base.metadata должен быть заполнен импортированными моделями сервиса.
    """
    async with engine.begin() as conn:
        await conn.run_sync(base.metadata.drop_all)
        await conn.run_sync(base.metadata.create_all)
