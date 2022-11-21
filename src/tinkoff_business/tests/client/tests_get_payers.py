from datetime import date
from functools import partial
import json
import pytest
import re

from app.models import LegalEntity
from tinkoff_business.client import TinkoffBusinessClient


@pytest.fixture
def client():
    return TinkoffBusinessClient()


@pytest.fixture
def bank_statement_json():
    with open("./tinkoff_business/tests/.fixtures/bank-statement.json") as fp:
        bank_statement_response = json.load(fp)

        bank_statement_response["operation"][0]["payerName"] = "Петрова Александра Ивановна"
        bank_statement_response["operation"][0]["payerInn"] = "100500"
        bank_statement_response["operation"][0].pop("payerKpp", None)

        bank_statement_response["operation"][1]["payerName"] = 'ООО "ПЕРЧИК"'
        bank_statement_response["operation"][1]["payerInn"] = "900600"
        bank_statement_response["operation"][1]["payerKpp"] = "200500"

        return bank_statement_response


@pytest.fixture
def mock_tinkoff_response(httpx_mock):
    return partial(
        httpx_mock.add_response,
        url=re.compile(r"https://business.tinkoff.ru/openapi/api/v1/bank-statement.*"),
    )


@pytest.fixture
def mock_http_get(mocker):
    return mocker.patch("tinkoff_business.http.TinkoffBusinessHTTP.get")


def test_http_get_method_called_with_params(client, mock_http_get):
    client.get_payers("100400", from_date=date(2022, 9, 1), till_date=date(2022, 10, 11))

    mock_http_get.assert_called_once_with(
        "bank-statement",
        params={
            "accountNumber": "100400",
            "from": "2022-09-01",
            "till": "2022-10-11",
        },
    )


@pytest.mark.freeze_time("2022-11-09")
def test_by_default_requests_bank_statement_from_yesterday_till_today(client, mock_http_get):
    client.get_payers("100400")  # no `from_date` and `till_date` provided

    mock_http_get.assert_called_once_with(
        "bank-statement",
        params={
            "accountNumber": "100400",
            "from": "2022-11-08",
            "till": "2022-11-09",
        },
    )


def test_payers(client, mock_tinkoff_response, bank_statement_json):
    mock_tinkoff_response(json=bank_statement_json)

    got = client.get_payers("100500")

    assert len(got) == 2
    assert LegalEntity(name="Петрова Александра Ивановна", inn="100500", kpp=None) in got
    assert LegalEntity(name='ООО "ПЕРЧИК"', inn="900600", kpp="200500") in got
