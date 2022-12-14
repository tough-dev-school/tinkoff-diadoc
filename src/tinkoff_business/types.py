from typing import TypedDict

from typing_extensions import NotRequired


class TinkoffRequisites(TypedDict):
    fullName: str
    inn: str
    kpp: NotRequired[str]


class TinkoffCompany(TypedDict):
    name: str
    city: str
    requisites: TinkoffRequisites


class TinkoffOperation(TypedDict):
    operationId: str
    payerName: str
    payerInn: str
    payerKpp: NotRequired[str]


class TinkoffBankStatement(TypedDict):
    accountNumber: str
    operation: list[TinkoffOperation]
