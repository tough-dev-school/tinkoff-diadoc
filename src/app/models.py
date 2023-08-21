from dataclasses import dataclass
from dataclasses import field


@dataclass(frozen=True)
class LegalEntity:
    name: str = field(hash=False, compare=False)
    inn: str
    kpp: str | None

    @property
    def inn_kpp(self):
        return f"{self.inn}{self.kpp}" if self.kpp else f"{self.inn}"
