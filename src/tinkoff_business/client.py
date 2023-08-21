from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import TYPE_CHECKING

from app.models import LegalEntity
from tinkoff_business.http import TinkoffBusinessHTTP
from tinkoff_business.models import TinkoffBankAccount

if TYPE_CHECKING:
    from tinkoff_business.types import TinkoffMyCompany
    from tinkoff_business.types import TinkoffStatement


class TinkoffBusinessClient:
    def __init__(self) -> None:
        self.http = TinkoffBusinessHTTP()

    def get_company(self) -> LegalEntity:
        company: TinkoffMyCompany = self.http.get("/v1/company")  # type: ignore
        return LegalEntity(
            name=company["name"],
            inn=company["requisites"]["inn"],
            kpp=company["requisites"].get("kpp") or None,
        )

    def get_bank_accounts(self) -> list[TinkoffBankAccount]:
        return [TinkoffBankAccount(bank_account["accountNumber"]) for bank_account in self.http.get("/v4/bank-accounts")]  # type: ignore

    def get_payers_with_non_empty_inn(self, account_number: str, from_date: datetime | None = None) -> list[LegalEntity]:
        """Get payers with non empty inn from 'statement' API.

        If 'from_date' is not provided 'now()' - 1day will be used.
        * Payer may not have an inn if it is a non-russian counteragent.
        """
        from_date = from_date.astimezone(timezone.utc) if from_date else datetime.now(timezone.utc) - timedelta(days=1)

        params = {
            "accountNumber": account_number,
            "from": from_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }

        statement: TinkoffStatement = self.http.get("/v1/statement", params=params)  # type: ignore
        return [
            LegalEntity(
                name=operation["payer"]["name"],
                inn=operation["payer"]["inn"],
                kpp=operation["payer"].get("kpp"),
            )
            for operation in statement["operations"]
            if "payer" in operation and "inn" in operation["payer"]
        ]
