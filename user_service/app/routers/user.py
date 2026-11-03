from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from user_service.app.database import get_db
from user_service.app.models.users import User
from user_service.app.schemas.user import UserCreate, UserResponse
from user_service.app.services.user_service import UserService

security = HTTPBasic()

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse
)
async def register_user(
    user_data: UserCreate, db: AsyncSession = Depends(get_db)
) -> UserResponse:
    user = UserService(db)
    return UserResponse.model_validate(await user.create(user_data))


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    service = UserService(db)
    return await service.authenticate(credentials.username, credentials.password)


@router.get("/all", status_code=status.HTTP_200_OK, response_model=list[UserResponse])
async def get_all(db: AsyncSession = Depends(get_db)):
    users = UserService(db)
    return await users.get_all_users()
