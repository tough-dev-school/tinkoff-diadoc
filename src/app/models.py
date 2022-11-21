from dataclasses import dataclass


@dataclass
class BankAccount:
    account_number: str


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
