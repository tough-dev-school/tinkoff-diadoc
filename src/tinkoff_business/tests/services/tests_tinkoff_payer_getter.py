from app.models import LegalEntity
from tinkoff_business.services import TinkoffPayerGetter


def test_get_payers(bank_statement_json):
    got = TinkoffPayerGetter(bank_statement_json)()

    assert len(got) == 2
    assert LegalEntity(name="Петрова Александра Ивановна", inn="100500", kpp=None) in got
    assert LegalEntity(name='ООО "ПЕРЧИК"', inn="900600", kpp="200500") in got
