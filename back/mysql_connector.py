import os
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "127.0.0.1"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASS", "rootpass"),
        database=os.environ.get("DB_NAME", "appdb"),
        autocommit=True
    )
