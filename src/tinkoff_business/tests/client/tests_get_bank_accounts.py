from functools import partial
import pytest

from app.models import BankAccount
from tinkoff_business.client import TinkoffBusinessClient
from tinkoff_business.services import TinkoffBankAccountGetter


@pytest.fixture
def client():
    return TinkoffBusinessClient()


@pytest.fixture
def mock_tinkoff_response(httpx_mock, bank_accounts_json):
    return partial(
        httpx_mock.add_response,
        url="https://business.tinkoff.ru/openapi/api/v1/bank-accounts",
        json=bank_accounts_json,
    )


@pytest.fixture
def mock_http_get(mocker):
    return mocker.patch("tinkoff_business.http.TinkoffBusinessHTTP.get")


@pytest.fixture
def spy_tinkoff_bank_account_getter(mocker):
    return mocker.spy(TinkoffBankAccountGetter, "__call__")


def test_http_get_method_used(client, mock_http_get):
    client.get_bank_accounts()

    mock_http_get.assert_called_once_with("bank-accounts")


def test_call_service_to_get_list_entity(client, mock_tinkoff_response, spy_tinkoff_bank_account_getter):
    mock_tinkoff_response()

    client.get_bank_accounts()

    spy_tinkoff_bank_account_getter.assert_called_once()


def test_returns_bank_accounts(client, mock_tinkoff_response):
    mock_tinkoff_response()

    got = client.get_bank_accounts()

    assert len(got) == 2
    assert BankAccount(account_number="40802678901234567890") in got
    assert BankAccount(account_number="100500") in got
