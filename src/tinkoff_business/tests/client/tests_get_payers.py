from datetime import date
from functools import partial
import pytest
import re

from app.models import LegalEntity


@pytest.fixture
def mock_tinkoff_response(httpx_mock, bank_statement_json):
    return partial(
        httpx_mock.add_response,
        url=re.compile(r"https://business.tinkoff.ru/openapi/api/v1/bank-statement.*"),
        json=bank_statement_json,
    )


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
    client.get_payers("100990")  # no `from_date` and `till_date` provided

    mock_http_get.assert_called_once_with(
        "bank-statement",
        params={
            "accountNumber": "100990",
            "from": "2022-11-08",
            "till": "2022-11-09",
        },
    )


def test_get_payers_return(client, mock_tinkoff_response):
    mock_tinkoff_response()

    got = client.get_payers("100500")

    assert got == [
        LegalEntity(name="Иванов Иван Иванович", inn="987654321987", kpp=None),
        LegalEntity(name='ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ "ПЕРЧИК"', inn="7725289900", kpp="123456789"),
    ]


def test_exclude_payer_inn(client, mock_tinkoff_response):
    mock_tinkoff_response()

    got = client.get_payers(account_number="100500", exclude_payer_inn="7725289900")

    assert got == [
        LegalEntity(name="Иванов Иван Иванович", inn="987654321987", kpp=None),
    ]
