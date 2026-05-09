from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    app_name: str = "AllInOne Backend"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    database_url: str
    redis_url: str = "redis://192.168.2.112:6379/0"
    redis_max_connections: int = 50

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()