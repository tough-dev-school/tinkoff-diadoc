from functools import partial
import pytest

from tinkoff_business.exceptions import TinkoffBusinessHTTPException
from tinkoff_business.http import TinkoffBusinessHTTP


@pytest.fixture
def http():
    return TinkoffBusinessHTTP()


@pytest.fixture
def mock_tinkoff_url(httpx_mock):
    return partial(
        httpx_mock.add_response,
        method="GET",
        url="https://business.tinkoff.ru/openapi/api/v1/url",
        json={"ok": True},
    )


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("/test/get", "https://business.tinkoff.ru/openapi/api/v1/test/get"),
        ("test/get", "https://business.tinkoff.ru/openapi/api/v1/test/get"),
        ("test/get/", "https://business.tinkoff.ru/openapi/api/v1/test/get"),
        ("/test/get/", "https://business.tinkoff.ru/openapi/api/v1/test/get"),
        ("test/get/?par=val", "https://business.tinkoff.ru/openapi/api/v1/test/get/?par=val"),
    ],
)
def test_format_url(url, expected, http):
    assert http.format_url(url) == expected


def test_get_method_requests_tinkoff_url_and_receives_data(mock_tinkoff_url, http):
    mock_tinkoff_url()

    got = http.get("url")

    assert got["ok"] is True


@pytest.mark.parametrize(
    ("query_params", "url"),
    [
        (
            {"par": "val"},
            "https://business.tinkoff.ru/openapi/api/v1/test/get?par=val",
        ),
        (
            {
                "par": "val",
                "par2": "val2",
            },
            "https://business.tinkoff.ru/openapi/api/v1/test/get?par=val&par2=val2",
        ),
    ],
)
def test_get_method_with_query_params_requests_right_url(mock_tinkoff_url, http, query_params, url):
    mock_tinkoff_url(url=url)

    got = http.get("test/get", params=query_params)

    assert got["ok"] is True


def test_post_method_requests_tinkoff_url(mock_tinkoff_url, http):
    mock_tinkoff_url(method="POST", status_code=201)

    got = http.post("url")

    assert got["ok"] is True


def test_post_method_sends_payload_to_tinkoff(mock_tinkoff_url, http, httpx_mock):
    mock_tinkoff_url(method="POST", status_code=201)

    http.post("url", payload={"key": "value"})

    request_content = httpx_mock.get_request().content
    assert request_content == b'{"key": "value"}'


@pytest.mark.parametrize(
    ("method", "status_code", "http_api_call"),
    [
        ("POST", 201, lambda http: http.post("url")),
        ("GET", 200, lambda http: http.get("url")),
    ],
)
def test_authorization_headers_set_right(method, status_code, http_api_call, mock_tinkoff_url, http, httpx_mock):
    mock_tinkoff_url(method=method, status_code=status_code)

    http_api_call(http)

    request_headers = httpx_mock.get_request().headers
    assert "Authorization" in request_headers
    assert request_headers["Authorization"] == "Bearer se7ret"


def test_raise_if_tinkoff_api_return_error_message(mock_tinkoff_url, http):
    mock_tinkoff_url(
        json={
            "errorId": "retw6789",
            "errorCode": "TINKOFF_ERROR_CODE",
            "errorMessage": "Ошибка от Tinkoff Business",
        }
    )

    with pytest.raises(TinkoffBusinessHTTPException, match="Ошибка от Tinkoff Business"):
        http.get("url")


def test_raise_if_not_expected_status_code(mock_tinkoff_url, http):
    mock_tinkoff_url(json={"key": "some valid json"})

    with pytest.raises(TinkoffBusinessHTTPException, match="Non-expected HTTP response from tinkoff: 200"):
        http.get("url", expected_status_code=202)


def test_raise_readable_error_if_non_json_response(mock_tinkoff_url, http):
    mock_tinkoff_url(text="Non JSON serializable content")

    with pytest.raises(TinkoffBusinessHTTPException, match="not a valid JSON"):
        http.get("url")
