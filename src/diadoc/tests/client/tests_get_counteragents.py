import json
import pytest


@pytest.fixture
def get_counteragents_json():
    with open("./diadoc/tests/.fixtures/GetCounteragents.json", "r") as fp:
        return json.load(fp)


@pytest.fixture
def mock_diadoc_get_counteragents(httpx_mock, get_counteragents_json):
    return httpx_mock.add_response(
        url="https://diadoc-api.kontur.ru/V2/GetCounteragents?myOrgId=100500",
        json=get_counteragents_json,
    )


def test_get_counteragents(client, mock_diadoc_get_counteragents, get_counteragents_json):
    organization_id = "100500"

    got = client.get_counteragents(my_organization_id=organization_id)

    assert len(got) == 2
    assert got == get_counteragents_json["Counteragents"]
