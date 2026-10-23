from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import List
from order_service.app.schemas.order_item import OrderItemResponse

class OrderBase(BaseModel):
    user_id: int
    status: str
    total_price: float

class OrderCreate(OrderBase):
    pass


class OrderUpdate(OrderBase):
    pass


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(..., description="Order ID")
    user_id: int
    status: str = Field(..., description="Status Order")
    total_price: int = Field(..., description="quantity * price")
    created_at: datetime
    items: List["OrderItemResponse"]
