from functools import partial
import pytest

from app.models import BankAccount


@pytest.fixture
def mock_tinkoff_response(httpx_mock, bank_accounts_json):
    return partial(
        httpx_mock.add_response,
        url="https://business.tinkoff.ru/openapi/api/v1/bank-accounts",
        json=bank_accounts_json,
    )


def test_http_get_method_used(client, mock_http_get):
    client.get_bank_accounts()

    mock_http_get.assert_called_once_with("bank-accounts")


def test_returns_bank_accounts(client, mock_tinkoff_response):
    mock_tinkoff_response()

    got = client.get_bank_accounts()

    assert got == [
        BankAccount(account_number="40802678901234567890"),
        BankAccount(account_number="100500"),
    ]
