import pytest

from diadoc.client import DiadocClient


@pytest.fixture(autouse=True)
def _configure_diadoc_token(mocker):
    mocker.patch("diadoc.http.DiadocHTTP.get_token", return_value="sec7ret")


@pytest.fixture
def client():
    return DiadocClient()
