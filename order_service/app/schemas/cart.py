from pydantic import BaseModel, Field
from typing import Optional, List


class CartItemBase(BaseModel):
    product_id: int = Field(..., description="Unique product id")
    quantity: int = Field(..., description="Quantity of product")


class CartItemCreate(CartItemBase):
    pass


class CartItemUpdate(CartItemBase):
    product_id: int = Field(..., description="Unique product id")
    quantity: int = Field(..., description="Quantity of product")


class CartItem(BaseModel):
    product_id: int
    name: str = Field(..., max_length=250, description="Product name")
    price: float = Field(..., gt=0, description="Product price")
    quantity: int = Field(..., description="Quantity of product")
    image_url: Optional[str] = Field(None, description="Product image url")
    subtotal: float = Field(..., gt=0, description="Subtotal of product")


class CartResponse(BaseModel):
    items: List[CartItem] = Field(..., description="List of cart items")
    total: float = Field(..., ge=0, description="Total cart total")
    items_count: int = Field(..., ge=0, description="Number of items per page")