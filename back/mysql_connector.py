import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="192.168.80.130",
        user="enzo",
        password="1234",
        database="appdb"
    )