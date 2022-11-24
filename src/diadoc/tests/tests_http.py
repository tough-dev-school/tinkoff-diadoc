from functools import partial
import pytest

from diadoc.exceptions import DiadocHTTPException
from diadoc.http import DiadocHTTP


@pytest.fixture
def http():
    return DiadocHTTP()


@pytest.fixture
def http_authorized(http):
    http.token = "TOKEN"
    return http


@pytest.fixture
def mock_diadoc_url(httpx_mock):
    return partial(
        httpx_mock.add_response,
        method="GET",
        url="https://diadoc-api.kontur.ru/url",
        json={"ok": True},
    )


@pytest.fixture
def mock_diadoc_auth_api(httpx_mock):
    return partial(
        httpx_mock.add_response,
        method="POST",
        url="https://diadoc-api.kontur.ru/v3/Authenticate?type=password",
        text="diadoc_auth_token",
    )


def test_base_url(http):
    assert http.diadoc_base_url == "https://diadoc-api.kontur.ru/"


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("/test/get", "https://diadoc-api.kontur.ru/test/get"),
        ("test/get", "https://diadoc-api.kontur.ru/test/get"),
        ("test/get/", "https://diadoc-api.kontur.ru/test/get"),
        ("/test/get/", "https://diadoc-api.kontur.ru/test/get"),
        ("test/get/?par=val", "https://diadoc-api.kontur.ru/test/get/?par=val"),
    ],
)
def test_format_url(url, expected, http):
    assert http.format_url(url) == expected


def test_get_base_headers(http):
    base_headers = http.get_base_headers()

    assert base_headers == {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "DiadocAuth ddauth_api_client_id=API-client-id",
    }


def test_token_return_received_token(mock_diadoc_auth_api, http):
    mock_diadoc_auth_api()

    token = http.token

    assert token == "diadoc_auth_token"


def test_getting_token_sent_right_request(http, mock_diadoc_auth_api, httpx_mock):
    mock_diadoc_auth_api()

    http.token

    request = httpx_mock.get_request()
    assert request.headers["Authorization"] == "DiadocAuth ddauth_api_client_id=API-client-id"
    assert request.headers["Content-Type"] == "application/json"
    assert request.headers["Accept"] == "application/json"
    assert request.content == b'{"login": "diadoc-superman@company.com", "password": "diadoc-super-password"}'


def test_token_is_cached(http, mock_diadoc_auth_api, httpx_mock):
    mock_diadoc_auth_api()
    http.token

    http.token

    assert len(httpx_mock.get_requests()) == 1


def test_headers(http_authorized):
    headers = http_authorized.headers

    assert headers == {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "DiadocAuth ddauth_api_client_id=API-client-id,ddauth_token=TOKEN",
    }


@pytest.mark.parametrize(
    ("method", "http_api_call"),
    [
        ("POST", lambda http, params: http.post("url", params=params)),
        ("GET", lambda http, params: http.get("url", params=params)),
    ],
)
def test_http_methods_return_received_json(http_authorized, mock_diadoc_url, method, http_api_call):
    mock_diadoc_url(url="https://diadoc-api.kontur.ru/url?param=value", method=method)

    got = http_api_call(http_authorized, params={"param": "value"})

    assert got["ok"] is True


@pytest.mark.parametrize(
    ("method", "http_api_call"),
    [
        ("POST", lambda http, payload: http.post("url", payload=payload)),
        ("GET", lambda http, payload: http.get("url", payload=payload)),
    ],
)
def test_http_methods_send_right_requests(http_authorized, mock_diadoc_url, method, http_api_call, httpx_mock):
    mock_diadoc_url(method=method)

    http_api_call(http_authorized, payload={"field_name": "some_value"})

    sent_request = httpx_mock.get_requests()[0]
    assert sent_request.headers["Content-Type"] == "application/json"
    assert sent_request.headers["Accept"] == "application/json"
    assert sent_request.headers["Authorization"] == "DiadocAuth ddauth_api_client_id=API-client-id,ddauth_token=TOKEN"
    assert sent_request.content == b'{"field_name": "some_value"}'


@pytest.mark.parametrize(
    ("method", "http_api_call"),
    [
        ("POST", lambda http: http.post("url")),
        ("GET", lambda http: http.get("url")),
    ],
)
def test_raise_on_unexpected_status_code(http_authorized, method, http_api_call, mock_diadoc_url):
    mock_diadoc_url(method=method, status_code=400)

    with pytest.raises(DiadocHTTPException, match="HTTP Error 400"):
        http_api_call(http_authorized)


@pytest.mark.parametrize(
    ("method", "http_api_call"),
    [
        ("POST", lambda http: http.post("url")),
        ("GET", lambda http: http.get("url")),
    ],
)
def test_raise_on_not_json_response(http_authorized, method, http_api_call, mock_diadoc_url):
    mock_diadoc_url(method=method, text="not a json")

    with pytest.raises(DiadocHTTPException, match="JSON decode error"):
        http_api_call(http_authorized)
