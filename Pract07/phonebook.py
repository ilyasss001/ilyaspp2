import psycopg2
import csv
from connect import get_connection

conn = get_connection()

cur = conn.cursor()

def create_table():
    cur.execute("""CREATE TABLE IF NOT EXISTS phonebook (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(255),
    second_name VARCHAR(255),
    phone_number VARCHAR(255) UNIQUE
    );
    """)
    conn.commit()
    print("Table created")

def upload_data_from_csv_file():
    with open("contacts.csv", "r") as f:
        reader = csv.reader(f)
        next(reader) #to skip columns
        for row in reader:
            cur.execute("""INSERT INTO phonebook (first_name, second_name, phone_number) VALUES
                (%s, %s, %s)""",
                (row[0], row[1], row[2])
                )
        conn.commit()
        print("Data inserted to the table from csv file")

def upload_data_from_console():
    print("How many rows?")
    n = int(input())
    for i in range(0, n):
        x, z, y = input().split()
        cur.execute("""INSERT INTO phonebook (first_name, second_name, phone_number) VALUES (%s, %s, %s)""",
            (x, z, y)
        )
    conn.commit()
    print("Data inserted to the table from console")

def change_name_or_phone():
    print("What do you want to change?")
    print("write 1 if you want to change name or write 2 if you want to change phone number")
    a = input()
    if a == "1":
        print("Whats the new name?")
        fnewname1, snewname2 = input().split()
        print("Whats the phone number from the last owner?")
        oldphone = input()
        sql = """UPDATE phonebook
                SET first_name = %s, second_name = %s
                WHERE phone_number = %s"""
        cur.execute(sql, (fnewname1, snewname2, oldphone))
        conn.commit()
    else:
        print("Whats the old name?")
        oldname1, oldname2 = input().split()
        print("Whats the new phone number?")
        new_phone_number = input()
        sql = """UPDATE phonebook
                SET phone_number = %s
                WHERE first_name = %s AND second_name = %s"""
        cur.execute(sql, (new_phone_number, oldname1, oldname2))
        conn.commit()

def querying_data_from_the_table():
    print("1 - get full name typing phone number")
    print("2 - get phone number typing first name or second name")
    print("3 - get the whole table")
    print("4 - get specified amount of rows")
    print("5 - ordered table by the first name")
    print("6 - second name that start with specified letter")
    a = int(input())
    if a == 1:
        print("Type phone number:")
        phonenumber = input()
        cur.execute("SELECT first_name, second_name FROM phonebook WHERE phone_number = %s", (phonenumber,))
        row = cur.fetchone()
        if row:
            print(row)
        else:
            print("Not found")

    elif a == 2:
        print("2 - second or 1 - first name?")
        b = int(input())
        if b == 1:
            print("Type first name:")
            first = input()
            cur.execute("""SELECT phone_number FROM phonebook WHERE first_name = %s""", (first,))
            rows = cur.fetchall()
            if len(rows) > 0:
                for row in rows:
                    print(row)
            else:
                print("Not found")
        else:
            print("Type second name:")
            second = input()
            cur.execute("""SELECT phone_number FROM phonebook WHERE second_name = %s""", (second,))
            rows = cur.fetchall()
            if len(rows) > 0:
                for row in rows:
                    print(row)
            else:
                print("Not found")
    elif a == 3:
        cur.execute("SELECT * FROM phonebook ORDER BY id")
        rows = cur.fetchall()
        if len(rows) > 0:
            for row in rows:
                print(row)
        else:
            print("Not found")
    elif a == 4:
        n = int(input())
        cur.execute("""SELECT * FROM phonebook ORDER BY id""")
        rows = cur.fetchmany(n)
        if len(rows) > 0:
            for row in rows:
                print(row)
        else:
            print("Not found")
    elif a == 5:
        cur.execute("""SELECT * FROM phonebook ORDER BY first_name""")
        rows = cur.fetchall()
        if len(rows) > 0:
            for row in rows:
                print(row)
        else:
            print("Not found")
    else:
        print("Which letter should start second name?")
        letter = input()
        cur.execute("""SELECT second_name FROM phonebook WHERE second_name LIKE %s""", (letter + "%",))
        rows = cur.fetchall()
        if len(rows) > 0:
            for row in rows:
                print(row)
        else:
            print("Not found")

def deleting_data_from_table():
    print("1 - delete by first name, 2 - delete by second name, 3 - delete by phone number")
    a = int(input())
    if a == 1:
        print("Enter first name:")
        first = input()
        cur.execute("""DELETE FROM phonebook WHERE first_name = %s""", (first,))
        conn.commit()
    elif a == 2:
        print("Enter second name:")
        second = input()
        cur.execute("""DELETE FROM phonebook WHERE second_name = %s""", (second,))
        conn.commit()
    else:
        print("Enter phone number:")
        phonenumber = input()
        cur.execute("""DELETE FROM phonebook WHERE phone_number = %s""", (phonenumber,))
        conn.commit()

def menu():
    create_table()
    print("1 - exit")
    print("2 - upload data from csv file")
    print("3 - upload data from console")
    print("4 - update data in table by name or phone number")
    print("5 - get data through querying")
    print("6 - delete data from table by name or phone number")
    while True:
        a = int(input())
        if a == 1:
            break
        elif a == 2:
            upload_data_from_csv_file()
        elif a == 3:
            upload_data_from_console()
        elif a == 4:
            change_name_or_phone()
        elif a == 5:
            querying_data_from_the_table()
        elif a == 6:
            deleting_data_from_table()
    return None
menu()

cur.close()
conn.close()