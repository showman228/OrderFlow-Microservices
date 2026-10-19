from pydantic import BaseModel


class OrderItem(BaseModel):
    product_id: int
    product_name: str
    order_id: int
    quantity: int
    price: int

class OrderItemCreate(OrderItem):
    pass


class OrderItemUpdate(OrderItem):
    pass

class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    order_id: int
    quantity: int
    price: int 