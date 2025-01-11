import pytest
from uuid import uuid4

from diadoc.models import DiadocPartner
from tinkoff_to_diadoc.exceptions import TinkoffToDiadocException


@pytest.fixture
def partner_matched_legal_entity(legal_entity):
    return DiadocPartner(
        name="ООО Какое-то имя",
        inn=legal_entity.inn,
        kpp=legal_entity.kpp,
        diadoc_id=str(uuid4()),
        diadoc_box_id=str(uuid4()),
        diadoc_partnership_status=None,
        is_active=True,
        is_roaming=False,
    )


@pytest.fixture(autouse=True)
def mock_tinkoff_get_company(mocker, legal_entity):
    return mocker.patch("tinkoff_business.client.TinkoffBusinessClient.get_company", return_value=legal_entity)


@pytest.fixture
def mock_diadoc_get_my_organizations(mocker):
    return lambda *partners: mocker.patch("diadoc.client.DiadocClient.get_my_organizations", return_value=partners)


def test_return_partner_matched_tinkoff_company(tinkoff_to_diadoc, mock_diadoc_get_my_organizations, partner_matched_legal_entity, ya_partner):
    mock_diadoc_get_my_organizations(partner_matched_legal_entity, ya_partner)

    my_company = tinkoff_to_diadoc.my_company

    assert my_company == partner_matched_legal_entity


def test_raise_if_no_partners_found_matched_tinkoff(tinkoff_to_diadoc, mock_diadoc_get_my_organizations, ya_partner):
    mock_diadoc_get_my_organizations(ya_partner)

    with pytest.raises(TinkoffToDiadocException, match="Did not find"):
        tinkoff_to_diadoc.my_company


def test_call_tinkoff_and_diadoc_clients(tinkoff_to_diadoc, mock_diadoc_get_my_organizations, partner_matched_legal_entity, mock_tinkoff_get_company):
    mock_diadoc = mock_diadoc_get_my_organizations(partner_matched_legal_entity)

    tinkoff_to_diadoc.my_company

    mock_diadoc.assert_called_once()
    mock_tinkoff_get_company.assert_called_once()
