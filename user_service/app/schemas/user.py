from pydantic import BaseModel, EmailStr, ConfigDict

class UserBase(BaseModel):

    email: EmailStr
    username: str | None
    firstname: str | None


class UserCreate(UserBase):
    password_hash: str


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int