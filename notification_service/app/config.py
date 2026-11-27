from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="notification_service/.env", extra="ignore")

    DEBUG: bool = True
    APP_NAME: str = "notification_service"

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    RABBIT_MQ_URL: str = "amqp://guest:guest@localhost:5672"
    order_exchange_name: str = "order.events"
    notification_queue_name: str = "notification.orders"
    order_created_routring_key: str = "order.created"
    order_paid_routing_key: str = "order.paid"


    CORS_ORIGINS: list[str] | str = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:5500",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5500",
    ]


    @property
    def get_url_db(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    ORDER_SERVICE_URL: str = "http://order_service:8001"


settings = Settings()