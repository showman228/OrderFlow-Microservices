from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from order_service.app.database import init_db
from order_service.app.config import settings

from order_service.app.routers.cart import router as cart_router
from order_service.app.routers.order import router as order_router
from order_service.app.api_clients.catalog_client import CatalogClient
from order_service.app.cache.redis import RedisCache
from order_service.app.consumer import PaymentConsumer
import httpx


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    app.state.catalog_client = httpx.AsyncClient(base_url=settings.CATALOG_SERVICE_URL)
    app.state.cache = RedisCache(settings.get_url_redis, settings.CACHE_TTL_SECONDS)
    app.state.payment_client = httpx.AsyncClient(base_url=settings.PAYMENT_SERVICE_URL)

    consumer = PaymentConsumer(
        url=settings.RABBIT_MQ_URL,
        exchange_name=settings.payment_exchange_name,
        queue_name=settings.payment_queue_name,
        routing_keys=[
            settings.payment_paid_routing_key,
            settings.payment_fail_routing_key,
            settings.payment_cancel_routing_key,
        ],
        cache=app.state.cache,
    )
    await consumer.connect()
    app.state.payment_consumer = consumer

    yield

    await consumer.close()
    await app.state.catalog_client.aclose()
    await app.state.cache.close()
    await app.state.payment_client.aclose()


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(cart_router)
app.include_router(order_router)


@app.get("/")
async def main():
    return {"message": "Welcome to Order-Service", "docs": "/docs"}


@app.get("/health/catalog")
async def health_catalog_client():
    client = CatalogClient(app.state.catalog_client)
    return await client.healthcheck()


@app.get("/health")
async def health():
    return {"status": "200"}
