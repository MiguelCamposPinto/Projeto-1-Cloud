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