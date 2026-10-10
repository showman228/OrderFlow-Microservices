from typing import List, Union
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="catalog_service/.env", extra="ignore")

    DEBUG: bool = True
    APP_NAME: str = "OrderFlow_Microservices"

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str 
    POSTGRES_HOST: str 
    POSTGRES_PORT: int 
    POSTGRES_DB: str

    CORS_ORIGIN: Union[List[str], str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:5500",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5500",
    ]

    static_dir: str = "catalog_service/static"
    images_dir: str = "catalog_service/static/images"

    @property
    def get_url_db(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()
