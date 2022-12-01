from functools import partial
import pytest

from diadoc.models import PartnershipStatus


@pytest.fixture
def exclude_payers(tinkoff_to_diadoc, legal_entity):
    return partial(
        tinkoff_to_diadoc.exclude_payers_in_partners,
        payers=[legal_entity],
    )


@pytest.mark.parametrize(
    "partnership_status",
    [
        PartnershipStatus.INVITE_WAS_SENT,
        PartnershipStatus.INVITE_SHOULD_BE_SEND,
        PartnershipStatus.REJECTED,
    ],
)
def test_include_payer_not_in_established_counteragents(exclude_payers, legal_entity, partner, create_counteragent, partnership_status):
    counteragent = create_counteragent(partner, partnership_status)

    payers = exclude_payers(counteragents=[counteragent])

    assert payers == [legal_entity]


def test_exclude_payer_in_established_counteragents(exclude_payers, partner, create_counteragent):
    counteragent = create_counteragent(partner, PartnershipStatus.ESTABLISHED)

    payers = exclude_payers(counteragents=[counteragent])

    assert payers == []


def test_exclude_payer_if_several_counteragents_found_one_of_them_established(exclude_payers, partner, create_counteragent):
    counteragent = create_counteragent(partner, PartnershipStatus.ESTABLISHED)
    same_partner_counteragent = create_counteragent(partner, PartnershipStatus.INVITE_SHOULD_BE_SEND)

    payers = exclude_payers(counteragents=[counteragent, same_partner_counteragent])

    assert payers == []
