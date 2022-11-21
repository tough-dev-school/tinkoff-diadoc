from dataclasses import dataclass

from app.models import BankAccount
from app.services import BaseService
from app.types import SimpleJSONType


@dataclass
class TinkoffBankAccountGetter(BaseService):
    bank_accounts_response: SimpleJSONType

    def act(self) -> list[BankAccount]:
        return [BankAccount(account_number=bank_account["accountNumber"]) for bank_account in self.bank_accounts_response]  # type: ignore
