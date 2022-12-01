from dataclasses import dataclass
from enum import Enum

from app.models import LegalEntity
from diadoc.types import DiadocCounteragent
from diadoc.types import DiadocOrganization


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
    diadoc_id: str
    is_active: bool
    is_roaming: bool
    diadoc_partnership_status: PartnershipStatus | None = None

    @property
    def in_partners(self):
        return self.diadoc_partnership_status == PartnershipStatus.ESTABLISHED

    @property
    def invite_not_needed(self):
        return self.diadoc_partnership_status in [PartnershipStatus.INVITE_WAS_SENT, PartnershipStatus.REJECTED]

    @staticmethod
    def from_organization(organization: DiadocOrganization, partnership_status: PartnershipStatus | None = None) -> "DiadocPartner":
        return DiadocPartner(
            name=organization["ShortName"],
            inn=organization["Inn"],
            kpp=organization["Kpp"] or None,
            diadoc_id=organization["OrgId"],
            is_active=organization["IsActive"],
            is_roaming=organization["IsRoaming"],
            diadoc_partnership_status=partnership_status,
        )

    @classmethod
    def from_organization_list(cls, organizations: list[DiadocOrganization]) -> list["DiadocPartner"]:
        return [cls.from_organization(organization) for organization in organizations]

    @classmethod
    def from_counteragent(cls, counteragent: DiadocCounteragent) -> "DiadocPartner":
        partnership_status = COUNTERAGENT_PARTNERSHIP_STATUS_MAP[counteragent["CurrentStatus"]]
        return cls.from_organization(counteragent["Organization"], partnership_status=partnership_status)

    @classmethod
    def from_counteragent_list(cls, counteragents: list[DiadocCounteragent]) -> list["DiadocPartner"]:
        return [cls.from_counteragent(counteragent) for counteragent in counteragents]
