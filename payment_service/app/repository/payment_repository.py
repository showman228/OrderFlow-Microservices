from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from payment_service.app.models.payment import Payment
from payment_service.app.schemas.payment import PaymentCreate


class PaymentRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_all_payments(self) -> list[Payment]:
        payments = await self.db.execute(select(Payment))
        return list(payments.scalars().all())

    async def get_by_id(self, payment_id: int) -> Payment | None:
        payment = await self.db.execute(select(Payment).where(Payment.id == payment_id))
        return payment.scalar_one_or_none()

    async def get_by_order_id(self, order_id: int) -> Payment | None:
        payment = await self.db.execute(
            select(Payment).where(Payment.order_id == order_id)
        )
        return payment.scalar_one_or_none()

    async def get_by_user_id(self, user_id: int) -> list[Payment]:
        payments = await self.db.execute(
            select(Payment).where(Payment.user_id == user_id)
        )
        return list(payments.scalars().all())

    async def create(self, payment_data: PaymentCreate) -> Payment:
        payment = Payment(
            order_id=payment_data.order_id,
            user_id=payment_data.user_id,
            amount=payment_data.amount,
        )
        self.db.add(payment)
        await self.db.commit()
        return payment

    async def update_status(self, payment_id: int, new_status: str) -> Payment | None:
        payment = await self.get_by_id(payment_id)
        if payment is None:
            return None

        payment.status = new_status
        await self.db.commit()
        return payment

    async def delete(self, payment_id: int) -> bool:
        payment = await self.get_by_id(payment_id)
        if payment is None:
            return False

        await self.db.delete(payment)
        await self.db.commit()
        return True
