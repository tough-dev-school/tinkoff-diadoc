import pytest


@pytest.fixture(autouse=True)
def mock_diadoc_get_counteragent(mocker, ya_diadoc_entity):
    return mocker.patch("diadoc.client.DiadocClient.get_counteragents", return_value=[ya_diadoc_entity])


@pytest.fixture
def get_counteragents(tinkoff_to_diadoc, diadoc_entity):
    return lambda: tinkoff_to_diadoc.get_counteragents(diadoc_entity)


def test_return_diadoc_entities(get_counteragents, ya_diadoc_entity):
    got = get_counteragents()

    assert got == [ya_diadoc_entity]


def test_diadoc_client_was_called(get_counteragents, mock_diadoc_get_counteragent, diadoc_entity):
    get_counteragents()

    mock_diadoc_get_counteragent.assert_called_with(diadoc_entity.diadoc_id)
