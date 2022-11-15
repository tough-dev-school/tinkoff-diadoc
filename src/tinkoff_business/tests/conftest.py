import pytest

from config.settings import get_settings


@pytest.fixture
def set_env_variable(monkeypatch):
    def _set_env_variable(env_name, env_value):
        get_settings.cache_clear()
        monkeypatch.setenv(env_name, env_value)

    yield _set_env_variable

    get_settings.cache_clear()


@pytest.fixture(autouse=True)
def _set_env_tinkoff_token(set_env_variable):
    set_env_variable("TINKOFF_BUSINESS_TOKEN", "se7ret")
