from dataclasses import dataclass
from datetime import date
from datetime import timedelta

from app.models import BankAccount
from app.models import LegalEntity
from tinkoff_business.http import TinkoffBusinessHTTP
from tinkoff_business.services import TinkoffBankAccountGetter
from tinkoff_business.services import TinkoffPayerGetter


@dataclass
class TinkoffBusinessClient:
    http: TinkoffBusinessHTTP = TinkoffBusinessHTTP()

    def get_bank_accounts(self) -> list[BankAccount]:
        return TinkoffBankAccountGetter(self.http.get("bank-accounts"))()

    def get_payers(self, account_number: str, from_date: date | None = None, till_date: date | None = None) -> list[LegalEntity]:
        """Get payers from 'bank-statement' API.

        If `till_date` is not provided today will be used.
        If `from_date` is not provided `till_date` - 1day will be used.
        """
        till_date = till_date or date.today()
        from_date = from_date or (till_date - timedelta(days=1))

        bank_statement_response = self.http.get(
            "bank-statement",
            params={
                "accountNumber": account_number,
                "from": from_date.strftime("%Y-%m-%d"),
                "till": till_date.strftime("%Y-%m-%d"),
            },
        )

        return TinkoffPayerGetter(bank_statement_response)()
