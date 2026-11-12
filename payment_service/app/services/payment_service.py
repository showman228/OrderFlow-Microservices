import asyncio

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from payment_service.app.config import settings
from payment_service.app.models.payment import Payment, PaymentStatus
from payment_service.app.repository.payment_repository import PaymentRepository
from payment_service.app.schemas.payment import PaymentCreate, PaymentResponse


class PaymentService:
    def __init__(self, db: AsyncSession) -> None:
        self.crud = PaymentRepository(db)

    async def get_all_payments(self) -> list[PaymentResponse]:
        payments = await self.crud.get_all_payments()
        return [PaymentResponse.model_validate(payment) for payment in payments]

    async def get_by_id(self, payment_id: int) -> PaymentResponse:
        payment = await self._get_or_404(payment_id)
        return PaymentResponse.model_validate(payment)

    async def get_by_order_id(self, order_id: int) -> PaymentResponse:
        payment = await self.crud.get_by_order_id(order_id)
        if payment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Payment with order_id={order_id} not found",
            )
        return PaymentResponse.model_validate(payment)

    async def get_by_user_id(self, user_id: int) -> list[PaymentResponse]:
        payments = await self.crud.get_by_user_id(user_id)
        return [PaymentResponse.model_validate(payment) for payment in payments]

    async def create(self, payment_data: PaymentCreate) -> PaymentResponse:
        payment = await self.crud.create(payment_data)
        return PaymentResponse.model_validate(payment)

    async def delete(self, payment_id: int) -> bool:
        await self._get_or_404(payment_id)
        await self.crud.delete(payment_id)
        return True

    async def pay(self, payment_id: int) -> PaymentResponse:
        payment = await self._get_or_404(payment_id)
        self._ensure_status(payment, {PaymentStatus.PENDING}, "paid")

        await self.crud.update_status(payment.id, PaymentStatus.PROCESSING.value)
        await asyncio.sleep(settings.PAYMENT_DELAY_SECONDS)
        updated = await self.crud.update_status(payment.id, PaymentStatus.PAID.value)

        return PaymentResponse.model_validate(updated)

    async def fail(self, payment_id: int) -> PaymentResponse:
        payment = await self._get_or_404(payment_id)
        self._ensure_status(
            payment, {PaymentStatus.PENDING, PaymentStatus.PROCESSING}, "failed"
        )

        updated = await self.crud.update_status(payment.id, PaymentStatus.FAILED.value)
        return PaymentResponse.model_validate(updated)

    async def cancel(self, payment_id: int) -> PaymentResponse:
        payment = await self._get_or_404(payment_id)
        if payment.status == PaymentStatus.PAID.value:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Paid payment cannot be cancelled",
            )

        updated = await self.crud.update_status(
            payment.id, PaymentStatus.CANCELLED.value
        )
        return PaymentResponse.model_validate(updated)

    async def _get_or_404(self, payment_id: int) -> Payment:
        payment = await self.crud.get_by_id(payment_id)
        if payment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Payment with id={payment_id} not found",
            )
        return payment

    @staticmethod
    def _ensure_status(
        payment: Payment, allowed: set[PaymentStatus], action: str
    ) -> None:
        if payment.status not in {item.value for item in allowed}:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Payment with status '{payment.status}' cannot be {action}",
            )
