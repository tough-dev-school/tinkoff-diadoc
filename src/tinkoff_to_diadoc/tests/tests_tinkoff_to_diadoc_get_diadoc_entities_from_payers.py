from functools import partial
import pytest

from app.models import LegalEntity


@pytest.fixture
def ya_entity():
    return LegalEntity(name="ООО Машинка", inn="7788990011", kpp="1233454")


@pytest.fixture
def get_entities_from_payers(tinkoff_to_diadoc, entity):
    return partial(tinkoff_to_diadoc.get_diadoc_entities_from_payers, payers=[entity])


@pytest.fixture
def mock_diadoc_get_by_inn_kpp(mocker):
    def _get_by_inn_kpp(diadoc_entities):
        return mocker.patch("diadoc.client.DiadocClient.get_organizations_by_inn_kpp", return_value=diadoc_entities)

    return _get_by_inn_kpp


def test_return_diadoc_entities(get_entities_from_payers, mock_diadoc_get_by_inn_kpp, diadoc_entity, ya_diadoc_entity):
    mock_diadoc_get_by_inn_kpp([diadoc_entity, ya_diadoc_entity])

    got = get_entities_from_payers()

    assert got == [diadoc_entity, ya_diadoc_entity]


def test_call_diadoc_get_by_inn_kpp_for_every_payer(get_entities_from_payers, entity, ya_entity, mock_diadoc_get_by_inn_kpp, mocker):
    mock_get_by_inn_kpp = mock_diadoc_get_by_inn_kpp([])

    get_entities_from_payers(payers=[entity, ya_entity])

    mock_get_by_inn_kpp.assert_has_calls(
        calls=[
            mocker.call(inn=entity.inn, kpp=entity.kpp),
            mocker.call(inn=ya_entity.inn, kpp=ya_entity.kpp),
        ],
        any_order=True,
    )
