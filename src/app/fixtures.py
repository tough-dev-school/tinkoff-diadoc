import json
import pytest


@pytest.fixture
def get_fixture():
    def _load(filename: str, *, directory_path: str):
        with open(f"{directory_path}{filename}", "r") as fp:
            return json.load(fp)

    return _load
