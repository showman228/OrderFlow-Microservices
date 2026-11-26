from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

class Notification(BaseModel):
    user_id: int
    order_id: int
    status: str
    total_price: float
    message: str

class NotificationCreate(Notification):
    pass

class OrderPaidNotificationCreate(BaseModel):
    order_id: int = Field(ge=1)
    user_id: int = Field(ge=1)
    amount: float = Field(ge=0, allow_inf_nan=False)

class NotificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    order_id: int
    status: str
    total_price: float
    message: str
    created_at: datetime

