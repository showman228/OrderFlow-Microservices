from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List, Optional
from ..schemas.category import CategoryResponse

class ProductBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., max_length=250, description="Product name")
    description: str = Field(None, description="Product description")
    price: int = Field(..., gt=0, description="Product price")
    category_id: int = Field(..., description="category id")
    image_url: Optional[str] = Field(None, description="Product image url")

class ProductCreate(ProductBase):
    pass


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Product id")
    name: str
    description: str
    price: int
    category_id: int
    image_url: Optional[str]
    created_at: datetime
    category: CategoryResponse = Field(..., description="Product category details")

class ProductListResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    products: List[ProductResponse]
    total: int = Field(..., description="Total product Count")