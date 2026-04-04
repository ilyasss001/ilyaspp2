import psycopg2

def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        dbname="pp2_db",
        user="postgres",
        password="i@ene%XJ"
    )
    print("Connected:", conn.status)  # 1 = OK
    return conn