from functools import partial
import pytest

from app.models import LegalEntity


@pytest.fixture
def mock_tinkoff_response(httpx_mock):
    return partial(httpx_mock.add_response, url="https://business.tinkoff.ru/openapi/api/v1/company")


def test_http_get_method_used(client, mock_http_get):
    client.get_company()

    mock_http_get.assert_called_once_with("/v1/company")


def test_get_company(client, mock_tinkoff_response, company_json):
    mock_tinkoff_response(json=company_json)

    got = client.get_company()

    assert got == LegalEntity(name='ООО "Рога и Копыта"', inn="1234567890", kpp="123456789")


def test_get_company_without_kpp(client, mock_tinkoff_response, company_json):
    company_json["requisites"].pop("kpp")
    mock_tinkoff_response(json=company_json)

    got = client.get_company()

    assert got == LegalEntity(name='ООО "Рога и Копыта"', inn="1234567890", kpp=None)
