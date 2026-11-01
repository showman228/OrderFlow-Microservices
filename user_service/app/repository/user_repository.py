from sqlalchemy import select
from user_service.app.models.users import User
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr

from user_service.app.schemas.user import UserCreate

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[User]:
        users = await self.db.execute(select(User))
        return users.scalars().all()        

    async def get_by_id(self, user_id: int) -> User | None:
        user = await self.db.execute(select(User).where(user_id == User.id))
        return user.scalars().one_or_none

    async def get_by_username(self, username: str) -> User | None:
        user = await self.db.execute(select(User).where(username == User.username))
        return user.scalars().one_or_none()

    async def get_by_email(self, email: EmailStr) -> User | None:
        user = await self.db.execute(select(User).where(User.email == email))
        return user.scalars().one_or_none()

    async def create(self, user_data: UserCreate, password_hash: str) -> User:
        user = User(
            email=user_data.email,
            password_hash=password_hash,
            username=user_data.username,
            firstname=user_data.firstname
        )

        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def update(self, user_data: UserCreate, user_id: int) -> User | None:
        user = await self.get_by_id(user_id)

        if user is None:
            return None

        for field, val in user_data.model_dump(exclude_unset=True).items():
            setattr(user, field, val)

        await self.db.commit()
        await self.db.refresh(user)

        return user

    
    async def delete(self, user_id: int) -> bool:
        user = await self.get_by_id(user_id)

        if user is None:
            return False

        self.db.delete(user)
        await self.db.commit()

        return True
