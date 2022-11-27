from diadoc.http import DiadocHTTP
from diadoc.models import DiadocLegalEntity
from diadoc.types import DiadocCounteragent
from diadoc.types import DiadocOrganization


class DiadocClient:
    def __init__(self) -> None:
        self.http = DiadocHTTP()

    def get_my_organizations(self) -> list[DiadocLegalEntity]:
        organizations: list[DiadocOrganization] = self.http.get("GetMyOrganizations")["Organizations"]  # type: ignore
        return DiadocLegalEntity.from_organization_list(organizations)

    def get_counteragents(self, my_organization_id: str) -> list[DiadocLegalEntity]:
        """Return organization counteragents from possibly paginated API.

        To get next page:
            Step 1: Get `IndexKey` from last counteragent in response
            Step 2: Send request with query param `afterIndexKey` equals `IndexKey` from Step 1
        """
        params = {"myOrgId": my_organization_id}

        counteragents: list[DiadocCounteragent] = []
        paginated_counteragents_empty = False

        while not paginated_counteragents_empty:
            paginated_counteragents: list[DiadocCounteragent] = self.http.get(url="V2/GetCounteragents", params=params)["Counteragents"]  # type: ignore

            if paginated_counteragents:
                counteragents += paginated_counteragents
                params["afterIndexKey"] = paginated_counteragents[-1]["IndexKey"]
            else:
                paginated_counteragents_empty = True

        return DiadocLegalEntity.from_counteragents_list(counteragents)
