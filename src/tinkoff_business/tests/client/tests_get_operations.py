from datetime import date
from functools import partial
import pytest
import re

from tinkoff_business.client import TinkoffBusinessClient


@pytest.fixture
def client():
    return TinkoffBusinessClient()


@pytest.fixture
def bank_statement_json():
    return {
        "accountNumber": "40802678901234567890",
        "saldoIn": 500,
        "income": 500,
        "outcome": 500,
        "saldoOut": 500,
        "operation": [
            {
                "operationId": "12345_89765",
                "id": "1234567890123456789",
                "date": "2015-04-01",
                "amount": 500,
                "drawDate": "2015-05-01",
                "payerName": "Иванов Иван Иванович",
                "payerInn": "987654321987",
                "payerAccount": "99998888777766665555",
                "payerCorrAccount": "40244447777333300000",
                "payerBic": "76543277778",
                "payerBank": "банк 'Лидеров'",
                "chargeDate": "2015-09-03",
                "recipient": "Петров Петр Петрович",
                "recipientInn": "765432198765",
                "recipientAccount": "77774444222277772222",
                "recipientCorrAccount": "40299998888777700000",
                "recipientBic": "12345678901",
                "recipientBank": "банк 'Чемпионов'",
                "paymentType": "",
                "operationType": "01",
                "uin": "0",
                "paymentPurpose": "материальная помощь",
                "creatorStatus": "",
                "kbk": "44445555666677778888",
                "oktmo": "44445555",
                "taxEvidence": "ТП",
                "taxPeriod": "ГД.00.2019",
                "taxDocNumber": "0",
                "taxDocDate": "0",
                "taxType": "taxType",
                "executionOrder": "5",
            },
        ],
    }


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
    client.get_operations("100400", from_date=date(2022, 9, 1), till_date=date(2022, 10, 11))

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
    client.get_operations("100400")  # no `from_date` and `till_date` provided

    mock_http_get.assert_called_once_with(
        "bank-statement",
        params={
            "accountNumber": "100400",
            "from": "2022-11-08",
            "till": "2022-11-09",
        },
    )


def test_return_operations_only(client, mock_tinkoff_response, bank_statement_json):
    mock_tinkoff_response(json=bank_statement_json)

    got = client.get_operations("100500")

    assert got == bank_statement_json["operation"]
