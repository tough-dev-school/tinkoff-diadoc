from functools import partial
import pytest

from diadoc.models import DiadocPartner


@pytest.fixture
def get_my_organizations_json(get_diadoc_fixture):
    return get_diadoc_fixture("GetMyOrganizations.json")


@pytest.fixture
def mock_diadoc_response(httpx_mock, get_my_organizations_json):
    return partial(
        httpx_mock.add_response,
        url="https://diadoc-api.kontur.ru/GetMyOrganizations",
        json=get_my_organizations_json,
    )


def test_get_my_organizations_return_diadoc_partners(client, mock_diadoc_response):
    mock_diadoc_response()

    diadoc_partners = client.get_my_organizations()

    assert diadoc_partners == [
        DiadocPartner(
            name="Королевич В. Е.",
            inn="123456789012",
            kpp=None,
            diadoc_id="229c4201-3680-4317-8a19-68d4748c0cd5",
            is_active=True,
            is_roaming=False,
        ),
        DiadocPartner(
            name='ООО "Рога и рыльца"',
            inn="7744001499",
            kpp="997950001",
            diadoc_id="aaddf4f0-6c13-4ddb-baf3-ad2265995365",
            is_active=True,
            is_roaming=True,
        ),
    ]
