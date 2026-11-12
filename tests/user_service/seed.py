import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from user_service.app.core.security import hash_password
from user_service.app.models.users import User


async def seed_users(db: AsyncSession, count: int = 3) -> list[User]:
    """Создаёт несколько пользователей и возвращает их (с id после commit)."""
    users = [
        User(
            email=f"mail{i + 1}@mail.com",
            password_hash=await asyncio.to_thread(hash_password, f"123{i + 1}"),
            username=f"User_{i + 1}",
            firstname=f"name_{i + 1}",
        )
        for i in range(count)
    ]
    db.add_all(users)
    await db.commit()

    for user in users:
        await db.refresh(user)

    return users
