import json
import pytest


@pytest.fixture
def bank_accounts_json():
    with open("./tinkoff_business/tests/.fixtures/bank-accounts.json", "r") as fp:
        response_json = json.load(fp)

        response_json[0]["AccountNumber"] = "40802678901234567890"
        response_json[0]["AccountNumber"] = "100500"

        return response_json


@pytest.fixture
def bank_statement_json():
    with open("./tinkoff_business/tests/.fixtures/bank-statement.json") as fp:
        bank_statement_response = json.load(fp)

        bank_statement_response["operation"][0]["payerName"] = "Петрова Александра Ивановна"
        bank_statement_response["operation"][0]["payerInn"] = "100500"
        bank_statement_response["operation"][0].pop("payerKpp", None)

        bank_statement_response["operation"][1]["payerName"] = 'ООО "ПЕРЧИК"'
        bank_statement_response["operation"][1]["payerInn"] = "900600"
        bank_statement_response["operation"][1]["payerKpp"] = "200500"

        return bank_statement_response
