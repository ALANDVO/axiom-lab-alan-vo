from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "freehire"
    environment: str = "development"
    database_url: str = "sqlite:///./freehire.db"
    demo_mode: bool = True
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    # LLM (optional, opt-in)
    llm_api_key: str | None = None
    llm_provider: str | None = None
    llm_model: str | None = None
    llm_base_url: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()