from sharedScope import *

def test_health_ok(client):
    resp = client.get("/health")
    assert resp.status_code == 200

    data = resp.get_json()
    assert data["ok"] is True
    # só checa que front_dir é uma string e que a chave index_exists existe
    assert isinstance(data["front_dir"], str)
    assert "index_exists" in data
