import sqlite3


def read_file():
    try:
        with open("RawAddressData.txt", "r", encoding="utf16") as f:
            data = f.readlines()
            for i in data:
                print(i)

            insert_to_database(data)

    except Exception as e:
        print("Error {}".format(e))


def insert_to_database(data):
    try:
        with sqlite3.connect("AddressData.db") as conn:
            sql_command = "INSERT INTO Address VALUES ('10', 'f', 'f', 's', 'a', 's', 'd', 'f', 'p')"
            conn.executescript(sql_command)

    except Exception as e:
        print("Error {}".format(e))


read_file()
