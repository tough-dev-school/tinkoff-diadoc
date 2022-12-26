from diadoc.http import DiadocHTTP
from diadoc.models import DiadocPartner
from diadoc.types import DiadocCounteragent
from diadoc.types import DiadocId
from diadoc.types import DiadocOrganization
from diadoc.types import DiadocTaskId


class DiadocClient:
    def __init__(self) -> None:
        self.http = DiadocHTTP()

    def get_my_organizations(self) -> list[DiadocPartner]:
        organizations: list[DiadocOrganization] = self.http.get("GetMyOrganizations")["Organizations"]  # type: ignore
        return DiadocPartner.from_organization_list(organizations)

    def get_counteragents(self, my_diadoc_id: DiadocId) -> list[DiadocPartner]:
        """Return organization counteragents from possibly paginated API.

        To get next page:
            Step 1: Get `IndexKey` from last counteragent in response
            Step 2: Send request with query param `afterIndexKey` equals `IndexKey` from Step 1
        """
        params = {"myOrgId": my_diadoc_id}

        counteragents: list[DiadocCounteragent] = []
        paginated_counteragents_empty = False

        while not paginated_counteragents_empty:
            paginated_counteragents: list[DiadocCounteragent] = self.http.get(url="V2/GetCounteragents", params=params)["Counteragents"]  # type: ignore

            if paginated_counteragents:
                counteragents += paginated_counteragents
                params["afterIndexKey"] = paginated_counteragents[-1]["IndexKey"]
            else:
                paginated_counteragents_empty = True

        return DiadocPartner.from_counteragent_list(counteragents)

    def get_organizations_by_inn_kpp(self, inn: str, kpp: str | None = None) -> list[DiadocPartner]:
        params = {"inn": inn}
        if kpp:
            params["kpp"] = kpp

        organizations: list[DiadocOrganization] = self.http.get("GetOrganizationsByInnKpp", params=params)["Organizations"]  # type: ignore
        return DiadocPartner.from_organization_list(organizations)

    def acquire_counteragent(self, my_diadoc_id: DiadocId, diadoc_id: DiadocId, message: str | None = None) -> DiadocTaskId:
        params = {"myOrgId": my_diadoc_id}
        payload = {"OrgId": diadoc_id}

        if message:
            payload["MessageToCounteragent"] = message

        return self.http.post("V2/AcquireCounteragent", params=params, payload=payload)["TaskId"]  # type: ignore
