from functools import partial
import pytest

from app.models import LegalEntity


@pytest.fixture
def ya_legal_entity():
    return LegalEntity(name="ООО Машинка", inn="7788990011", kpp="1233454")


@pytest.fixture
def get_distinct_partners(tinkoff_to_diadoc, legal_entity):
    return partial(
        tinkoff_to_diadoc.get_distinct_partners_from_payers,
        payers=[legal_entity],
    )


@pytest.fixture(autouse=True)
def mock_diadoc_get_by_inn_kpp(mocker, partner, ya_partner):
    return mocker.patch("diadoc.client.DiadocClient.get_organizations_by_inn_kpp", return_value=[partner, ya_partner])


def test_return_diadoc_partners(get_distinct_partners, partner, ya_partner):
    got = get_distinct_partners()

    assert got == {partner, ya_partner}


def test_call_diadoc_get_by_inn_kpp_for_every_payer(get_distinct_partners, legal_entity, ya_legal_entity, mock_diadoc_get_by_inn_kpp, mocker):
    get_distinct_partners(payers=[legal_entity, ya_legal_entity])

    mock_diadoc_get_by_inn_kpp.assert_has_calls(
        calls=[
            mocker.call(inn=legal_entity.inn, kpp=legal_entity.kpp),
            mocker.call(inn=ya_legal_entity.inn, kpp=ya_legal_entity.kpp),
        ],
        any_order=True,
    )
