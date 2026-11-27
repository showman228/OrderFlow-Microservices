from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="order_service/.env", extra="ignore")

    DEBUG: bool = True
    APP_NAME: str = "Order_service"

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str
    CACHE_TTL_SECONDS: int = 360

    RABBIT_MQ_URL: str = "amqp://guest:guest@localhost:5672"
    #payment_service
    payment_paid_routing_key: str = "payment.paid"
    payment_fail_routing_key: str = "payment.fail"
    payment_cancel_routing_key: str = "payment.cancel"
    payment_exchange_name: str = "payment.events"
    payment_queue_name: str = "payment.results"

    #notification_service
    order_exchange_name: str = "order.events"
    order_queue_name: str = "notification.orders"
    order_created_routring_key: str = "order.created"
    order_paid_routing_key: str = "order.paid"

    CORS_ORIGINS: list[str] | str = [
        "http://localhost:5174",
        "http://localhost:3001",
        "http://localhost:5501",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:5501",
    ]


    @property
    def get_url_db(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def get_url_redis(self) -> str:
        return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/0"

    CATALOG_SERVICE_URL: str = "http://catalog_service:8000" # запускаем через докер
    PAYMENT_SERVICE_URL: str = "http://payment_service:8003" # запускаем через докер


settings = Settings()
