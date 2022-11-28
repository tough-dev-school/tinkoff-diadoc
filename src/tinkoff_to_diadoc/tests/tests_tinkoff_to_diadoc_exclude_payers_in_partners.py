from functools import partial
import pytest
from uuid import uuid4

from diadoc.models import DiadocLegalEntity
from diadoc.models import PartnershipStatus


@pytest.fixture
def create_counteragent(entity):
    return lambda partnership_status: DiadocLegalEntity(
        name=entity.name,
        inn=entity.inn,
        kpp=entity.kpp,
        diadoc_id=str(uuid4()),
        diadoc_partnership_status=partnership_status,
        is_active=True,
    )


@pytest.fixture
def exclude_payers(tinkoff_to_diadoc, entity):
    return partial(
        tinkoff_to_diadoc.exclude_payers_in_partners,
        payers=[entity],
    )


@pytest.mark.parametrize(
    "partnership_status",
    [
        PartnershipStatus.INVITE_WAS_SENT,
        PartnershipStatus.INVITE_SHOULD_BE_SEND,
        PartnershipStatus.REJECTED,
    ],
)
def test_include_payer_not_in_established_counteragents(exclude_payers, entity, create_counteragent, partnership_status):
    counteragent = create_counteragent(partnership_status)

    payers = exclude_payers(counteragents=[counteragent])

    assert payers == [entity]


def test_exclude_payer_in_established_counteragents(exclude_payers, create_counteragent):
    counteragent = create_counteragent(PartnershipStatus.ESTABLISHED)

    payers = exclude_payers(counteragents=[counteragent])

    assert payers == []


def test_exclude_payer_if_several_counteragents_found_one_of_them_established(exclude_payers, create_counteragent):
    counteragent = create_counteragent(PartnershipStatus.ESTABLISHED)
    same_entity_counteragent = create_counteragent(PartnershipStatus.INVITE_SHOULD_BE_SEND)

    payers = exclude_payers(counteragents=[counteragent, same_entity_counteragent])

    assert payers == []
