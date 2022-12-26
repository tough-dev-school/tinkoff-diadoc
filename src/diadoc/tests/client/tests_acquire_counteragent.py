from functools import partial
import pytest
import re


@pytest.fixture(autouse=True)
def mock_diadoc_response(httpx_mock):
    return httpx_mock.add_response(
        method="POST",
        url=re.compile("https://diadoc-api.kontur.ru/V2/AcquireCounteragent.*"),
        json={
            "TaskId": "5ef95ef4-8ab9-4c1c-b333-6f78c6a43fd2",
        },
    )


@pytest.fixture
def acquire_counteragent(client, my_organization):
    return partial(
        client.acquire_counteragent,
        my_diadoc_id=my_organization.diadoc_id,
        diadoc_id="2c9d3a6d-d8b2-46fc-8bce-af99fc68c575",
    )


def test_acquire_counteragent_return_diadoc_task_id(acquire_counteragent):
    got = acquire_counteragent()

    assert got == "5ef95ef4-8ab9-4c1c-b333-6f78c6a43fd2"


def test_my_org_id_in_query_params(acquire_counteragent, httpx_mock):
    acquire_counteragent()

    request_query = httpx_mock.get_request().url.query
    assert b"myOrgId=75fcac12-ec63-4cdd-9076-87a8a2e6e8ba" in request_query


def test_payload_in_request_correct(acquire_counteragent, httpx_mock):
    acquire_counteragent(message="Hello everyone!")

    request_content = httpx_mock.get_request().content
    assert request_content == b'{"OrgId": "2c9d3a6d-d8b2-46fc-8bce-af99fc68c575", "MessageToCounteragent": "Hello everyone!"}'


@pytest.mark.parametrize(
    "message",
    [None, "", "Yo!"],
)
def test_do_not_include_message_in_payload_if_empty(acquire_counteragent, httpx_mock, message):
    acquire_counteragent(message=message)

    request_content = httpx_mock.get_request().content
    assert b"message" not in request_content
