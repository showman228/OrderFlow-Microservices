from typing import Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from user_service.app.models.users import User
from user_service.app.database import get_db
from user_service.app.core.security import Token
from user_service.app.schemas.user import UserCreate, UserResponse
from user_service.app.services.user_service import UserService, oauth2_scheme
from user_service.app.config import settings
from user_service.app.core.security import create_access_token

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db)
) -> Token:

    user = UserService(db)

    if not user.authenticate(form_data.username, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token)

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)) -> dict:
    user = UserService(db)
    new_user: UserResponse = user.create(user_data)
    return {"message": f"User: {new_user.username} registered successfully"}

@router.get("/me")
async def read_me(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession = Depends(get_db)
) -> UserResponse:

    user = UserService(db)
    return UserResponse.model_validate(user.get_current_user(token))

