import pytest

from tinkoff_to_diadoc.exceptions import TinkoffToDiadocException


@pytest.fixture
def mock_get_company(mocker):
    def _get_company(entity):
        return mocker.patch("tinkoff_business.client.TinkoffBusinessClient.get_company", return_value=entity)

    return _get_company


@pytest.fixture
def mock_get_my_organizations(mocker):
    def _get_my_organizations(diadoc_entities):
        return mocker.patch("diadoc.client.DiadocClient.get_my_organizations", return_value=diadoc_entities)

    return _get_my_organizations


@pytest.fixture
def get_my_company(tinkoff_to_diadoc):
    return lambda: tinkoff_to_diadoc.get_my_company()


def test_return_diadoc_entity_matched_tinkoff_company(get_my_company, mock_get_my_organizations, mock_get_company, entity, diadoc_entity, ya_diadoc_entity):
    mock_get_company(entity)
    mock_get_my_organizations([ya_diadoc_entity, diadoc_entity])

    my_company = get_my_company()

    assert my_company.inn_kpp == entity.inn_kpp
    assert my_company == diadoc_entity  # `diadoc_entity` has same inn and kpp as `entity`


def test_raise_if_tinkoff_entity_not_found_in_diadoc(get_my_company, mock_get_my_organizations, mock_get_company, entity, ya_diadoc_entity):
    mock_get_company(entity)
    mock_get_my_organizations([ya_diadoc_entity])

    with pytest.raises(TinkoffToDiadocException, match="Did not find"):
        get_my_company()


def test_call_tinkoff_and_diadoc_clients(get_my_company, mock_get_my_organizations, diadoc_entity, mock_get_company, entity):
    mock_tinkoff = mock_get_company(entity)
    mock_diadoc = mock_get_my_organizations([diadoc_entity])

    get_my_company()

    mock_tinkoff.assert_called_once()
    mock_diadoc.assert_called_once()
