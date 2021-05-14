import pytest # type: ignore
import app # type: ignore

@pytest.fixture
def api():
    api = app.app.test_client()
    return api