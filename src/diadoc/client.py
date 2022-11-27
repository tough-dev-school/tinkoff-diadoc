from diadoc.http import DiadocHTTP
from diadoc.models import DiadocLegalEntity
from diadoc.types import DiadocOrganization


class DiadocClient:
    def __init__(self) -> None:
        self.http = DiadocHTTP()

    def get_my_organizations(self) -> list[DiadocLegalEntity]:
        organizations: list[DiadocOrganization] = self.http.get("GetMyOrganizations")["Organizations"]  # type: ignore
        return DiadocLegalEntity.from_organization_list(organizations)
