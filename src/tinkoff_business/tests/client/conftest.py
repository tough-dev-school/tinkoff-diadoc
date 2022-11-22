import json
import pytest

from tinkoff_business.client import TinkoffBusinessClient


@pytest.fixture
def company_json():
    with open("./tinkoff_business/tests/.fixtures/company.json", "r") as fp:
        return json.load(fp)


@pytest.fixture
def bank_accounts_json():
    with open("./tinkoff_business/tests/.fixtures/bank-accounts.json", "r") as fp:
        return json.load(fp)


@pytest.fixture
def bank_statement_json():
    with open("./tinkoff_business/tests/.fixtures/bank-statement.json") as fp:
        return json.load(fp)


@pytest.fixture
def mock_http_get(mocker):
    return mocker.patch("tinkoff_business.http.TinkoffBusinessHTTP.get")


@pytest.fixture
def client():
    return TinkoffBusinessClient()
