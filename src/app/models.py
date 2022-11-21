from dataclasses import dataclass

from app.types import SimpleJSONType


@dataclass
class BankAccount:
    account_number: str

    @classmethod
    def from_tinkoff_bank_accounts(cls, bank_accounts_response: SimpleJSONType) -> list["BankAccount"]:
        return [cls(account_number=bank_account["accountNumber"]) for bank_account in bank_accounts_response]  # type: ignore


@dataclass
class LegalEntity:
    name: str
    inn: str
    kpp: str | None

    def __str__(self) -> str:
        if self.kpp is None:
            return f"{self.name}, ИНН {self.inn}"
        else:
            return f"{self.name}, ИНН {self.inn}, КПП {self.kpp}"

    @classmethod
    def from_tinkoff_bank_statement(cls, bank_statement_response: SimpleJSONType) -> list["LegalEntity"]:
        operations = bank_statement_response["operation"]  # type: ignore

        return [
            cls(
                name=operation["payerName"],
                inn=operation["payerInn"],
                kpp=operation.get("payerKpp", None),
            )
            for operation in operations
        ]
