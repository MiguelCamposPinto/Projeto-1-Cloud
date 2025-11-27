from datetime import datetime
from sharedScope import *

#POST /api/messages faz trim em author/text
def test_post_message_trims_whitespace(client):
    resp = client.post(
        "/api/messages",
        json={"author": "   enzo   ", "text": "   oi teste   "},
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["author"] == "enzo"
    assert data["text"] == "oi teste"


#POST retorna id e created_at no formato ISO (terminando com Z)
from datetime import datetime, timezone

def test_post_message_returns_id_and_created_at(client):
    resp = client.post(
        "/api/messages",
        json={"author": "user", "text": "mensagem"},
    )
    assert resp.status_code == 201
    data = resp.get_json()

    created_at = data.get("created_at")

    # tem id e created_at
    assert isinstance(data.get("id"), int)
    assert isinstance(created_at, str)

    # consegue fazer parse como ISO 8601
    parsed = datetime.fromisoformat(created_at)
    # timezone-aware em UTC
    assert parsed.tzinfo == timezone.utc

    # 12) POST muito grande (stress test)
def test_post_message_with_large_text(client):
    long_text = "a" * 5000
    resp = client.post("/api/messages", json={"author": "tester", "text": long_text})
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["text"] == long_text
    assert data["author"] == "tester"