from datetime import datetime
from functools import partial
import pytest
import re
from zoneinfo import ZoneInfo

from app.models import LegalEntity


@pytest.fixture
def mock_tinkoff_response(httpx_mock, bank_statement_json):
    return partial(
        httpx_mock.add_response,
        url=re.compile(r"https://business.tinkoff.ru/openapi/api/v1/statement.*"),
        json=bank_statement_json,
    )


@pytest.fixture
def bank_statement_without_payer(bank_statement_json):
    bank_statement_json["operations"][0].pop("payer")
    return bank_statement_json


@pytest.fixture
def bank_statement_payer_empty_inn(bank_statement_json):
    bank_statement_json["operations"][0]["payer"].pop("inn")
    return bank_statement_json


def test_http_get_method_called_with_params(client, mock_http_get):
    client.get_payers_with_non_empty_inn("100400", from_date=datetime(2022, 9, 1, 23, 10, tzinfo=ZoneInfo("Asia/Magadan")))

    mock_http_get.assert_called_once_with(
        "/v1/statement",
        params={
            "accountNumber": "100400",
            "from": "2022-09-01T12:10:00Z",
        },
    )


@pytest.mark.freeze_time("2022-11-09 09:20Z")
def test_by_default_requests_bank_statement_from_for_last_24_hours(client, mock_http_get):
    client.get_payers_with_non_empty_inn("100990")  # no `from_date`

    mock_http_get.assert_called_once_with(
        "/v1/statement",
        params={
            "accountNumber": "100990",
            "from": "2022-11-08T09:20:00Z",
        },
    )


def test_get_payers_with_non_empty_inn_return_legal_entiry(client, mock_tinkoff_response):
    mock_tinkoff_response()

    got = client.get_payers_with_non_empty_inn("100500")

    assert got == [LegalEntity(name="ИП Котиков Александр Михайлович", inn="17499237465", kpp=None)]


def test_skip_operations_without_payer(client, mock_tinkoff_response, bank_statement_without_payer):
    mock_tinkoff_response(json=bank_statement_without_payer)

    got = client.get_payers_with_non_empty_inn("100500")

    assert got == []


def test_do_not_include_payers_with_empty_inn(client, mock_tinkoff_response, bank_statement_payer_empty_inn):
    mock_tinkoff_response(json=bank_statement_payer_empty_inn)

    got = client.get_payers_with_non_empty_inn("100500")

    assert got == []
