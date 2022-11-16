import pytest


@pytest.fixture(autouse=True)
def _set_env_tinkoff_token(set_env_variable):
    set_env_variable("TINKOFF_BUSINESS_TOKEN", "se7ret")
