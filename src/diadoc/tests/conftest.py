import pytest


@pytest.fixture(autouse=True)
def _set_diadoc_credentials(monkeypatch):
    monkeypatch.setenv("DIADOC_LOGIN", "diadoc-superman@company.com")
    monkeypatch.setenv("DIADOC_PASSWORD", "diadoc-super-password")
    monkeypatch.setenv("DIADOC_CLIENT_ID", "API-client-id")
