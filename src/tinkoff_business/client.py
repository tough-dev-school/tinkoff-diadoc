from dataclasses import dataclass
from datetime import date
from datetime import timedelta
from typing import Any

from tinkoff_business.http import TinkoffBusinessHTTP


@dataclass
class TinkoffBusinessClient:
    http: TinkoffBusinessHTTP = TinkoffBusinessHTTP()

    def get_bank_account_numbers(self) -> list[str]:
        return [bank_account["accountNumber"] for bank_account in self.http.get("bank-accounts")]  # type: ignore

    def get_operations(self, account_number: str, from_date: date | None = None, till_date: date | None = None) -> list[dict[str, Any]]:
        """Get operations from bank statement.

        If `till_date` is not provided today will be used.
        If `from_date` is not provided `till_date` - 1day will be used.
        """
        till_date = till_date or date.today()
        from_date = from_date or (till_date - timedelta(days=1))

        return self.http.get(  # type: ignore
            "bank-statement",
            params={
                "accountNumber": account_number,
                "from": from_date.strftime("%Y-%m-%d"),
                "till": till_date.strftime("%Y-%m-%d"),
            },
        )["operation"]
