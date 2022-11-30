from dataclasses import dataclass
from dataclasses import field


@dataclass
class BankAccount:
    account_number: str


@dataclass(unsafe_hash=True)
class LegalEntity:
    name: str = field(hash=False, compare=False)
    inn: str
    kpp: str | None

    @property
    def inn_kpp(self):
        return f"{self.inn}{self.kpp}" if self.kpp else f"{self.inn}"
