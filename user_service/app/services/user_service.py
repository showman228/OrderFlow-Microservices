from user_service.app.repository.user_repository import UserRepository
from user_service.app.models.users import User
from user_service.app.schemas.user import UserResponse, UserCreate
from user_service.app.core.security import hash_password, verify_password, decode_user

from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class UserService:
    def __init__(self, db: AsyncSession):
        self.user_crud = UserRepository(db)

    async def get_all_users(self) -> list[UserResponse]:
        users = await self.user_crud.get_all()
        return [UserResponse.model_validate(user) for user in users]

    async def get_by_id(self, user_id: int) -> UserResponse | None:
        user = await self.user_crud.get_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found by id"
            ) 
        return UserResponse.model_validate(user)

    async def get_by_username(self, username: str) -> UserResponse | None:
        user = await self.user_crud.get_by_username(username)
        if user is None:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found by username"
                )
        return UserResponse.model_validate(user)

    async def get_by_email(self, email: str) -> UserResponse | None:
        user = await self.user_crud.get_by_email(email)
        if user is None:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found by email"
                )
        return UserResponse.model_validate(user)

    async def create(self, user_data: UserCreate) -> UserResponse | None:
        existing = await self.user_crud.get_by_email(user_data.email)
        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This user already registered"
            )
        password_hash = hash_password(user_data.password)
        user = await self.user_crud.create(user_data, password_hash)
        return UserResponse.model_validate(user)


    async def update(self, user_data: UserCreate, user_id: int) -> UserResponse | None:
        user = await self.user_crud.update(user_data, user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found by id"
            )
        return UserResponse.model_validate(user)

        
    async def delete(self, user_id: int) -> bool:
        user = await self.user_crud.get_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not existing"
            )
        return True

    async def authenticate(self, useranme: str, password: str) -> User:
        user = await self.get_by_username(useranme)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User this username not found"
            )
        if not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="incorrect password"
            )
        return user

    async def get_current_user(
        self,
        token: Annotated[str, Depends(oauth2_scheme)],
    ) -> User:

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        username = decode_user(token)
        if username is None:
            credentials_exception

        user = await self.user_crud.get_by_username(username)

        if user is None:
            credentials_exception

        return user


        
        
