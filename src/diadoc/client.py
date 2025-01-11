import sentry_sdk

from diadoc import proto_types
from diadoc.exceptions import DiadocHTTPException
from diadoc.http import DiadocHTTP
from diadoc.models import DiadocPartner


class DiadocClient:
    def __init__(self) -> None:
        self.http = DiadocHTTP()

    def get_my_organizations(self) -> list[DiadocPartner]:
        organizations: list[proto_types.Organization] = self.http.get("GetMyOrganizations")["Organizations"]  # type: ignore
        return DiadocPartner.from_organization_list(organizations)

    def get_counteragents(self, my_organization: DiadocPartner) -> list[DiadocPartner]:
        """Return organization counteragents from possibly paginated API.

        To get next page:
            Step 1: Get `IndexKey` from last counteragent in response
            Step 2: Send request with query param `afterIndexKey` equals `IndexKey` from Step 1
        """
        params = {"myBoxId": my_organization.diadoc_box_id}

        counteragents: list[proto_types.Counteragent] = []
        paginated_counteragents_empty = False

        while not paginated_counteragents_empty:
            paginated_counteragents: list[proto_types.Counteragent] = self.http.get(url="V3/GetCounteragents", params=params)["Counteragents"]  # type: ignore

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

        organizations: list[proto_types.Organization] = self.http.get("GetOrganizationsByInnKpp", params=params)["Organizations"]  # type: ignore
        return DiadocPartner.from_organization_list(organizations)

    def acquire_counteragent(self, my_organization: DiadocPartner, to_acquire: DiadocPartner, message: str | None = None) -> None:
        params = {"myBoxId": my_organization.diadoc_box_id}
        payload = {"BoxId": to_acquire.diadoc_box_id}

        if message:
            payload["MessageToCounteragent"] = message

        try:
            self.http.post("V3/AcquireCounteragent", params=params, payload=payload)
        except DiadocHTTPException as exc:  # do not fail on HTTP errors, just send them to sentry
            if exc.code == 409:
                sentry_sdk.capture_message(
                    message=(
                        "Can't acquire the counteragent. The reason is most likely that there is no roaming with the agent's provider. "
                        f"counteragent={to_acquire}, "
                        f"message={exc.message}",
                    )
                )
            else:
                sentry_sdk.capture_exception(exc)
