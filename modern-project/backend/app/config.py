from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    client_id: str | None = None
    client_secret: str | None = None
    tenant_id: str | None = None
    authority_host: str = "https://login.microsoftonline.com"
    redirect_uri: str = "http://localhost:8000/auth/callback"
    graph_scope: str = "https://graph.microsoft.com/.default"
    default_domain: str | None = None

    model_config = SettingsConfigDict(env_prefix="O365_", env_file=".env", extra="ignore")


settings = Settings()
