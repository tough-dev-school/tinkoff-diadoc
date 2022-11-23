import json
import pytest

from tinkoff_business.client import TinkoffBusinessClient


@pytest.fixture
def get_fixture():
    def _load(filename: str):
        with open(f"./tinkoff_business/tests/.fixtures/{filename}", "r") as fp:
            return json.load(fp)

    return _load


@pytest.fixture
def company_json(get_fixture):
    return get_fixture("company.json")


@pytest.fixture
def bank_accounts_json(get_fixture):
    return get_fixture("bank-accounts.json")


@pytest.fixture
def bank_statement_json(get_fixture):
    return get_fixture("bank-statement.json")


@pytest.fixture
def mock_http_get(mocker):
    return mocker.patch("tinkoff_business.http.TinkoffBusinessHTTP.get")


@pytest.fixture
def client():
    return TinkoffBusinessClient()
