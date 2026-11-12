from sqlalchemy.ext.asyncio import AsyncSession

from payment_service.app.models import Payment


async def seed_payments(db: AsyncSession, count: int = 3) -> list[Payment]:
    """Создаёт несколько платежей со статусом pending и возвращает их."""
    payments = [
        Payment(
            order_id=i + 1,
            user_id=i + 1,
            amount=float(1000 + i),
        )
        for i in range(count)
    ]

    db.add_all(payments)
    await db.commit()

    for payment in payments:
        await db.refresh(payment)

    return payments
