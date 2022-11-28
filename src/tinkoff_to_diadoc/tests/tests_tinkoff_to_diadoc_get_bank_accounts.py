import pytest


@pytest.fixture(autouse=True)
def mock_tinkoff_get_bank_accounts(mocker, bank_account, ya_bank_account):
    return mocker.patch("tinkoff_business.client.TinkoffBusinessClient.get_bank_accounts", return_value=[bank_account, ya_bank_account])


def test_return_bank_accounts(tinkoff_to_diadoc, bank_account, ya_bank_account):
    got = tinkoff_to_diadoc.get_bank_accounts()

    assert got == [bank_account, ya_bank_account]


def test_tinkoff_client_was_called(tinkoff_to_diadoc, mock_tinkoff_get_bank_accounts):
    tinkoff_to_diadoc.get_bank_accounts()

    mock_tinkoff_get_bank_accounts.assert_called_once()
