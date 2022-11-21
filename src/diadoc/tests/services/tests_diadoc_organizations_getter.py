import json
import pytest

from diadoc.services import DiadocOrganizationGetter


@pytest.fixture
def get_my_organizations_json():
    with open("./diadoc/tests/.fixtures/GetMyOrganizations.json", "r") as fp:
        organizations = json.load(fp)

        organizations["Organizations"][0]["OrgId"] = "9ae75028-3643-487b-acb6-9be364a96c90"
        organizations["Organizations"][0]["FullName"] = "Пирогов Валя Сергеич"
        organizations["Organizations"][0]["Inn"] = "70707070707"
        organizations["Organizations"][0]["Kpp"] = ""  # diadoc return empty string for entities without KPP

        organizations["Organizations"][1]["OrgId"] = "556387af-0a38-4c76-aaaa-5ca58ef55bdb"
        organizations["Organizations"][1]["FullName"] = "ООО Петрушка и Макушка"
        organizations["Organizations"][1]["Inn"] = "778080808080"
        organizations["Organizations"][1]["Kpp"] = "779999999999"

        return organizations


def test_get_legal_entities_from_my_organizations_response(get_my_organizations_json):
    got = DiadocOrganizationGetter(get_my_organizations_json)()

    assert len(got) == 2
    first_legal_entity = got[0]
    second_legal_entity = got[1]
    assert first_legal_entity.name == "Пирогов Валя Сергеич"
    assert first_legal_entity.inn == "70707070707"
    assert first_legal_entity.kpp is None  # empty KPP is saved as None
    assert first_legal_entity.diadoc_id == "9ae75028-3643-487b-acb6-9be364a96c90"
    assert second_legal_entity.name == "ООО Петрушка и Макушка"
    assert second_legal_entity.inn == "778080808080"
    assert second_legal_entity.kpp == "779999999999"
    assert second_legal_entity.diadoc_id == "556387af-0a38-4c76-aaaa-5ca58ef55bdb"
