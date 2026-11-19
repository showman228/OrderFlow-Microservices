from datetime import datetime

from pydantic import BaseModel, ConfigDict

class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    product_name: str
    order_id: int
    quantity: int
    price: float

class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    status: str 
    total_price: float 
    created_at: datetime
    items: list[OrderItemResponse]
    
