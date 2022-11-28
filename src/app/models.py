from dataclasses import dataclass


@dataclass
class BankAccount:
    account_number: str


@dataclass
class LegalEntity:
    name: str
    inn: str
    kpp: str | None

    @property
    def inn_kpp(self):
        return f"{self.inn}{self.kpp}" if self.kpp else f"{self.inn}"
