from sharedScope import *
from datetime import datetime

# 1) /health integrado com app e filesystem (FRONT_DIR/index.html)
def test_integration_health_endpoint(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["ok"] is True
    # Só checa que as chaves existem
    assert "front_dir" in data
    assert "index_exists" in data


# 2) fluxo completo: insere mensagem (POST) e recupera (GET) do banco
def test_integration_create_and_list_messages(client):
    payload = {"author": "integration", "text": "hello from integration"}
    r = client.post("/api/messages", json=payload)
    assert r.status_code == 201
    created = r.get_json()
    assert "id" in created

    r2 = client.get("/api/messages")
    assert r2.status_code == 200
    msgs = r2.get_json()
    assert any(m["id"] == created["id"] for m in msgs)


# 3) erro de validação via HTTP (payload inválido) integrando com a lógica da app
def test_integration_validation_error(client):
    # sem text
    r = client.post(
        "/api/messages",
        json={"author": "alguem", "text": ""},
    )
    assert r.status_code == 400
    data = r.get_json()
    assert "error" in data
    assert "author and text required" in data["error"]

# 4) GET "/" serve index.html corretamente
def test_integration_root_serves_index_html(client, monkeypatch, tmp_path):
    #cria um front falso temporário
    front_fake = tmp_path
    fake_index = front_fake / "index.html"
    fake_index.write_text("<html><body>Fake Index</body></html>")

    #substitui front_dir dentro do app.py para apontar para o front falso
    monkeypatch.setattr("back.app.FRONT_DIR", front_fake)
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Fake Index" in resp.data

# 5) GET /api/messages
def test_integration_created_at_from_database(client):
    #cria uma mensagem (escreve no bd)
    r = client.post("/api/messages", json = {"author": "db", "text": "test"})
    assert r.status_code == 201

    #pega mensagem via GET method
    resp = client.get("/api/messages")
    assert resp.status_code == 200
    msgs = resp.get_json()

    assert len(msgs) == 1
    created_at = msgs[0]["created_at"]

    dt = datetime.fromisoformat(created_at)
    assert isinstance(dt, datetime)