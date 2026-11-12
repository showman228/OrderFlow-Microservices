from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from payment_service.app.models.payment import PaymentStatus


class PaymentCreate(BaseModel):
    order_id: int = Field(..., ge=1, description="Order id")
    user_id: int = Field(..., ge=1, description="User id")
    amount: float = Field(..., gt=0, description="Payment amount")


class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int
    user_id: int
    amount: float
    status: PaymentStatus
    created_at: datetime
