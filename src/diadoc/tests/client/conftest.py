import pytest

from diadoc.client import DiadocClient


@pytest.fixture(autouse=True)
def _configure_diadoc_env(set_env_variable):
    set_env_variable("DIADOC_LOGIN", "email@example.com")
    set_env_variable("DIADOC_PASSWORD", "PASS700")
    set_env_variable("DIADOC_CLIENT_ID", "API-CLIENT-ID")


@pytest.fixture(autouse=True)
def _configure_diadoc_token(mocker):
    mocker.patch("diadoc.http.DiadocHTTP.get_token", return_value="sec7ret")


@pytest.fixture
def client():
    return DiadocClient()
