from functools import partial
import pytest
import re

from diadoc.models import DiadocPartner


@pytest.fixture
def mock_diadoc_response(httpx_mock, get_diadoc_fixture):
    return partial(
        httpx_mock.add_response,
        url=re.compile(r"https://diadoc-api.kontur.ru/GetOrganizationsByInnKpp.*"),
        json=get_diadoc_fixture("GetOrganizationsByInnKpp.json"),
    )


@pytest.fixture
def get_organizations(client):
    return partial(client.get_organizations_by_inn_kpp, inn="7710140679", kpp="771301001")


def test_get_inn_kpp_organizations_return_diadoc_partners(get_organizations, mock_diadoc_response):
    mock_diadoc_response()

    got = get_organizations()

    assert got == [
        DiadocPartner(
            name='АО "ТИНЬКОФФ БАНК"',
            inn="7710140679",
            kpp="771301001",
            diadoc_id="8e165910-7ee8-4dc8-9d96-af7df4e8e0cd",
            diadoc_box_id="2700ef9e-0108-4619-8d3e-74463cedc6c2",
            is_active=True,
            is_roaming=True,
        ),
        DiadocPartner(
            name='АО "ТИНЬКОФФ БАНК"',
            inn="7710140679",
            kpp="771301001",
            diadoc_id="a3e04137-55f3-4324-87d2-35c437a2d15a",
            diadoc_box_id="4f7ce8b1-5761-4cb9-86ef-87ac132e45cb",
            is_active=True,
            is_roaming=False,
        ),
    ]


@pytest.mark.parametrize(
    ("inn", "kpp", "expected_query"),
    [
        ("77112233", "100500", b"inn=77112233&kpp=100500"),
        ("77112233", None, b"inn=77112233"),
        ("77112233", "", b"inn=77112233"),
    ],
)
def test_request_query_params_correct(client, mock_diadoc_response, httpx_mock, inn, kpp, expected_query):
    mock_diadoc_response()

    client.get_organizations_by_inn_kpp(inn=inn, kpp=kpp)

    assert httpx_mock.get_request().url.query == expected_query
