import mysql.connector

#7 - test unit
# ver se ao mudar esses dados se o bd nega conexao
def get_connection():
    return mysql.connector.connect(
        host="192.168.80.130",
        user="enzo",
        password="1234",
        database="appdb"
    )