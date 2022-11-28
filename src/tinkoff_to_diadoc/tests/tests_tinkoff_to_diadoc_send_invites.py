import pytest


@pytest.fixture(autouse=True)
def _set_message_to_counteragents(monkeypatch):
    monkeypatch.setenv("MESSAGE_TO_ACQUIRE_COUNTERAGENT", "Давай запартнеримся в Диадок!")


@pytest.fixture
def mock_acquire_counteragent(mocker):
    return mocker.patch("diadoc.client.DiadocClient.acquire_counteragent")


@pytest.fixture
def send_invites(tinkoff_to_diadoc):
    return lambda diadoc_entities: tinkoff_to_diadoc.send_invites(diadoc_entities)


def test_call_acquire_counteragent_for_every_counteragent(send_invites, diadoc_entity, ya_diadoc_entity, mock_acquire_counteragent, mocker):
    send_invites([diadoc_entity, ya_diadoc_entity])

    mock_acquire_counteragent.assert_has_calls(
        calls=[
            mocker.call(diadoc_id=diadoc_entity.diadoc_id, message="Давай запартнеримся в Диадок!"),
            mocker.call(diadoc_id=ya_diadoc_entity.diadoc_id, message="Давай запартнеримся в Диадок!"),
        ],
        any_order=True,
    )
