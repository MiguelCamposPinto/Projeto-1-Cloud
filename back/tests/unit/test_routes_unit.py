import json
import pytest
from back.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c

def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    payload = res.get_json()
    assert 'ok' in payload and payload['ok'] is True
