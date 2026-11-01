from user_service.app.repository.user_repository import UserRepository
from user_service.app.models.users import User
from user_service.app.schemas.user import UserResponse, UserCreate

from typing import Annotated

from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

secutiry = HTTPBasic()

class UserService:
    def __init__(self, db: AsyncSession):
        self.user_crud = UserRepository(db)

    async def get_all_users(self) -> list[UserResponse]:
        users = await self.user_crud.get_all()
        return [UserResponse.model_validate(user) for user in users]

    async def get_by_id(self, user_id: int) -> UserResponse | None:
        pass

    async def get_by_username(self, username: str) -> UserResponse | None:
        pass

    async def get_by_email(self, email: str) -> UserResponse | None:
        pass

    async def create(self, user_data: UserCreate, password_hash: str) -> UserResponse:
        pass

    async def update(self, user_data: UserCreate, user_id: int) -> UserResponse | None:
        pass

    async def delete(self, user_id: int) -> bool:
        pass

    async def authenticate(self, useranme: str, password: str) -> User:
        pass

    async def get_current_user(
        self,
        credentials: Annotated[HTTPBasicCredentials, Depends(secutiry)],
        db: AsyncSession = Depends(get_db),
) -> User:
        return await self.authenticate(credentials.username, credentials.password)
