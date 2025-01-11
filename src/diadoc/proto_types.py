from typing import Literal, TypedDict


class Box(TypedDict):
    """https://developer.kontur.ru/docs/diadoc-api/proto/Box.html"""

    BoxId: str  # exists in response, but not used — according to docs BoxIdGuid should be used as boxId param
    Title: str
    BoxIdGuid: str


class Organization(TypedDict):
    """https://developer.kontur.ru/docs/diadoc-api/proto/Organization.html"""

    ShortName: str
    Inn: str
    Kpp: str
    OrgId: str
    Boxes: list[Box]  # boxes contains one and only one box
    IsActive: bool
    IsRoaming: bool


CounteragentStatus = Literal[
    "UnknownCounteragentStatus",
    "IsMyCounteragent",
    "InvitesMe",
    "IsInvitedByMe",
    "RejectsMe",
    "IsRejectedByMe",
    "NotInCounteragentList",
]


class Counteragent(TypedDict):
    """https://developer.kontur.ru/docs/diadoc-api/proto/Counteragent.html"""

    IndexKey: str
    Organization: Organization
    CurrentStatus: CounteragentStatus
