from contextlib import nullcontext as does_not_raise
from functools import partial
import pytest
import re


@pytest.fixture
def mock_diadoc_response(httpx_mock):
    return httpx_mock.add_response(
        method="POST",
        url=re.compile("https://diadoc-api.kontur.ru/V2/AcquireCounteragent.*"),
        json={
            "TaskId": "5ef95ef4-8ab9-4c1c-b333-6f78c6a43fd2",
        },
    )


@pytest.fixture
def mock_sentry_capture(mocker):
    return mocker.patch("diadoc.client.capture_exception")


@pytest.fixture
def acquire_counteragent(client, my_organization):
    return partial(
        client.acquire_counteragent,
        my_diadoc_id=my_organization.diadoc_id,
        diadoc_id="2c9d3a6d-d8b2-46fc-8bce-af99fc68c575",
    )


def test_my_org_id_in_query_params(acquire_counteragent, httpx_mock, mock_diadoc_response):
    acquire_counteragent()

    request_query = httpx_mock.get_request().url.query
    assert b"myOrgId=75fcac12-ec63-4cdd-9076-87a8a2e6e8ba" in request_query


def test_payload_in_request_correct(acquire_counteragent, httpx_mock, mock_diadoc_response):
    acquire_counteragent(message="Hello everyone!")

    request_content = httpx_mock.get_request().content
    assert request_content == b'{"OrgId":"2c9d3a6d-d8b2-46fc-8bce-af99fc68c575","MessageToCounteragent":"Hello everyone!"}'


@pytest.mark.parametrize(
    "message",
    [None, ""],
)
def test_do_not_include_message_in_payload_if_empty(acquire_counteragent, httpx_mock, message, mock_diadoc_response):
    acquire_counteragent(message=message)

    request_content = httpx_mock.get_request().content
    assert b"MessageToCounteragent" not in request_content


def test_do_not_raise_on_errors_and_capture_exception_to_sentry(acquire_counteragent, httpx_mock, mock_sentry_capture):
    httpx_mock.add_response(status_code=409, text="Setting is required for document exchange. Apply for roaming on www.diadoc.ru/roaming")

    with does_not_raise():
        acquire_counteragent()

    mock_sentry_capture.assert_called_once()
