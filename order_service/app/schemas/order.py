from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from order_service.app.schemas.order_item import OrderItemResponse, OrderItemCreate

class OrderBase(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    user_id: int
    status: str
    total_price: int

class OrderCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: list[OrderItemCreate]
    user_id: int


class OrderUpdate(BaseModel):
    user_id: int | None = None
    items: list[OrderItemCreate] | None = None
    status: str | None = None


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Order ID")
    user_id: int
    status: str = Field(..., description="Status Order")
    total_price: float = Field(..., description="quantity * price")
    created_at: datetime
    items: list[OrderItemResponse]
