import pytest
from back.app import app
from back.mysql_connector import get_connection


@pytest.fixture(scope="function", autouse=True)
def clean_db():
    """
    Limpa a tabela messages antes de cada teste.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM messages")
    conn.commit()
    cur.close()
    conn.close()
    yield


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


# 1) /health básico
def test_health_ok(client):
    resp = client.get("/health")
    assert resp.status_code == 200

    data = resp.get_json()
    assert data["ok"] is True
    # só checa que front_dir é uma string e que a chave index_exists existe
    assert isinstance(data["front_dir"], str)
    assert "index_exists" in data


# 2) POST /api/messages sem body -> 400
def test_post_message_requires_body(client):
    resp = client.post("/api/messages", json=None)
    assert resp.status_code == 400

    data = resp.get_json()
    assert "error" in data
    assert "author and text required" in data["error"]


# 3) POST /api/messages com author/text vazios -> 400
def test_post_message_empty_author_or_text(client):
    resp = client.post("/api/messages", json={"author": "", "text": "algum texto"})
    assert resp.status_code == 400

    resp2 = client.post("/api/messages", json={"author": "alguem", "text": ""})
    assert resp2.status_code == 400


# 4) POST /api/messages faz trim em author/text
def test_post_message_trims_whitespace(client):
    resp = client.post(
        "/api/messages",
        json={"author": "   enzo   ", "text": "   oi teste   "},
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["author"] == "enzo"
    assert data["text"] == "oi teste"


# 5) POST retorna id e created_at no formato ISO (terminando com Z)
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



# 6) GET /api/messages retorna mensagens em ordem crescente de id
def test_list_messages_returns_all_in_order(client):
    # cria algumas mensagens
    texts = ["msg1", "msg2", "msg3"]
    for t in texts:
        r = client.post("/api/messages", json={"author": "a", "text": t})
        assert r.status_code == 201

    resp = client.get("/api/messages")
    assert resp.status_code == 200
    data = resp.get_json()

    returned_texts = [m["text"] for m in data]
    assert returned_texts == texts  # mesma ordem de inserção

    ids = [m["id"] for m in data]
    assert ids == sorted(ids)


# 7) GET /api/messages com since_id filtra corretamente
def test_list_messages_since_id_filters(client):
    # cria três mensagens
    r1 = client.post("/api/messages", json={"author": "a", "text": "um"})
    r2 = client.post("/api/messages", json={"author": "a", "text": "dois"})
    r3 = client.post("/api/messages", json={"author": "a", "text": "tres"})

    id1 = r1.get_json()["id"]
    id2 = r2.get_json()["id"]
    id3 = r3.get_json()["id"]

    # since_id = id1 -> deve vir id2 e id3
    resp = client.get(f"/api/messages?since_id={id1}")
    assert resp.status_code == 200
    data = resp.get_json()
    returned_ids = [m["id"] for m in data]
    assert returned_ids == [id2, id3]
