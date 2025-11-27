from sharedScope import *
from unittest.mock import MagicMock

def test_delete_message_success(client, monkeypatch):

    fake_db = MagicMock()
    fake_cursor = fake_db.cursor.return_value
    fake_cursor.rowcount = 1  # simulando sucesso no delete

    # substitui get_db() por fake_db
    monkeypatch.setattr("back.app.get_db", lambda: fake_db)

    resp = client.delete("/api/messages/10")

    assert resp.status_code == 200
    data = resp.get_json()
    assert data["ok"] is True

    fake_cursor.execute.assert_called_once()
    fake_db.commit.assert_called_once()


def test_delete_message_not_found(client, monkeypatch):
    fake_db = MagicMock()
    fake_cursor = fake_db.cursor.return_value
    fake_cursor.rowcount = 0  # simulando que não encontrou a linha

    monkeypatch.setattr("back.app.get_db", lambda: fake_db)

    resp = client.delete("/api/messages/99999")

    assert resp.status_code == 404
    data = resp.get_json()
    assert "error" in data

    fake_cursor.execute.assert_called_once()
    fake_db.commit.assert_not_called()
