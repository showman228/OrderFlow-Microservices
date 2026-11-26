from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="payment_service/.env", extra="ignore")

    DEBUG: bool = True
    APP_NAME: str = "payment_service"

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    PAYMENT_DELAY_SECONDS: float = 2.0

    RABBIT_MQ_URL: str = "amqp://guest:guest@localhost:5672"
    payment_paid_routing_key: str = "payment.paid"
    payment_fail_routing_key: str = "payment.fail"
    payment_cancel_routing_key: str = "payment.cancel"
    payment_exchange_name: str = "payment.events"
    payment_queue_name: str = "payment.results"


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


settings = Settings()
