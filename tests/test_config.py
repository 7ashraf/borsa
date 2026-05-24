from borsa.config import Settings


def test_default_settings() -> None:
    s = Settings()
    assert s.port == 8000
    assert s.host == "0.0.0.0"
    assert s.cache_ttl_seconds == 300
    assert s.demo_cache_ttl_seconds == 600
    assert s.fetch_quotes_on_startup is True
    assert s.auto_refresh_quotes is True
    assert s.enable_yahoo_finance is False
    assert s.demo_daily_limit == 50
    assert s.log_level == "info"
    assert s.dev_mode is False


def test_empty_key_means_no_provider() -> None:
    s = Settings(alpha_vantage_key="", finnhub_key="")
    assert s.alpha_vantage_key == ""
    assert s.finnhub_key == ""


def test_demo_keys_are_independent() -> None:
    s = Settings(
        alpha_vantage_key="user-key",
        demo_alpha_vantage_key="demo-key",
    )
    assert s.alpha_vantage_key == "user-key"
    assert s.demo_alpha_vantage_key == "demo-key"


def test_cors_origins_default_to_wildcard() -> None:
    s = Settings()
    assert "*" in s.cors_origins
