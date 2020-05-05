"""
Вспомогательные фунции для сбора логов.
Помогают получить отдельные поля логов
"""

import re
import time


date_dict = {}


def get_date(row: str):
    global date_dict
    space_count = 0
    index = 0
    '''
    while space_count < 3:
        if row[index] == ' ':
            space_count += 1
            if space_count == 3:
                break
        index += 1
        if index >= len(row):
            raise Exception("index >= len(row)")
    date = row[:index]
    res_row = row[index + 1:]
    '''
    tmp = ' '.join([x for x in row.split(" ") if x != ''])
    tmp = tmp.split(" ", 3)
    if len(tmp) >= 3:
        month = tmp[0]
        day =  tmp[1]
        time =  tmp[2]
        date = month + " " + day + " " + time

        res_row = tmp[3]
        check = date_dict.get(date)
        if check is None:
            date_dict[date] = 0
        else:
            date_dict[date] += 1
        return date + "."+ str(date_dict[date]), res_row
    return None


def show_error(all_errors: dict, error_code):
    import pprint
    for error_ULSK, error_data in all_errors.items():
        for error in error_data:
            if error_code == error[1]:
                print(error_code, ":", error_ULSK)


def get_flow_date(row: str):
    tmp = ' '.join([x for x in row.split(" ") if x != ''])
    tmp = tmp.split(" ", 3)
    if len(tmp) >= 3:
        month = tmp[0]
        day =  tmp[1]
        time =  tmp[2]
        date = month + " " + day + " " + time

        res_row = tmp[3]
        return date, res_row
    return None, row


def get_radiusd(row: str):
    end = row.find(":")
    return row[: end], row[end + 2:]


def get_pid(row: str):
    start = row.find("[") + 1
    end = row.find("]")
    return row[start: end], row[end + 2:]


def get_message_type(row: str):
    end = row.find(":")
    if end == 0:
        return None, row
    return row[: end], row[end + 2:]


def get_user(row: str):
    '''
    start = row.find("'") + 1
    end = row.find("'", start + 1)
    if start == end or start == end + 1:
        return None, row
    if "@" in row[start: end]:
        return row[start: end], row[end + 1:]
    return None, row
    '''
    user = re.search(r"[^ ]+@[^ ]+", row)
    if user is None:
        return None, row
    user = user.group(0)
    user = user.strip("'")
    return user, row
    raise Exception("OK not in row and FAILED not in row")


def get_result_status(row: str):
    state = [
        "FAILED",
        "OK"
        ]
    for elem in state:
        if elem in row:
            return elem
    return None
    raise Exception("OK not in row and FAILED not in row")


def get_operation_state(row: str):
    state = [
        "Alive",
        "Stop",
        "Start"
        ]
    for elem in state:
        if elem in row:
            return elem
    return None
    raise Exception("Alive and Stop and Start not in row")


def get_ULSK(row: str):
    res = re.findall(r"ULSK-\w+,", row)
    ULSK1 = None
    ULSK2 = None
    ULSK3 = None
    for i in range(len(res)):
        res[i] = res[i][5:-1]
    if len(res) >= 1:
        ULSK1 = res[0]
    if len(res) >= 2:
        ULSK2 = res[1]
    if len(res) >= 3:
        ULSK3 = res[2]
    return ULSK1, ULSK2, ULSK3


def get_RADIUS(row: str):
    res = re.search(r'RADIUS,\d?,', row)
    if res is None:
        return None
    return res.group(0)[7:-1]


def get_session_id(row: str):
    res = re.split(r'RADIUS,\d?,[^,]+,[^,]+,[^,]+,', row)
    if len(res) > 1:
        res = res[1][:res[1].find(',')]
        return res
    return None


def get_incoming(row: str):
    res = re.split(r'RADIUS,\d?,[^,]+,[^,]+,[^,]+,[^,]+,', row)
    if len(res) > 1:
        res = res[1][:res[1].find(',')]
        return res
    return None


def get_outcoming(row: str):
    res = re.split(r'RADIUS,\d?,[^,]+,[^,]+,[^,]+,[^,]+,[^,]+,', row)
    if len(res) > 1:
        res = res[1][:res[1].find(',')]
        return res
    return None


def get_ip(row: str):
    res = re.split(r'RADIUS,\d?,[^,]+,', row)
    if len(res) > 1:
        res = res[1][:res[1].find(',')]
        return res
    return None


def get_BRAS(row: str):
    res = re.split(r'RADIUS,\d?,[^,]+,[^,]+,[^,]+,', row)
    if len(res) > 1:
        res = res[1][:res[1].find(',')]
        return res
    return None


def get_mac(row: str):
    res = re.findall(r',[^,]+\)', row)
    if res is None or len(res) == 0:
        return None
    res = res[-1][2:-1].strip()
    return res


def get_traffic_direction(row: str):
    res = re.split(r'RADIUS,\d?,[^,]+,[^,]+,', row)
    if len(res) > 1:
        res = res[1][:res[1].find(')')]
        end = res.find(',')
        if end >= 0:
            res = res[:end]
        return res
    return None


def get_delay(row: str):
    res = re.search(r'delay \d+.\d+', row)
    if res is None:
        return None
    return res.group(0)[6:]


def get_skiped(row: str):
    text = 'Skiped due to traffic limit'
    if text in row:
        return 'Skiped'
    return None


def get_error_code(row: str):
    res = re.search(r'-- code [^,]+', row)
    if res == None:
        res = re.search(r'-- code -\d+', row)
    if res is None:
        return None
    return res.group(0)[8:].strip()


def get_data(row: str):
    start = row.find("(") + 1
    end = row.find(")")
    return row[start: end]
