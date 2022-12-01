import pytest


@pytest.fixture(autouse=True)
def _set_message_to_counteragents(monkeypatch):
    monkeypatch.setenv("MESSAGE_TO_ACQUIRE_COUNTERAGENT", "Давай запартнеримся в Диадок!")


@pytest.fixture
def mock_acquire_counteragent(mocker):
    return mocker.patch("diadoc.client.DiadocClient.acquire_counteragent")


@pytest.fixture
def send_invites(tinkoff_to_diadoc):
    return lambda *partners: tinkoff_to_diadoc.send_invites(partners)


def test_call_acquire_counteragent_for_every_partner(send_invites, partner, ya_partner, mock_acquire_counteragent, mocker):
    send_invites(partner, ya_partner)

    mock_acquire_counteragent.assert_has_calls(
        calls=[
            mocker.call(diadoc_id=partner.diadoc_id, message="Давай запартнеримся в Диадок!"),
            mocker.call(diadoc_id=ya_partner.diadoc_id, message="Давай запартнеримся в Диадок!"),
        ],
        any_order=True,
    )
