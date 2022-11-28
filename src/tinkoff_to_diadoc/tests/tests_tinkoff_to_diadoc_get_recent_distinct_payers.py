from functools import partial
import pytest

from app.models import LegalEntity


@pytest.fixture
def ya_entity():
    return LegalEntity(name="ООО Белые вороны", inn="7499558899", kpp="899988998")


@pytest.fixture
def mock_tinkoff_get_payers(mocker):
    return mocker.patch("tinkoff_business.client.TinkoffBusinessClient.get_payers", return_value=[])


@pytest.fixture
def get_distinct_payers(tinkoff_to_diadoc, bank_account, diadoc_entity):
    return partial(
        tinkoff_to_diadoc.get_recent_distinct_payers,
        bank_accounts=[bank_account],
        my_company=diadoc_entity,
    )


def test_get_payers_with_args_is_called(get_distinct_payers, bank_account, ya_bank_account, mock_tinkoff_get_payers, mocker):
    get_distinct_payers(bank_accounts=[bank_account, ya_bank_account])

    mock_tinkoff_get_payers.assert_has_calls(
        calls=[
            mocker.call(account_number="100500", exclude_payer_inn="772354588891"),
            mocker.call(account_number="900500", exclude_payer_inn="772354588891"),
        ],
        any_order=True,
    )


def test_return_distinct_payers(mock_tinkoff_get_payers, get_distinct_payers, entity, ya_entity):
    mock_tinkoff_get_payers.side_effect = [
        [entity, ya_entity, entity, entity],  # tinkoff `get_payers` returns several payments from same company
    ]

    distinct_payers = get_distinct_payers()

    assert distinct_payers == [entity, ya_entity]
