from functools import partial
import pytest
from uuid import uuid4

from diadoc.models import DiadocPartner
from diadoc.models import PartnershipStatus


@pytest.fixture
def not_active_partner():
    return DiadocPartner(
        name="ООО Петрушка",
        inn="7788445533",
        kpp="200500",
        diadoc_id=str(uuid4()),
        diadoc_partnership_status=PartnershipStatus.INVITE_SHOULD_BE_SEND,
        is_active=False,
        is_roaming=False,
    )


@pytest.fixture
def exclude_to_invite(tinkoff_to_diadoc, partner):
    return partial(
        tinkoff_to_diadoc.exclude_partners_not_needed_to_invite,
        partners=[partner],
        counteragents=[],
    )


def test_return_all_provided_partners_if_nothing_to_exclude(exclude_to_invite, partner, ya_partner):
    got = exclude_to_invite(partners=[partner, ya_partner])

    assert got == [partner, ya_partner]


@pytest.mark.parametrize(
    "partnership_status",
    [
        PartnershipStatus.REJECTED,
        PartnershipStatus.INVITE_WAS_SENT,
    ],
)
def test_exclude_partners_in_counteragents_not_invite_required(exclude_to_invite, create_counteragent, partner, partnership_status):
    counteragent = create_counteragent(partner, partnership_status)

    got = exclude_to_invite(counteragents=[counteragent])

    assert got == []


def test_include_partners_in_counteragents_invite_should_sent(exclude_to_invite, create_counteragent, partner):
    counteragent = create_counteragent(partner, PartnershipStatus.INVITE_SHOULD_BE_SEND)

    got = exclude_to_invite(counteragents=[counteragent])

    assert got == [partner]


def test_do_not_exclude_partners_not_in_counteragents(exclude_to_invite, create_counteragent, partner, ya_partner):
    counteragent = create_counteragent(ya_partner, PartnershipStatus.REJECTED)

    got = exclude_to_invite(counteragents=[counteragent])

    assert got == [partner]


def test_exclude_not_active_diadoc_partners(exclude_to_invite, not_active_partner, partner, ya_partner):
    got = exclude_to_invite(partners=[not_active_partner, partner, ya_partner])

    assert got == [partner, ya_partner]
