from dataclasses import dataclass

from app.models import LegalEntity
from app.services import BaseService
from app.types import SimpleJSONType


@dataclass
class TinkoffPayerGetter(BaseService):
    bank_statement_response: SimpleJSONType

    def act(self) -> list[LegalEntity]:
        operations = self.bank_statement_response["operation"]  # type: ignore

        return [
            LegalEntity(
                name=operation["payerName"],
                inn=operation["payerInn"],
                kpp=operation.get("payerKpp", None),
            )
            for operation in operations
        ]
