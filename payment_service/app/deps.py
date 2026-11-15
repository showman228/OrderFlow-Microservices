from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from payment_service.app.database import get_db
from payment_service.app.producer import PaymentProducer

SessionDep = Annotated[AsyncSession, Depends(get_db)]


def get_producer(request: Request) -> PaymentProducer:
    return request.app.state.payment_producer


ProducerDep = Annotated[PaymentProducer, Depends(get_producer)]
