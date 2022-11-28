from typing import Literal, TypeAlias, TypedDict

DiadocId: TypeAlias = str
DiadocTaskId: TypeAlias = str


class DiadocOrganization(TypedDict):
    ShortName: str
    Inn: str
    Kpp: str
    OrgId: DiadocId
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
