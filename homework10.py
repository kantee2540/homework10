import sqlite3

address_info = []


def read_file():
    try:
        with open("RawAddressData.txt", "r", encoding="utf16") as f:
            read_data = f.readlines()
            for i in read_data:
                split_data = i.split(" ")
                print(get_information(split_data))
                # print(split_data)

        for i in address_info:
            print(i)
        # insert_to_database(data)data[1]

    except Exception as e:
        print("Error {}".format(e))


def get_information(splited_data):
    swine = None
    soi = None
    for x, y in enumerate(splited_data):
        if (("ม." in y) and ("กทม." not in y)) \
                or (("หมู่" in y) and ("หมู่บ้าน" not in y)):
            if y == "หมู่" or y == 'ม.':
                swine = splited_data[x + 1]
            else:
                swine = find_swine(y)
                for q, u in enumerate(swine):
                    if not u.isnumeric():
                        soi = swine[q:None]
                        swine = swine[0:q]
                        break

    return {"swine": swine, "soi": soi}


# Find Swine
def find_swine(data):
    my_str = ""
    swine_str = ""
    found_first = False
    for i in range(len(data)):
        if (data[i] == 'ห' or data[i] == 'ม') and not found_first:
            found_first = True
            my_str = data[i:None]

        elif data[i].isnumeric():
            swine_str = my_str[i:None]
            break

    return swine_str


# Find Soi
def find_soi(data):
    for x, y in enumerate(data):
        if "ซ." in y or "ซอย" in y:
            if y == "ซอย" or y == "ซอย." or y == "ซ.":
                soi = data[x + 1]
                return y + soi

            else:
                return y

    return "ไม่ระบุ"


def find_zone(data):
    return ""


def insert_to_database(data):
    try:
        with sqlite3.connect("AddressData.db") as conn:
            sql_command = "INSERT INTO Address VALUES ('10', 'f', 'f', 's', 'a', 's', 'd', 'f', 'p')"
            conn.executescript(sql_command)

    except Exception as e:
        print("Error {}".format(e))


if __name__ == '__main__':
    read_file()
