from sharedScope import *

#POST /api/messages sem body -> 400
def test_post_message_requires_body(client):
    resp = client.post("/api/messages", json=None)
    assert resp.status_code == 400

    data = resp.get_json()
    assert "error" in data
    assert "author and text required" in data["error"]

#POST /api/messages sem author/text -> 400
def test_post_message_requires_author_and_text(client):
    resp = client.post("/api/messages", json={})
    assert resp.status_code == 400

    data = resp.get_json()
    assert "error" in data
    assert "author and text required" in data["error"]

#POST com corpo inválido (não JSON) -> 400  
def test_post_message_non_json_returns_400(client):
    resp = client.post(
        "/api/messages",
        data = "not json",
        content_type="text/plain",
    )
    assert resp.status_code == 400
    assert "error" in resp.get_json()

#POST /api/messages com author/text vazios -> 400
def test_post_message_empty_author_or_text(client):
    resp = client.post("/api/messages", json={"author": "", "text": "algum texto"})
    assert resp.status_code == 400

    resp2 = client.post("/api/messages", json={"author": "alguem", "text": ""})
    assert resp2.status_code == 400