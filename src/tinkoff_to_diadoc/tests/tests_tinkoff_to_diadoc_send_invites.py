import pytest

from diadoc.models import DiadocPartner


@pytest.fixture(autouse=True)
def _set_message_to_counteragents(monkeypatch):
    monkeypatch.setenv("MESSAGE_TO_ACQUIRE_COUNTERAGENT", "Давай запартнеримся в Диадок!")


@pytest.fixture
def mock_acquire_counteragent(mocker):
    return mocker.patch("diadoc.client.DiadocClient.acquire_counteragent")


@pytest.fixture
def my_company():
    return DiadocPartner(
        name="Пивзавод",
        inn="771245768212",
        kpp=None,
        diadoc_id="75fcac12-ec63-4cdd-9076-87a8a2e6e8ba",
        is_active=True,
        is_roaming=False,
    )


@pytest.fixture
def send_invites(tinkoff_to_diadoc):
    return lambda my_company, partners: tinkoff_to_diadoc.send_invites(my_company, partners)


def test_call_acquire_counteragent_for_every_partner(send_invites, my_company, partner, ya_partner, mock_acquire_counteragent, mocker):
    send_invites(my_company, [partner, ya_partner])

    mock_acquire_counteragent.assert_has_calls(
        calls=[
            mocker.call(my_company.diadoc_id, partner.diadoc_id, "Давай запартнеримся в Диадок!"),
            mocker.call(my_company.diadoc_id, ya_partner.diadoc_id, "Давай запартнеримся в Диадок!"),
        ],
        any_order=True,
    )
