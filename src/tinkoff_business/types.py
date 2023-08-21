from typing import NotRequired, TypedDict


class TinkoffMyRequisites(TypedDict):
    fullName: str
    inn: str
    kpp: NotRequired[str]


class TinkoffMyCompany(TypedDict):
    name: str
    city: str
    requisites: TinkoffMyRequisites


class TinkoffPayer(TypedDict):
    name: str
    inn: NotRequired[str]
    kpp: NotRequired[str]


class TinkoffOperation(TypedDict):
    operationId: str
    payer: TinkoffPayer


class TinkoffStatement(TypedDict):
    operations: list[TinkoffOperation]
    nextCursor: NotRequired[str]
