from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Modern O365 Admin"
    auth_secret: str = "change-me"
    auth_algorithm: str = "HS256"
    auth_exp_minutes: int = 60
    database_url: str = "sqlite:///./data.db"
    graph_scope: str = "https://graph.microsoft.com/.default"

    class Config:
        env_prefix = "O365_"


@lru_cache
def get_settings() -> Settings:
    return Settings()
