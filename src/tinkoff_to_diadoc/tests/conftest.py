import pytest
from uuid import uuid4

from app.models import LegalEntity
from diadoc.models import DiadocPartner
from diadoc.models import PartnershipStatus
from tinkoff_business.models import TinkoffBankAccount
from tinkoff_to_diadoc import TinkoffToDiadoc


@pytest.fixture
def bank_account():
    return TinkoffBankAccount(account_number="100500")


@pytest.fixture
def ya_bank_account():
    return TinkoffBankAccount(account_number="900500")


@pytest.fixture
def legal_entity():
    return LegalEntity(name="ИП Конфеты и программы", inn="772354588891", kpp=None)


@pytest.fixture
def partner():
    return DiadocPartner(
        name="ИП Конфеты и программы",
        inn="772354588891",
        kpp=None,
        diadoc_id=str(uuid4()),
        diadoc_box_id=str(uuid4()),
        diadoc_partnership_status=None,
        is_active=True,
        is_roaming=False,
    )


@pytest.fixture
def ya_partner():
    return DiadocPartner(
        name="ООО Учись больше",
        inn="7723993400",
        kpp="997950001",
        diadoc_id=str(uuid4()),
        diadoc_box_id=str(uuid4()),
        diadoc_partnership_status=None,
        is_active=True,
        is_roaming=True,
    )


@pytest.fixture
def create_counteragent():
    def _create(partner: DiadocPartner, partnership_status: PartnershipStatus):
        return DiadocPartner(
            name=partner.name,
            inn=partner.inn,
            kpp=partner.kpp,
            diadoc_id=partner.diadoc_id,
            diadoc_box_id=partner.diadoc_box_id,
            diadoc_partnership_status=partnership_status,
            is_active=True,
            is_roaming=False,
        )

    return _create


@pytest.fixture
def tinkoff_to_diadoc():
    return TinkoffToDiadoc()
