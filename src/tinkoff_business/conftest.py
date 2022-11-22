import pytest


@pytest.fixture(autouse=True)
def _set_tinkoff_token(monkeypatch):
    monkeypatch.setenv("TINKOFF_BUSINESS_TOKEN", "se7ret")
