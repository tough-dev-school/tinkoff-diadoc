import json
import pytest


@pytest.fixture
def get_my_organizations_json():
    with open("./diadoc/tests/.fixtures/GetMyOrganizations.json", "r") as fp:
        organizations = json.load(fp)

        organizations["Organizations"][0]["OrgId"] = "9ae75028-3643-487b-acb6-9be364a96c90"
        organizations["Organizations"][1]["OrgId"] = "556387af-0a38-4c76-aaaa-5ca58ef55bdb"

        return organizations


@pytest.fixture
def mock_diadoc_get_my_organizations(httpx_mock, get_my_organizations_json):
    return httpx_mock.add_response(
        url="https://diadoc-api.kontur.ru/GetMyOrganizations",
        json=get_my_organizations_json,
    )


def test_get_my_organization_ids(client, mock_diadoc_get_my_organizations):
    got = client.get_my_organization_ids()

    assert len(got) == 2
    assert got[0] == "9ae75028-3643-487b-acb6-9be364a96c90"
    assert got[1] == "556387af-0a38-4c76-aaaa-5ca58ef55bdb"
