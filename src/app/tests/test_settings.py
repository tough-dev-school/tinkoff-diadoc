from app.settings import get_settings


def test_settings_read_env(monkeypatch):
    monkeypatch.setenv("DEBUG", "True")

    settings = get_settings()  # act

    assert settings.DEBUG is True
