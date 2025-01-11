import pytest


@pytest.fixture
def my_company(partner):
    return partner


@pytest.fixture(autouse=True)
def mock_diadoc_get_counteragent(mocker, ya_partner):
    return mocker.patch("diadoc.client.DiadocClient.get_counteragents", return_value=[ya_partner])


@pytest.fixture
def get_counteragents(tinkoff_to_diadoc, my_company):
    return lambda: tinkoff_to_diadoc.get_counteragents(my_company=my_company)


def test_return_diadoc_partners(get_counteragents, ya_partner):
    got = get_counteragents()

    assert got == [ya_partner]


def test_diadoc_client_was_called(get_counteragents, mock_diadoc_get_counteragent, my_company):
    get_counteragents()

    mock_diadoc_get_counteragent.assert_called_with(my_company)
