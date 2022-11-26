from dataclasses import dataclass


@dataclass
class BankAccount:
    account_number: str


@dataclass
class LegalEntity:
    name: str
    inn: str
    kpp: str | None
    diadoc_id: str | None = None
