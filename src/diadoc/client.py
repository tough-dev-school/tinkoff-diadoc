from app.models import LegalEntity
from diadoc.http import DiadocHTTP
from diadoc.types import DiadocOrganization


class DiadocClient:
    def __init__(self) -> None:
        self.http = DiadocHTTP()

    def get_my_organizations(self) -> list[LegalEntity]:
        organizations: list[DiadocOrganization] = self.http.get("GetMyOrganizations")["Organizations"]  # type: ignore

        return [
            LegalEntity(
                name=organization["ShortName"],
                inn=organization["Inn"],
                kpp=organization["Kpp"] or None,
                diadoc_id=organization["OrgId"],
            )
            for organization in organizations
        ]
