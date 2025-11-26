from mysql.connector import connect
import os

cfg = {
  'host': os.environ.get('DB_HOST', '127.0.0.1'),
  'user': os.environ.get('DB_USER', 'root'),
  'password': os.environ.get('DB_PASS', ''),
  'database': os.environ.get('DB_NAME', 'appdb'),
}

conn = connect(**cfg)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS messages (
  id INT PRIMARY KEY AUTO_INCREMENT,
  author VARCHAR(255) NOT NULL,
  text TEXT NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()
cur.close()
conn.close()
print("DB ready")
