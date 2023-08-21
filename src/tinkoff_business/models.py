from dataclasses import dataclass


@dataclass(frozen=True)
class TinkoffBankAccount:
    account_number: str
