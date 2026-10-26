from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import List, Optional
from order_service.app.schemas.order_item import OrderItemResponse, OrderItemCreate

class OrderBase(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    user_id: int
    status: str
    total_price: int

class OrderCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    items: List[OrderItemCreate]
    user_id: int


class OrderUpdate(BaseModel):
    user_id: Optional[int] = None
    items: Optional[List[OrderItemCreate]] = None
    status: Optional[str] = None


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Order ID")
    user_id: int
    status: str = Field(..., description="Status Order")
    total_price: float = Field(..., description="quantity * price")
    created_at: datetime
    items: List[OrderItemResponse]
