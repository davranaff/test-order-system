from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "restaurant_db"

    log_level: str = "INFO"
    log_file: str = "app.log"

    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True

    cors_origins: list = ["http://localhost:3000", "http://localhost:8080"]

    enable_metrics: bool = True
    metrics_port: int = 9090

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()