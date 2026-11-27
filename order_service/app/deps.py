from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from order_service.app.cache.redis import RedisCache
from order_service.app.api_clients.catalog_client import CatalogClient
from order_service.app.api_clients.payment_client import PaymentClient
from order_service.app.database import get_db
from order_service.app.producer import OrderProducer

SessionDep = Annotated[AsyncSession, Depends(get_db)]


def get_catalog_client(request: Request) -> CatalogClient:
    return CatalogClient(request.app.state.catalog_client)

def get_cache(request: Request) -> RedisCache:
    return request.app.state.cache

def get_payment_client(request: Request) -> PaymentClient:
    return PaymentClient(request.app.state.payment_client)

def get_order_producer(request: Request) -> OrderProducer:
    return request.app.state.order_producer

CatalogClientDep = Annotated[CatalogClient, Depends(get_catalog_client)]
CacheDep = Annotated[RedisCache, Depends(get_cache)]
PaymentClientDep = Annotated[PaymentClient, Depends(get_payment_client)]
OrderProducerDep = Annotated[OrderProducer, Depends(get_order_producer)]