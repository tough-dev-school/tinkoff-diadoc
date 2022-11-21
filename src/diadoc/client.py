from typing import Any

from diadoc.http import DiadocHTTP


class DiadocClient:
    def __init__(self) -> None:
        self.http = DiadocHTTP()

    def get_my_organization_ids(self) -> list[str]:
        organizations = self.http.get("GetMyOrganizations")["Organizations"]  # type: ignore
        return [organization["OrgId"] for organization in organizations]  # type: ignore

    def get_counteragents(self, my_organization_id: str, counteragent_status: str | None = None) -> list[dict[str, Any]]:
        params = {"myOrgId": my_organization_id}

        if counteragent_status is not None:
            params["counteragentStatus"] = counteragent_status

        return self.http.get("/V2/GetCounteragents", params=params)["Counteragents"]  # type: ignore
