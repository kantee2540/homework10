import sqlite3
import re

address_info = []
location_data = []


def read_file():
    try:
        with open("RawAddressData.txt", "r", encoding="utf16") as f:
            read_data = f.read().splitlines()
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
    address= None
    swine = None
    soi = None
    road = None
    zone = None
    province = None
    postal_code = None

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

        elif "ซ." in y or "ซอย" in y:
            if y == 'ซอย.' or y == 'ซ.':
                soi = splited_data[x + 1]
            else:
                soi = find_soi(y)

        elif 'ถนน' in y or 'ถ.' in y:
            if y == 'ถนน':
                road = splited_data[x + 1]
            else:
                road = find_road(y)

        elif 'เขต' in y or 'อ.' in y:
            zone = find_zone(y)

        elif 'จ.' in y:
            province = find_province(y)

        else:
            for i in location_data:
                if y != "":
                    if y in i["Zone"] and y not in i["Province"] and y != "เมือง":
                        zone = y
                        break

                    elif y in i["Province"]:
                        province = y
                        break

                    elif y in i["PostalCode"] and len(y) == 5:
                        postal_code = y
                        break

            result = re.search(r'/', y)
            if result:
                address = y

    return {"address": address, "swine": swine, "soi": soi, "road": road, "zone": zone, "province": province, "postalcode": postal_code}


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
    end_soi = 0
    for i in range(len(data)):
        if data[i] == 'ย' or data[i] == '.':
            end_soi = i + 1
            break

    return data[end_soi:None]


def find_road(data):
    end_road = 0
    for i in range(len(data)):
        if data[i] == '.':
            end_road = i + 1
            break
        elif data[i] == 'น':
            end_road = i + 2
            break

    return data[end_road:None]


def find_zone(data):
    end_zone = 0
    for i in range(len(data)):
        if data[i] == '.':
            end_zone = i + 1
            break

        elif data[i] == 'ต':
            end_zone = i + 1
            break

    return data[end_zone:None]


def find_province(data):
    end_zone = 0
    for i in range(len(data)):
        if data[i] == '.':
            end_zone = i + 1
    return data[end_zone:None]


def read_database():
    try:
        db = "Thai.db"
        with (sqlite3.connect(db)) as conn:
            conn.row_factory = sqlite3.Row
            sql_command = """SELECT * FROM Location_Thai"""
            cursor = conn.execute(sql_command)
            for i in cursor:
                location_data.append({"Province": i["Province"],
                                      "District": i["District"],
                                      "PostalCode": str(i["PostalCode"]),
                                      "Zone": i["Zone"]})
            print(location_data)

    except Exception as e:
        print("Error {}".format(e))

    return location_data


def insert_to_database(data):
    try:
        with sqlite3.connect("AddressData.db") as conn:
            sql_command = "INSERT INTO Address VALUES ('10', 'f', 'f', 's', 'a', 's', 'd', 'f', 'p')"
            conn.executescript(sql_command)

    except Exception as e:
        print("Error {}".format(e))


if __name__ == '__main__':
    read_database()
    read_file()
    txt = '14/6  asdf 111 ถ.ลาดพร้าวแขวงคลองจั่น เขตลาดพร้าว 10240'
    # result = re.search(r'/', txt)
    # if result:
    #     print("YES")
    # else:
    #     print("NO")
