from functools import partial
import pytest

from diadoc.client import DiadocClient


@pytest.fixture
def get_diadoc_fixture(get_fixture):
    return partial(get_fixture, directory_path="./diadoc/tests/.fixtures/")


@pytest.fixture
def client(mocker):
    mocker.patch("diadoc.http.DiadocHTTP.token", return_value="TOKEN", new_callable=mocker.PropertyMock)
    return DiadocClient()
