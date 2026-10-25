from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import List, Optional
from order_service.app.schemas.order_item import OrderItemResponse, OrderItem


class OrderCreate(BaseModel):
    items: List[OrderItem]    #OrderItemResponse
    user_id: int


class OrderUpdate(BaseModel):
    user_id: Optional[int] = None
    items: Optional[List[OrderItem]] = None    #OrderItemResponse
    status: Optional[str] = None


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="Order ID")
    user_id: int
    status: str = Field(..., description="Status Order")
    total_price: float = Field(..., description="quantity * price")
    created_at: datetime
    items: List["OrderItemResponse"]
