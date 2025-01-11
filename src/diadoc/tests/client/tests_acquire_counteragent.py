from contextlib import nullcontext as does_not_raise
from functools import partial
import pytest
import re

from diadoc.client import DiadocClient
from diadoc.models import DiadocPartner


@pytest.fixture
def partner():
    return DiadocPartner(
        name="Кракозябра LTD",
        inn="770099123001",
        kpp=None,
        diadoc_id="47bc8517-391d-43b4-9818-ab05d0cdb547",
        diadoc_box_id="2c9d3a6d-d8b2-46fc-8bce-af99fc68c57",
        is_active=True,
        is_roaming=True,
    )


@pytest.fixture
def mock_diadoc_response(httpx_mock):
    return httpx_mock.add_response(
        method="POST",
        url=re.compile("https://diadoc-api.kontur.ru/V3/AcquireCounteragent.*"),
        json={
            "TaskId": "5ef95ef4-8ab9-4c1c-b333-6f78c6a43fd2",
        },
    )


@pytest.fixture
def mock_sentry_capture_message(mocker):
    return mocker.patch("sentry_sdk.capture_message")


@pytest.fixture
def mock_sentry_capture_exc(mocker):
    return mocker.patch("sentry_sdk.capture_exception")


@pytest.fixture
def acquire_counteragent(client: DiadocClient, my_organization, partner):
    return partial(
        client.acquire_counteragent,
        my_organization=my_organization,
        to_acquire=partner,
    )


def test_my_org_box_id_in_query_params(acquire_counteragent, httpx_mock, mock_diadoc_response):
    acquire_counteragent()

    request_query = httpx_mock.get_request().url.query
    assert b"myBoxId=1ecf0eca-bfe3-4153-96a3-4ee0e72b69ed" in request_query


def test_payload_in_request_correct(acquire_counteragent, httpx_mock, mock_diadoc_response):
    acquire_counteragent(message="Hello everyone!")

    request_content = httpx_mock.get_request().content
    assert request_content == b'{"BoxId":"2c9d3a6d-d8b2-46fc-8bce-af99fc68c57","MessageToCounteragent":"Hello everyone!"}'


@pytest.mark.parametrize(
    "message",
    [None, ""],
)
def test_do_not_include_message_in_payload_if_empty(acquire_counteragent, httpx_mock, message, mock_diadoc_response):
    acquire_counteragent(message=message)

    request_content = httpx_mock.get_request().content
    assert b"MessageToCounteragent" not in request_content


def test_do_not_raise_and_send_sentry_info_message_on_409_errors(acquire_counteragent, httpx_mock, mock_sentry_capture_message, mock_sentry_capture_exc):
    httpx_mock.add_response(status_code=409, text="Setting is required for document exchange. Apply for roaming on www.diadoc.ru/roaming")

    with does_not_raise():
        acquire_counteragent()

    mock_sentry_capture_message.assert_called_once()
    mock_sentry_capture_exc.assert_not_called()


def test_do_not_raise_and_capture_sentry_exc_on_http_errors(acquire_counteragent, httpx_mock, mock_sentry_capture_message, mock_sentry_capture_exc):
    httpx_mock.add_response(status_code=504, text="Just diadoc timeout message")

    with does_not_raise():
        acquire_counteragent()

    mock_sentry_capture_exc.assert_called_once()
    mock_sentry_capture_message.assert_not_called()
