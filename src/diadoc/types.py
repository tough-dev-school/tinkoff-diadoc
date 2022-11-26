from typing import Literal, TypedDict


class DiadocOrganization(TypedDict):
    ShortName: str
    Inn: str
    Kpp: str
    OrgId: str
    IsActive: bool
    IsRoaming: bool


DiadocCounteragentStatus = Literal[
    "UnknownCounteragentStatus",
    "IsMyCounteragent",
    "InvitesMe",
    "IsInvitedByMe",
    "RejectsMe",
    "IsRejectedByMe",
    "NotInCounteragentList",
]


class DiadocCounteragent(TypedDict):
    IndexKey: str
    Organization: DiadocOrganization
    CurrentStatus: DiadocCounteragentStatus
