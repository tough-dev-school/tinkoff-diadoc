from typing import TypedDict


class DiadocOrganization(TypedDict):
    ShortName: str
    Inn: str
    Kpp: str
    OrgId: str
    IsActive: bool
    IsRoaming: bool
