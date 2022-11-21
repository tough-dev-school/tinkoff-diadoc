from typing import Any

from app.models import LegalEntity
from diadoc.http import DiadocHTTP
from diadoc.services import DiadocOrganizationGetter


class DiadocClient:
    def __init__(self) -> None:
        self.http = DiadocHTTP()

    def get_my_organizations(self) -> list[LegalEntity]:
        return DiadocOrganizationGetter(self.http.get("GetMyOrganizations"))()  # type: ignore

    def get_counteragents(self, my_organization_id: str, counteragent_status: str | None = None) -> list[dict[str, Any]]:
        params = {"myOrgId": my_organization_id}

        if counteragent_status is not None:
            params["counteragentStatus"] = counteragent_status

        return self.http.get("/V2/GetCounteragents", params=params)["Counteragents"]  # type: ignore
