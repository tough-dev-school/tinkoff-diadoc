from functools import partial
import pytest

from diadoc.models import DiadocLegalEntity
from diadoc.models import PartnershipStatus


@pytest.fixture
def create_counteragent():
    def _create(diadoc_entity, partnership_status):
        return DiadocLegalEntity(
            name=diadoc_entity.name,
            inn=diadoc_entity.inn,
            kpp=diadoc_entity.inn,
            diadoc_id=diadoc_entity.diadoc_id,
            diadoc_partnership_status=partnership_status,
            is_active=True,
        )

    return _create


@pytest.fixture
def filter_to_invite(tinkoff_to_diadoc, diadoc_entity):
    return partial(
        tinkoff_to_diadoc.filter_diadoc_entities_to_invite,
        diadoc_entities=[diadoc_entity],
        counteragents=[],
    )


def test_return_all_provided_entities(filter_to_invite, diadoc_entity, ya_diadoc_entity):
    got = filter_to_invite(diadoc_entities=[diadoc_entity, ya_diadoc_entity])

    assert got == [diadoc_entity, ya_diadoc_entity]


@pytest.mark.parametrize(
    "partnership_status",
    [
        PartnershipStatus.REJECTED,
        PartnershipStatus.INVITE_WAS_SENT,
    ],
)
def test_exclude_entities_in_counteragents_not_invite_required(filter_to_invite, create_counteragent, diadoc_entity, partnership_status):
    counteragent = create_counteragent(diadoc_entity, partnership_status)

    got = filter_to_invite(counteragents=[counteragent])

    assert got == []


def test_include_entities_in_counteragents_invite_should_sent(filter_to_invite, create_counteragent, diadoc_entity):
    counteragent = create_counteragent(diadoc_entity, PartnershipStatus.INVITE_SHOULD_BE_SEND)

    got = filter_to_invite(counteragents=[counteragent])

    assert got == [diadoc_entity]


def test_do_not_exclude_entities_not_in_counteragents(filter_to_invite, create_counteragent, diadoc_entity, ya_diadoc_entity):
    counteragent = create_counteragent(ya_diadoc_entity, PartnershipStatus.REJECTED)

    got = filter_to_invite(counteragents=[counteragent])

    assert got == [diadoc_entity]


def test_exclude_not_active_diadoc_entities(filter_to_invite, diadoc_entity, ya_diadoc_entity):
    diadoc_entity.is_active = False

    got = filter_to_invite(diadoc_entities=[diadoc_entity, ya_diadoc_entity])

    assert got == [ya_diadoc_entity]
