from functools import partial
import pytest

from app.models import LegalEntity


@pytest.fixture
def my_company(partner):
    return partner


@pytest.fixture
def ya_legal_entity():
    return LegalEntity(name="ООО Белые вороны", inn="7499558899", kpp="899988998")


@pytest.fixture(autouse=True)
def mock_tinkoff_get_payers(mocker, legal_entity, ya_legal_entity):
    return mocker.patch(
        "tinkoff_business.client.TinkoffBusinessClient.get_payers_with_non_empty_inn",
        return_value=[legal_entity, legal_entity, ya_legal_entity],  # return `legal_entity` twice
    )


@pytest.fixture
def get_distinct_payers(tinkoff_to_diadoc, bank_account, my_company):
    return partial(
        tinkoff_to_diadoc.get_recent_distinct_payers,
        bank_accounts=[bank_account],
        my_company=my_company,
    )


def test_return_distinct_payers(get_distinct_payers, legal_entity, ya_legal_entity):
    distinct_payers = get_distinct_payers()

    assert distinct_payers == {legal_entity, ya_legal_entity}  # the return is set that excludes duplicates


def test_my_company_is_excluded_from_distinct_payers(get_distinct_payers, legal_entity, my_company, mock_tinkoff_get_payers):
    mock_tinkoff_get_payers.return_value = [legal_entity, my_company]

    distinct_payers = get_distinct_payers()

    assert distinct_payers == {legal_entity}


def test_get_payers_with_args_is_called(get_distinct_payers, bank_account, ya_bank_account, mock_tinkoff_get_payers, mocker):
    get_distinct_payers(bank_accounts=[bank_account, ya_bank_account])

    mock_tinkoff_get_payers.assert_has_calls(
        calls=[
            mocker.call(account_number="100500"),
            mocker.call(account_number="900500"),
        ],
        any_order=True,
    )
