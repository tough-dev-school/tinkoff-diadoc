from datetime import date
from datetime import timedelta

from app.models import BankAccount
from app.models import LegalEntity
from tinkoff_business.http import TinkoffBusinessHTTP


class TinkoffBusinessClient:
    def __init__(self) -> None:
        self.http = TinkoffBusinessHTTP()

    def get_company(self) -> LegalEntity:
        company = self.http.get("company")
        return LegalEntity(
            name=company["name"],  # type: ignore
            inn=company["requisites"]["inn"],  # type: ignore
            kpp=company["requisites"].get("kpp") or None,  # type: ignore
        )

    def get_bank_accounts(self) -> list[BankAccount]:
        return [BankAccount(bank_account["accountNumber"]) for bank_account in self.http.get("bank-accounts")]  # type: ignore

    def get_payers(
        self,
        account_number: str,
        from_date: date | None = None,
        till_date: date | None = None,
        exclude_payer_inn: str | None = None,
    ) -> list[LegalEntity]:
        """Get payers from 'bank-statement' API.

        If 'exclude_payer_inn' provided the return excludes operations were 'exclude_payer_inn' is payer.

        If `till_date` is not provided today will be used.
        If `from_date` is not provided `till_date` - 1day will be used.
        """
        till_date = till_date or date.today()
        from_date = from_date or (till_date - timedelta(days=1))

        params = {
            "accountNumber": account_number,
            "from": from_date.strftime("%Y-%m-%d"),
            "till": till_date.strftime("%Y-%m-%d"),
        }

        return [
            LegalEntity(
                name=operation["payerName"],
                inn=operation["payerInn"],
                kpp=operation.get("payerKpp"),
            )
            for operation in self.http.get("bank-statement", params=params)["operation"]  # type: ignore
            if exclude_payer_inn is None or operation["payerInn"] != exclude_payer_inn
        ]
