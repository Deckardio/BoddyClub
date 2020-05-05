import sys
import os
import time
import datetime


import support_func as sup


MAX_SESSION_INTERVAL = 100
MAX_ROW_PER_LOG = 3000000

class State:
    Alive = "Alive"
    Stop = "Stop"
    Start = "Start"


class Direction:
    Base = ''
    One = '1'
    Two = '2'
    Three = '3'
    Four = '4'
    Five = '5'
    Six = '6'


class Error:
    def __init__(self, login=None, ULSK=None, code=None, date=None):
        self.login = login
        self.ULSK = ULSK
        self.code = code
        self.date = date


class Flow:
    def __init__(self, login=None, ULSK=None, code=None, state=None, incoming=None, outcoming=None, delay=None, date=None, direction=None, bras_ip=None):
        self.login = login
        self.ULSK = ULSK
        self.state = state
        self.incoming = incoming
        self.outcoming = outcoming
        self.delay = delay
        self.date = date
        self.direction = direction
        self.bras_ip = bras_ip


class UserInfo:
    def __init__(self, login=None, ULSK=None, code=None, date=None):
        self.login = login
        self.flows = []
        self.zero_error_count = 0


def check_line(line: str):
    date, line = sup.get_flow_date(line)
    radiusd = None
    pid = None
    message_type = None
    user = None
    status = None
    state = None
    ULSK1 = None
    ULSK2 = None
    ULSK3 = None
    radius = None
    incoming = None
    outcoming = None
    traf_direction = None
    session_id = None
    ip = None
    mac = None
    delay = None
    bras_ip = None
    is_error = None
    if line is not None:
        radiusd, line = sup.get_radiusd(line)
    if line is not None:
        pid, line = sup.get_pid(line)
    if line is not None:
        message_type, line = sup.get_message_type(line)
    if line is not None:
        user, line = sup.get_user(line)
    if line is not None:
        is_error = sup.get_error_code(line)
        if (is_error == '1011' or 
            is_error == '-52' or 
            is_error == '-42' or 
            is_error == '-21' or 
            is_error == '-52' or 
            is_error == '-44' or 
            is_error == '-40' or 
            is_error == '-38' or 
            is_error == '-46'):
            ULSK1, ULSK2, ULSK3 = sup.get_ULSK(line)
        if is_error is None:
            status = sup.get_result_status(line)
            state = sup.get_operation_state(line)
            ULSK1, ULSK2, ULSK3 = sup.get_ULSK(line)
            radius = sup.get_RADIUS(line)

            if state == State.Alive or state == State.Stop:
                incoming = sup.get_incoming(line)
                outcoming = sup.get_outcoming(line)

            if state == State.Start or state == State.Alive or state == State.Stop:
                ip = sup.get_ip(line)
                traf_direction = sup.get_traffic_direction(line)
                session_id = sup.get_session_id(line)
            if (state == State.Start and radius == '') or state == State.Alive or state == State.Stop:
                mac = sup.get_mac(line)
            if state == State.Start and radius == '':
                bras_ip = sup.get_BRAS(line)

            delay = sup.get_delay(line)
            return Flow(
                login=user,
                ULSK=ULSK1,
                date=int(time.mktime(time.strptime("20 " + date, "%y %b %d %H:%M:%S"))),
                incoming=incoming,
                outcoming=outcoming,
                state=state,
                delay=delay,
                direction=radius,
                bras_ip=bras_ip
                )
        else:
            return Error(
                login=user,
                ULSK=ULSK1,
                code=is_error,
                date=int(time.mktime(time.strptime("20 " + date, "%y %b %d %H:%M:%S")))
                )
        return None


def flows_cleaner(flows: dict, last_time: int):
    # cur_time = int(time.time())
    # print(last_time)
    removed_key = []
    for key in flows:
        for i in range(len(flows[key])):
            if flows[key][i][1] < last_time - MAX_SESSION_INTERVAL:
                del flows[key][i]
                if len(flows[key]) == 0:
                    removed_key.append(key)
                    # del flows[key]
    for elem in removed_key:
        del flows[elem]


def check_small_session(data, flows: dict):
    # print([data.state, data.direction])
    if data.state == State.Start and data.direction == Direction.Base:
        # print([data.login, data.date, data.state, data.direction])
        if flows.get(data.login) is None:
            flows[data.login] = [[data.ULSK, data.date]]
        else:
            flows[data.login].append([data.ULSK, data.date])
        print("Количество текущих сессий: {0}".format(len(flows)))
    if data.state == State.Stop and data.direction == Direction.Base:
        if flows.get(data.login) is not None:
            for index, session_info in enumerate(flows[data.login]):
                    if data.ULSK == session_info[0]:
                        del flows[data.login][index]
                        if len(flows[data.login]) == 0:
                            del flows[data.login]
                        print("Количество текущих сессий: {0}".format(len(flows)))
                        if data.date <= session_info[1] + 100:
                            return data.date - session_info[1]
                            
    return None


error_desc = {
    "0": "Skiped due to traffic limit",
    "1011": "Password match failure",
    "1100": "FAILED No username found",
    "-3": "FAILED Service isn?t ON.",
    "-52": "FAILED Service isn?t ON.",
    "-42": "FAILED Tarification error.<SQL>ORA-20001",
    "-21": "FAILED Not enough money on account",
    "-40": "FAILED STOP on NORMAL closed session",
    "-44": "FAILED ALIVE on NORMAL closed session",
    "-46": "FAILED Session in work",
    "-38": "FAILED Doubling session in TB_WTMPS"
}


def get_new_filename():
    file_template = "radius.log.{0}"
    return file_template.format(int(time.time()))


if __name__ == "__main__":
    if os.path.isdir("logs") is False:
        os.mkdir("logs")
    flows = {}
    i = 0
    line = ''
    sys.stdin.reconfigure(encoding='ISO-8859-1')
    file_number = 0
    ww = open('logs/' + get_new_filename(), 'w', encoding='ISO-8859-1')
    while True:
        line = sys.stdin.readline()
        if line != '' and line != '\n':
            i += 1
            data = check_line(line)
            ww.write(line)
            if i > MAX_ROW_PER_LOG:
                ww.close()
                ww = open('logs/' + get_new_filename(), 'w', encoding='ISO-8859-1')
                i = 0
            line = ''

            if isinstance(data, Error):
                date = datetime.datetime.utcfromtimestamp(data.date).strftime('%Y-%m-%d %H:%M:%S')
                code_desc = data.code
                if data.code in error_desc:
                    code_desc = error_desc[data.code] + "({0})".format(data.code)
                print("{0}: {1} - {2}".format(date, data.login, code_desc))
            elif isinstance(data, Flow):
                is_small = check_small_session(data, flows)
                if is_small is not None:
                    print("{3}: Обнаружена короткая сессия у пользователя({2} секунд): {0} - {1}".format(data.login, data.ULSK,  is_small, data.date))
                if i % 100 == 0:
                    flows_cleaner(flows, data.date)
                    # i = 0
    ww.close()