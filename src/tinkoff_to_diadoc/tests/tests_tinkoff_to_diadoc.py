import pytest

from diadoc.exceptions import DiadocHTTPException
from tinkoff_business.exceptions import TinkoffBusinessHTTPException
from tinkoff_to_diadoc import TinkoffToDiadoc


@pytest.fixture
def exception_diadoc_client(mocker):
    return mocker.patch("diadoc.http.DiadocHTTP.request", side_effect=DiadocHTTPException)


@pytest.fixture
def exception_tinkoff_business_client(mocker):
    return mocker.patch("tinkoff_business.http.TinkoffBusinessHTTP.request", side_effect=TinkoffBusinessHTTPException)


@pytest.fixture
def mock_capture_exception(mocker):
    return mocker.patch("sentry_sdk.capture_exception")


@pytest.fixture
def tinkoff_to_diadoc():
    return lambda: TinkoffToDiadoc().act()


def test_capture_exception_if_diadoc_exception_occurred(tinkoff_to_diadoc, exception_diadoc_client, mock_capture_exception):
    tinkoff_to_diadoc()

    mock_capture_exception.assert_called_once()


def test_capture_exception_if_tinkoff_business_exception_occurred(tinkoff_to_diadoc, exception_tinkoff_business_client, mock_capture_exception):
    tinkoff_to_diadoc()

    mock_capture_exception.assert_called_once()
