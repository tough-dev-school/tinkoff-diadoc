from dataclasses import dataclass

from app.models import LegalEntity
from diadoc.types import DiadocOrganization


@dataclass
class DiadocLegalEntity(LegalEntity):
    diadoc_id: str
    is_active: bool
    is_roaming: bool

    @staticmethod
    def from_organization(organization=DiadocOrganization) -> "DiadocLegalEntity":
        return DiadocLegalEntity(
            name=organization["ShortName"],
            inn=organization["Inn"],
            kpp=organization["Kpp"] or None,
            diadoc_id=organization["OrgId"],
            is_active=organization["IsActive"],
            is_roaming=organization["IsRoaming"],
        )

    @classmethod
    def from_organization_list(cls, organizations: list[DiadocOrganization]) -> list["DiadocLegalEntity"]:
        return [cls.from_organization(organization) for organization in organizations]
