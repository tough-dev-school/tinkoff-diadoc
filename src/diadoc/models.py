from dataclasses import dataclass
from dataclasses import field
from enum import Enum
from typing import Self

from app.models import LegalEntity
from diadoc import proto_types


class PartnershipStatus(Enum):
    ESTABLISHED = "established"
    INVITE_SHOULD_BE_SEND = "invite_should_be_send"
    INVITE_WAS_SENT = "invite_was_sent"
    REJECTED = "rejected"


COUNTERAGENT_PARTNERSHIP_STATUS_MAP = {
    "UnknownCounteragentStatus": PartnershipStatus.INVITE_SHOULD_BE_SEND,
    "IsMyCounteragent": PartnershipStatus.ESTABLISHED,
    "InvitesMe": PartnershipStatus.INVITE_SHOULD_BE_SEND,
    "IsInvitedByMe": PartnershipStatus.INVITE_WAS_SENT,
    "RejectsMe": PartnershipStatus.REJECTED,
    "IsRejectedByMe": PartnershipStatus.REJECTED,
    "NotInCounteragentList": PartnershipStatus.INVITE_SHOULD_BE_SEND,
}


@dataclass(frozen=True)
class DiadocPartner(LegalEntity):
    diadoc_id: str = field(repr=False)
    diadoc_box_id: str
    is_active: bool = field(repr=False)
    is_roaming: bool = field(repr=False)
    diadoc_partnership_status: PartnershipStatus | None = field(default=None, repr=False)

    @property
    def in_partners(self):
        return self.diadoc_partnership_status == PartnershipStatus.ESTABLISHED

    @property
    def invite_not_needed(self):
        return self.diadoc_partnership_status in [PartnershipStatus.INVITE_WAS_SENT, PartnershipStatus.REJECTED]

    @classmethod
    def from_organization(cls, organization: proto_types.Organization, partnership_status: PartnershipStatus | None = None) -> Self:
        return cls(
            name=organization["ShortName"],
            inn=organization["Inn"],
            kpp=organization["Kpp"] or None,
            diadoc_id=organization["OrgId"],
            diadoc_box_id=organization["Boxes"][0]["BoxIdGuid"],
            is_active=organization["IsActive"],
            is_roaming=organization["IsRoaming"],
            diadoc_partnership_status=partnership_status,
        )

    @classmethod
    def from_organization_list(cls, organizations: list[proto_types.Organization]) -> list[Self]:
        return [cls.from_organization(organization) for organization in organizations]

    @classmethod
    def from_counteragent(cls, counteragent: proto_types.Counteragent) -> Self:
        partnership_status = COUNTERAGENT_PARTNERSHIP_STATUS_MAP[counteragent["CurrentStatus"]]
        return cls.from_organization(counteragent["Organization"], partnership_status=partnership_status)

    @classmethod
    def from_counteragent_list(cls, counteragents: list[proto_types.Counteragent]) -> list[Self]:
        return [cls.from_counteragent(counteragent) for counteragent in counteragents]
