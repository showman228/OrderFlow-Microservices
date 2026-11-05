from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from order_service.app.schemas.order_item import OrderItemResponse


class OrderItemIn(BaseModel):
    product_id: int = Field(..., ge=1, description="Product id from catalog service")
    quantity: int = Field(..., ge=1, description="Quantity of product")


class OrderBase(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    user_id: int
    status: str
    total_price: float


class OrderCreate(BaseModel):
    user_id: int = Field(..., ge=1, description="Order owner id")
    items: list[OrderItemIn] = Field(..., min_length=1, description="Ordered products")


class OrderUpdate(BaseModel):
    user_id: int | None = None
    status: str | None = None


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Order ID")
    user_id: int
    status: str = Field(..., description="Status Order")
    total_price: float = Field(..., description="quantity * price")
    created_at: datetime
    items: list[OrderItemResponse]
