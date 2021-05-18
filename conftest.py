import pytest # type: ignore
import app # type: ignore
from models import recipes, users # type: ignore

@pytest.fixture
def api(monkeypatch):
    test_user = 'test'
    monkeypatch.setattr(recipes, "mongoDB_username", test_user)
    monkeypatch.setattr(users, "mongoDB_username", test_user)
    api = app.app.test_client()
    return api