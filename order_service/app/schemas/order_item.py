from typing import Optional

from pydantic import BaseModel, ConfigDict


class OrderItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_id: int
    product_id: int
    product_name: str
    quantity: int
    price: float


class OrderItemCreate(OrderItem):
    pass


class OrderItemUpdate(BaseModel):
    product_id: Optional[int] = None
    product_name: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[float] = None


class OrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    product_name: str
    order_id: int
    quantity: int
    price: float
