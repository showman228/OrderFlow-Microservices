from pydantic import BaseModel, Field, ConfigDict
import re

class CategoryCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., description="Name of Category")
    slug: str = Field(..., pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Unique identifier for this category")
    name: str
    slug: str