from app.models import BankAccount
from tinkoff_business.services import TinkoffBankAccountGetter


def test_tinkoff_bank_account_getter(bank_accounts_json):
    got = TinkoffBankAccountGetter(bank_accounts_json)()

    assert len(got) == 2
    assert BankAccount(account_number="40802678901234567890") in got
    assert BankAccount(account_number="100500") in got
