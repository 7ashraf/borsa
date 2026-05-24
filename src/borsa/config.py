from __future__ import annotations
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Provider keys for /v1 endpoints — user brings their own
    alpha_vantage_key: str = ""
    finnhub_key: str = ""

    # Operator-controlled keys used exclusively for the /demo endpoint
    demo_alpha_vantage_key: str = ""
    demo_finnhub_key: str = ""

    # Logging
    log_level: str = "info"
    dev_mode: bool = False   # pretty console output when True

    # Cache
    cache_ttl_seconds: int = 300
    demo_cache_ttl_seconds: int = 600
    cache_max_size: int = 512
    fetch_quotes_on_startup: bool = True
    auto_refresh_quotes: bool = True
    enable_yahoo_finance: bool = False

    # Demo rate limiting
    demo_daily_limit: int = 50

    # CORS
    cors_origins: list[str] = ["*"]

    # Server
    host: str = "0.0.0.0"
    port: int = 8000


settings = Settings()
