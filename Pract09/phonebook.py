from connect import get_connection
import psycopg2
conn = get_connection()
cur = conn.cursor()
def create_table():
    cur.execute("""CREATE TABLE IF NOT EXISTS phonebook2 (
    id SERIAL PRIMARY KEY,
    first_name TEXT,
    second_name TEXT,
    phone_number TEXT UNIQUE
    );""")
    conn.commit()
    print("Table created")

def pattern():
    print("Search object:")
    x = input()
    cur.execute("""SELECT * FROM get_user_name_or_phone_number_by_pattern(%s)""", (x,))
    rows = cur.fetchall()
    for row in rows:
        print(row)

def pagination():
    print("Type limit:")
    lim = int(input())
    print("How many rows you want to skip firstly?")
    off_set = int(input())
    cur.execute("""SELECT * FROM show_with_pagination(%s, %s)""", (lim, off_set,))
    rows = cur.fetchall()
    for row in rows:
        print(row)

def upsert():
    print("Type your frist name:")
    name_one = input()
    print("Type your second name:")
    name_two = input()
    print("Type your phone number:")
    p_phone_number = input()
    cur.execute("""CALL upsert_contact(%s, %s, %s)""", (name_one, name_two, p_phone_number))
    conn.commit()

def delete():
    print("Delete by what object: type it")
    x = input()
    cur.execute("CALL delete_by_name_or_phonenumber(%s)", (x,))
    conn.commit()

def validate():
    print("How many rows?")
    n = int(input())
    print("1name: 2name: phone_number:")
    name_one = []
    name_two = []
    phone = []
    for i in range(0, n):
        a, b, c = input().split()
        name_one.append(a)
        name_two.append(b)
        phone.append(c)
    cur.execute("CALL validate_phone_correctness(%s, %s, %s)", (name_one, name_two, phone))
    conn.commit()
        

def menu():
    create_table()
    print("1 - exit")
    print("2 - Search by pattern")
    print("3 - Get data with pagination")
    print("4 - Upsert")
    print("5 - Delete by name or phone number")
    print("6 - Validate phone correctness")
    while True:
        a = int(input())
        if a == 1:
            break
        elif a == 2:
            pattern()
        elif a == 3:
            pagination()
        elif a == 4:
            upsert()
        elif a == 5:
            delete()
        elif a == 6:
            validate()
    return None

menu()
cur.close()
conn.close()