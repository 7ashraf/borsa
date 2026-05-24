import pytest

from borsa.data.symbols import (
    EGX_SYMBOLS,
    all_symbols,
    get_symbol_name,
    get_yahoo_ticker,
    is_valid_symbol,
)


def test_egx_symbols_not_empty() -> None:
    assert len(EGX_SYMBOLS) > 0


def test_known_symbol_is_valid() -> None:
    assert is_valid_symbol("COMI") is True


def test_case_insensitive_validation() -> None:
    assert is_valid_symbol("comi") is True


def test_unknown_symbol_is_invalid() -> None:
    assert is_valid_symbol("NOTREAL") is False


def test_get_yahoo_ticker_known() -> None:
    ticker = get_yahoo_ticker("COMI")
    assert ticker == "COMI.CA"


def test_get_yahoo_ticker_unknown() -> None:
    assert get_yahoo_ticker("NOTREAL") is None


def test_get_symbol_name_known() -> None:
    name = get_symbol_name("COMI")
    assert name == "Commercial International Bank"


def test_all_symbols_returns_list() -> None:
    result = all_symbols()
    assert isinstance(result, list)
    assert len(result) == len(EGX_SYMBOLS)


def test_all_symbols_have_required_keys() -> None:
    for entry in all_symbols():
        assert "symbol" in entry
        assert "yahoo_ticker" in entry
        assert "name" in entry


def test_every_symbol_has_yahoo_ticker() -> None:
    for sym, meta in EGX_SYMBOLS.items():
        assert "yahoo_ticker" in meta, f"{sym} missing yahoo_ticker"
        assert meta["yahoo_ticker"].endswith(".CA"), f"{sym} yahoo_ticker should end with .CA"
