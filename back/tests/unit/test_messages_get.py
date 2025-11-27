from sharedScope import *

#GET /api/messages retorna lista vazia quando não há mensagens
def test_list_messages_empty_returns_empty_list(client):
    resp = client.get("/api/messages")
    assert resp.status_code == 200

    data = resp.get_json()
    assert isinstance(data, list)
    assert len(data) == 0

#GET /api/messages ingora parâmetros inválidos
def test_list_messages_ignores_unknown_params(client):
    client.post("/api/messages", json={"author": "a", "text": "msg"})
    resp = client.get("/api/messages?since_id=abc")
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == 1  # retorna normalmente

#GET /api/messages retorna mensagens em ordem crescente de id
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


#GET /api/messages com since_id filtra corretamente
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

