from functools import partial
import pytest

from diadoc.client import DiadocClient
from diadoc.models import DiadocPartner


@pytest.fixture
def get_diadoc_fixture(get_fixture):
    return partial(get_fixture, directory_path="./diadoc/tests/.fixtures/")


@pytest.fixture
def client(mocker):
    mocker.patch("diadoc.http.DiadocHTTP.token", return_value="TOKEN", new_callable=mocker.PropertyMock)
    return DiadocClient()


@pytest.fixture
def my_organization():
    return DiadocPartner(
        name="Пивзавод",
        inn="771245768212",
        kpp=None,
        diadoc_id="75fcac12-ec63-4cdd-9076-87a8a2e6e8ba",
        diadoc_box_id="1ecf0eca-bfe3-4153-96a3-4ee0e72b69ed",
        is_active=True,
        is_roaming=False,
    )
