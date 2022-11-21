from dataclasses import dataclass

from app.models import LegalEntity
from app.services import BaseService
from app.types import SimpleJSONType


@dataclass
class DiadocOrganizationGetter(BaseService):
    """Convert response with structures of 'Diadoc Organization' to list of LegalEntity."""

    diadoc_organizations_response: SimpleJSONType

    def act(self) -> list[LegalEntity]:
        return [
            LegalEntity(
                name=organization["FullName"],
                inn=organization["Inn"],
                kpp=organization["Kpp"] or None,
                diadoc_id=organization["OrgId"],
            )
            for organization in self.diadoc_organizations_response["Organizations"]  # type: ignore
        ]
