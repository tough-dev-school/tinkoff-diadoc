from functools import partial
import json
import pytest

from diadoc.services import DiadocOrganizationGetter


@pytest.fixture
def get_my_organizations_json():
    with open("./diadoc/tests/.fixtures/GetMyOrganizations.json", "r") as fp:
        response = json.load(fp)

        response["Organizations"][0]["OrgId"] = "9ae75028-3643-487b-acb6-9be364a96c90"
        response["Organizations"][1]["OrgId"] = "556387af-0a38-4c76-aaaa-5ca58ef55bdb"

        return response


@pytest.fixture
def mock_diadoc_api_response(httpx_mock, get_my_organizations_json):
    return partial(
        httpx_mock.add_response,
        url="https://diadoc-api.kontur.ru/GetMyOrganizations",
        json=get_my_organizations_json,
    )


@pytest.fixture
def spy_diadoc_organization_getter(mocker):
    return mocker.spy(DiadocOrganizationGetter, "__call__")


def test_get_my_organizations_call_service(client, mock_diadoc_api_response, spy_diadoc_organization_getter):
    mock_diadoc_api_response()

    legal_entities = client.get_my_organizations()

    assert len(legal_entities) == 2
    spy_diadoc_organization_getter.assert_called_once()


def test_get_returned_legal_entities(client, mock_diadoc_api_response):
    mock_diadoc_api_response()

    legal_entities = client.get_my_organizations()

    assert len(legal_entities) == 2
    assert legal_entities[0].diadoc_id == "9ae75028-3643-487b-acb6-9be364a96c90"
    assert legal_entities[1].diadoc_id == "556387af-0a38-4c76-aaaa-5ca58ef55bdb"
