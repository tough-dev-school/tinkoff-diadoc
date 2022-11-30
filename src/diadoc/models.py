from dataclasses import dataclass
from dataclasses import field
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


@dataclass(unsafe_hash=True)
class DiadocLegalEntity(LegalEntity):
    diadoc_id: str
    is_active: bool = field(hash=False, compare=False)
    diadoc_partnership_status: PartnershipStatus | None = field(default=None, hash=False, compare=False)

    @property
    def in_partners(self):
        return self.diadoc_partnership_status == PartnershipStatus.ESTABLISHED

    @property
    def invite_not_needed(self):
        return self.diadoc_partnership_status in [PartnershipStatus.INVITE_WAS_SENT, PartnershipStatus.REJECTED]

    @staticmethod
    def from_organization(organization=DiadocOrganization) -> "DiadocLegalEntity":
        return DiadocLegalEntity(
            name=organization["ShortName"],
            inn=organization["Inn"],
            kpp=organization["Kpp"] or None,
            diadoc_id=organization["OrgId"],
            is_active=organization["IsActive"],
        )

    @classmethod
    def from_organization_list(cls, organizations: list[DiadocOrganization]) -> list["DiadocLegalEntity"]:
        return [cls.from_organization(organization) for organization in organizations]

    @classmethod
    def from_counteragent(cls, counteragent=DiadocCounteragent) -> "DiadocLegalEntity":
        legal_entity = cls.from_organization(counteragent["Organization"])
        legal_entity.diadoc_partnership_status = COUNTERAGENT_PARTNERSHIP_STATUS_MAP[counteragent["CurrentStatus"]]
        return legal_entity

    @classmethod
    def from_counteragents_list(cls, counteragents: list[DiadocCounteragent]) -> list["DiadocLegalEntity"]:
        return [cls.from_counteragent(counteragent) for counteragent in counteragents]
