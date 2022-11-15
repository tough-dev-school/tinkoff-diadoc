import pytest

from config import get_settings


@pytest.fixture
def _set_settings_debug_true(monkeypatch):
    get_settings.cache_clear()

    monkeypatch.setenv("DEBUG", "True")
    yield

    get_settings.cache_clear()


def test_read_settings():
    settings = get_settings()

    assert hasattr(settings, "DEBUG") is True
    assert settings.DEBUG is False


@pytest.mark.usefixtures("_set_settings_debug_true")
def test_read_environment_settings():
    settings = get_settings()

    assert settings.DEBUG is True
