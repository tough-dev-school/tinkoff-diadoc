from functools import partial
import json
import pytest

from app.models import BankAccount
from tinkoff_business.client import TinkoffBusinessClient


@pytest.fixture
def client():
    return TinkoffBusinessClient()


@pytest.fixture
def bank_accounts_json():
    with open("./tinkoff_business/tests/.fixtures/bank-accounts.json", "r") as fp:
        response_json = json.load(fp)

        response_json[0]["AccountNumber"] = "40802678901234567890"
        response_json[0]["AccountNumber"] = "100500"

        return response_json


@pytest.fixture
def mock_tinkoff_response(httpx_mock):
    return partial(httpx_mock.add_response, url="https://business.tinkoff.ru/openapi/api/v1/bank-accounts")


@pytest.fixture
def mock_http_get(mocker):
    return mocker.patch("tinkoff_business.http.TinkoffBusinessHTTP.get")


def test_http_get_method_used(client, mock_http_get):
    client.get_bank_accounts()

    mock_http_get.assert_called_once_with("bank-accounts")


def test_returns_bank_accounts(client, mock_tinkoff_response, bank_accounts_json):
    mock_tinkoff_response(json=bank_accounts_json)

    got = client.get_bank_accounts()

    assert len(got) == 2
    assert BankAccount(account_number="40802678901234567890") in got
    assert BankAccount(account_number="100500") in got
