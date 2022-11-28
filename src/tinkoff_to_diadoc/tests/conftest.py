import pytest
from uuid import uuid4

from app.models import BankAccount
from app.models import LegalEntity
from diadoc.models import DiadocLegalEntity
from tinkoff_to_diadoc import TinkoffToDiadoc


@pytest.fixture
def bank_account():
    return BankAccount(account_number="100500")


@pytest.fixture
def ya_bank_account():
    return BankAccount(account_number="900500")


@pytest.fixture
def entity():
    return LegalEntity(name="ИП Конфеты и программы", inn="772354588891", kpp=None)


@pytest.fixture
def diadoc_entity():
    return DiadocLegalEntity(
        name="ИП Конфеты и программы",
        inn="772354588891",
        kpp=None,
        diadoc_id=str(uuid4()),
        diadoc_partnership_status=None,
        is_active=True,
    )


@pytest.fixture
def ya_diadoc_entity():
    return DiadocLegalEntity(
        name="ООО Учись больше",
        inn="7723993400",
        kpp="997950001",
        diadoc_id=str(uuid4()),
        diadoc_partnership_status=None,
        is_active=True,
    )


@pytest.fixture
def tinkoff_to_diadoc():
    return TinkoffToDiadoc()
