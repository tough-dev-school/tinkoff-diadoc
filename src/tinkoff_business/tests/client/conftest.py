from functools import partial
import pytest

from tinkoff_business.client import TinkoffBusinessClient


@pytest.fixture
def get_tinkoff_fixture(get_fixture):
    return partial(get_fixture, directory_path="./tinkoff_business/tests/.fixtures/")


@pytest.fixture
def company_json(get_tinkoff_fixture):
    return get_tinkoff_fixture("company.json")


@pytest.fixture
def bank_accounts_json(get_tinkoff_fixture):
    return get_tinkoff_fixture("bank-accounts.json")


@pytest.fixture
def bank_statement_json(get_tinkoff_fixture):
    return get_tinkoff_fixture("statement.json")


@pytest.fixture
def mock_http_get(mocker):
    return mocker.patch("tinkoff_business.http.TinkoffBusinessHTTP.get")


@pytest.fixture
def client():
    return TinkoffBusinessClient()
