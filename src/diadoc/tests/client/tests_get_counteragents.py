from functools import partial
import pytest
import re

from diadoc.models import DiadocLegalEntity
from diadoc.models import PartnershipStatus


@pytest.fixture
def my_organization():
    return DiadocLegalEntity(
        name="Пивзавод",
        inn="771245768212",
        kpp=None,
        diadoc_id="75fcac12-ec63-4cdd-9076-87a8a2e6e8ba",
        is_active=True,
        is_roaming=False,
    )


@pytest.fixture
def page_one(get_diadoc_fixture):
    return get_diadoc_fixture("GetCounteragents_page_one.json")


@pytest.fixture
def page_two(get_diadoc_fixture):
    return get_diadoc_fixture("GetCounteragents_page_two.json")


@pytest.fixture(autouse=True)
def empty_page():
    return {"TotalCount": 0, "Counteragents": [], "TotalCountType": "Equal"}


@pytest.fixture
def mock_response(httpx_mock):
    return partial(
        httpx_mock.add_response,
        url=re.compile("https://diadoc-api.kontur.ru/V2/GetCounteragents.*"),
    )


@pytest.fixture
def get_counteragents(client, my_organization):
    return partial(client.get_counteragents, my_diadoc_id=my_organization.diadoc_id)


def test_get_counteragents_return_legal_entities(get_counteragents, mock_response, page_one, empty_page):
    mock_response(json=page_one)
    mock_response(json=empty_page)

    got = get_counteragents()

    assert got == [
        DiadocLegalEntity(
            name="Королевич В. Е.",
            inn="123456789012",  # same as dict key
            kpp=None,
            diadoc_id="229c4201-3680-4317-8a19-68d4748c0cd5",
            diadoc_partnership_status=PartnershipStatus.INVITE_SHOULD_BE_SEND,
            is_active=True,
            is_roaming=False,
        ),
        DiadocLegalEntity(
            name='ООО "Рога и рыльца"',
            inn="7744001499",  # same as dict key
            kpp="997950001",
            diadoc_id="aaddf4f0-6c13-4ddb-baf3-ad2265995365",
            diadoc_partnership_status=PartnershipStatus.ESTABLISHED,
            is_active=True,
            is_roaming=True,
        ),
    ]


def test_get_counteragents_from_all_pages(get_counteragents, mock_response, page_one, page_two, empty_page):
    mock_response(json=page_one)
    mock_response(json=page_two)
    mock_response(json=empty_page)

    got = get_counteragents()

    assert len(got) == 3


@pytest.mark.parametrize(
    ("diadoc_status", "expected"),
    [
        ("UnknownCounteragentStatus", PartnershipStatus.INVITE_SHOULD_BE_SEND),
        ("NotInCounteragentList", PartnershipStatus.INVITE_SHOULD_BE_SEND),
        ("InvitesMe", PartnershipStatus.INVITE_SHOULD_BE_SEND),
        ("IsMyCounteragent", PartnershipStatus.ESTABLISHED),
        ("IsInvitedByMe", PartnershipStatus.INVITE_WAS_SENT),
        ("RejectsMe", PartnershipStatus.REJECTED),
        ("IsRejectedByMe", PartnershipStatus.REJECTED),
    ],
)
def test_partnership_status_sets_correctly(get_counteragents, mock_response, page_two, empty_page, diadoc_status, expected):
    page_two["Counteragents"][0]["CurrentStatus"] = diadoc_status
    mock_response(json=page_two)
    mock_response(json=empty_page)

    legal_entity = get_counteragents()[0]

    assert legal_entity.diadoc_partnership_status == expected


def test_my_org_id_param_in_every_request(get_counteragents, mock_response, empty_page, httpx_mock):
    mock_response(json=empty_page)

    get_counteragents()

    request_query = httpx_mock.get_request().url.query
    assert b"myOrgId=75fcac12-ec63-4cdd-9076-87a8a2e6e8ba" in request_query


def test_to_get_next_page_set_after_index_key_param(get_counteragents, mock_response, page_two, empty_page, httpx_mock):
    mock_response(json=page_two)
    mock_response(json=empty_page)

    get_counteragents()

    second_request_query = httpx_mock.get_requests()[1].url.query
    assert b"afterIndexKey=08D8000B66C83D09602000EE6E4BB1418BAFB2DAD792C0D7" in second_request_query
