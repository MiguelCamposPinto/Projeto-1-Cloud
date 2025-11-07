from flask import Flask, request, jsonify, send_from_directory, abort
import mysql.connector, os
from datetime import datetime
from pathlib import Path
from mysql_connector import get_connection

APP_DIR = Path(__file__).resolve().parent
FRONT_DIR = (APP_DIR / ".." / "front").resolve()
DB_PATH = APP_DIR / "chat.db"

app = Flask(__name__, static_folder=None)

def get_db():
    return get_connection()

def init_db():
    conn = get_db()
    if(conn.is_connected()):
        print("Conectado!")
    else:
        print("Erro ao conectar ao DB!")
        
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INT PRIMARY KEY AUTO_INCREMENT,
            author VARCHAR(255) NOT NULL,
            text   TEXT NOT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close(); conn.close()

init_db()

@app.get("/health")
def health():
    return jsonify(
        ok=True,
        front_dir=str(FRONT_DIR),
        index_exists=(FRONT_DIR / "index.html").exists()
    )

@app.get("/api/messages")
def list_messages():
    since_id = request.args.get("since_id", type=int)
    conn = get_db(); cur = conn.cursor()
    if since_id is None:
        cur.execute("SELECT id, author, text, created_at FROM messages ORDER BY id ASC")
    else:
        cur.execute("SELECT id, author, text, created_at FROM messages WHERE id > %s ORDER BY id ASC", (since_id,))
    rows = [dict(id=r[0], author=r[1], text=r[2], created_at=r[3]) for r in cur.fetchall()]
    cur.close(); conn.close()
    return jsonify(rows)

@app.post("/api/messages")
def post_message():
    data = request.get_json(silent=True) or {}
    author = (data.get("author") or "").strip()
    text   = (data.get("text") or "").strip()
    if not author or not text:
        return jsonify(error="author and text required"), 400
    conn = get_db(); cur = conn.cursor()
    cur.execute("INSERT INTO messages(author, text) VALUES(%s, %s)", (author, text))
    conn.commit()
    new_id = cur.lastrowid
    cur.close(); conn.close()
    return jsonify(id=new_id, author=author, text=text, created_at=datetime.utcnow().isoformat()+"Z"), 201

@app.get("/")
def index():
    index_path = FRONT_DIR / "index.html"
    if not index_path.exists():
        app.logger.error("index.html não encontrado em: %s", index_path)
        abort(404)
    return send_from_directory(FRONT_DIR, "index.html")

@app.get("/front/<path:filename>")
def front_assets(filename):
    file_path = FRONT_DIR / filename
    if not file_path.exists():
        app.logger.error("Asset não encontrado: %s", file_path)
        abort(404)
    return send_from_directory(FRONT_DIR, filename)

if __name__ == "__main__":
    app.logger.info("FRONT_DIR: %s", FRONT_DIR)
    app.run(host="0.0.0.0", port=8085, debug=False)
