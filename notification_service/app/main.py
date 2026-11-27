from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from notification_service.app.database import init_db
from notification_service.app.config import settings
from notification_service.app.routers.notification import router as notification_router
from notification_service.app.consumer import NotificationConsumer
from notification_service.app.api_clients.order_client import OrderClient
import httpx

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    app.state.order_client = httpx.AsyncClient(base_url=settings.ORDER_SERVICE_URL)
    consumer = NotificationConsumer(
            url=settings.RABBIT_MQ_URL,
            exchange_name=settings.order_exchange_name,
            queue_name=settings.notification_queue_name,
            routing_keys=[
                settings.order_paid_routing_key,
                settings.order_created_routring_key
            ],
            order_client=OrderClient(app.state.order_client)
        )
    await consumer.connect()
    yield
    await consumer.close()
    await app.state.order_client.aclose()


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notification_router)

@app.get("/")
async def main():
    return {"message": "Welcome to Notification-Service", "docs": "/docs"}


@app.get("/health")
async def health():
    return {"status": "200"}