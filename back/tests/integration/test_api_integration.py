import pytest
from back.app import app
from back.mysql_connector import get_connection


@pytest.fixture(scope="function", autouse=True)
def clean_db():
    """
    Limpa a tabela messages antes de cada teste de integração.
    Integração aqui = app Flask + MySQL real.
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
