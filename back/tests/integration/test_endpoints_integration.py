import requests

BASE_URL = "http://127.0.0.1:8085"

def test_post_and_list_messages():
    # envia uma mensagem
    r = requests.post(f"{BASE_URL}/api/messages", json={
        "author": "tests",
        "text": "hello from test"
    })
    assert r.status_code == 201
    j = r.json()
    assert "id" in j

    # consulta mensagens
    r = requests.get(f"{BASE_URL}/api/messages")
    assert r.status_code == 200
    msgs = r.json()
    assert any(m["author"] == "tests" for m in msgs)
