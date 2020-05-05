"""
Получает полезную информацию из логов radius'а
"""
import csv
import re
import time
import sys
import os


import click


import Graph_v0_4
import support_func as sup
import digit
import gui_kmeans
import pandas as pd


def show_precent(number: int):
    sys.stdout.write("\rReaded: %i" % number)
    sys.stdout.flush()


def parse_all_data(filename: str, count=None):
    if os.path.isdir("Results") is False:
        os.mkdir("Results")
    RES_PATH = "Results/res_flow_1.csv"
    print("start")
    counter = 0
    is_started = False
    with open(RES_PATH, "w", encoding='ISO-8859-1', newline='') as res_file:
        res_writer = csv.writer(res_file)
        res_writer.writerow([
            "Date",
            "Billing-Accounting",
            "Login",
            "OK/FAILED",
            "Alive/Stop/Start",
            "ULSK1",
            "RADIUS 0-6",
            "MAC ab",
            "traffic direction",
            "session id",
            "incoming",
            "outcoming",
            "ULSK2",
            "ULSK3",
            "delay"
        ])
        with open(filename, "r", encoding='ISO-8859-1') as ff:
            for line in ff:
                date, line = sup.get_date(line)
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
                if line is not None:
                    radiusd, line = sup.get_radiusd(line)
                if line is not None:
                    pid, line = sup.get_pid(line)
                if line is not None:
                    message_type, line = sup.get_message_type(line)
                if line is not None:
                    user, line = sup.get_user(line)
                if line is not None:
                    status = sup.get_result_status(line)
                    state = sup.get_operation_state(line)
                    ULSK1, ULSK2, ULSK3 = sup.get_ULSK(line)
                    radius = sup.get_RADIUS(line)
                    if state == "Alive" or state == "Stop":
                        incoming = sup.get_incoming(line)
                        outcoming = sup.get_outcoming(line)
                    
                    if state == "Start" or state == "Alive" or state == "Stop":
                        ip = sup.get_ip(line)
                        traf_direction = sup.get_traffic_direction(line)
                        session_id = sup.get_session_id(line)
                    if (state == "Start" and radius == '') or state == "Alive" or state == "Stop":
                        mac = sup.get_mac(line)

                    delay = sup.get_delay(line)
                res_writer.writerow([
                    date,
                    message_type,
                    user,
                    status,
                    state,
                    ULSK1,
                    radius,
                    mac,
                    traf_direction,
                    session_id,
                    incoming,
                    outcoming,
                    ULSK2,
                    ULSK3,
                    delay
                    ])
                counter += 1
                if count is not None:
                    if counter == count:
                        break
                if counter % 10000 == 0:
                    print(counter)
    print("end")


def init_flow_info():
    flow_info = [
        None,  # start
        None,  # stop
        None,  # interval
        None,  # login
        None,  # mac
        None,  # ulsk
        None,  # bras ip
        0,  # start count
        0,  # alive count
        0,  # stop count
        0,  # incoming
        0,  # outcoming
        0,  # error count
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0
    ]
    return flow_info


def get_all_flows(filename:str, result_filename: str, count=None):
    print("reading...")
    counter = 0
    flow_dict = {}
    with open(result_filename, "w", encoding='ISO-8859-1', newline='') as res_file:
        headers = [
            "begin",
            "end",
            "time interval",
            "login",
            "mac ab",
            "ULSK1",
            "BRAS ip",
            "start count",
            "alive count",
            "stop count",
            "incoming",
            "outcoming",
            "error_count",
            "code 0",
            "code 1011",
            "code 1100",
            "code -3",
            "code -52",
            "code -42",
            "code -21",
            "code -40",
            "code -44",
            "code -46",
            "code -38"
        ]
        error_codes = [
            '0',
            '1011',
            '1100',
            '-3',
            '-52',
            '-42',
            '-21',
            '-40',
            '-44',
            '-46',
            '-38'
        ]

        res_writer = csv.writer(res_file)
        res_writer.writerow(headers)
        with open(filename, "r", encoding='ISO-8859-1') as ff:
            for line in ff:
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

                        if state == "Alive" or state == "Stop":
                            incoming = sup.get_incoming(line)
                            outcoming = sup.get_outcoming(line)

                        if state == "Start" or state == "Alive" or state == "Stop":
                            ip = sup.get_ip(line)
                            traf_direction = sup.get_traffic_direction(line)
                            session_id = sup.get_session_id(line)
                        if (state == "Start" and radius == '') or state == "Alive" or state == "Stop":
                            mac = sup.get_mac(line)
                        if state == "Start" and radius == '':
                            bras_ip = sup.get_BRAS(line)

                        delay = sup.get_delay(line)
                if is_error is not None and ULSK1 is not None:
                    if flow_dict.get(ULSK1) is not None:
                        for index in range(len(error_codes)):
                            sample_code = error_codes[index]
                            if is_error == sample_code:
                                flow_dict[ULSK1][12] += 1
                                flow_dict[ULSK1][13 + index] += 1
                                break
                            
                if is_error is None and ULSK1 is not None:
                    if state == "Start":
                        if flow_dict.get(ULSK1) is None:
                            flow_dict[ULSK1] = init_flow_info()
                            flow_dict[ULSK1][0] = int(time.mktime(time.strptime("20 " + date, "%y %b %d %H:%M:%S")))
                            flow_dict[ULSK1][1] = int(time.mktime(time.strptime("20 " + date, "%y %b %d %H:%M:%S")))
                    if state == "Start" and radius == '':
                            flow_dict[ULSK1][1] = int(time.mktime(time.strptime("20 " + date, "%y %b %d %H:%M:%S")))
                            flow_dict[ULSK1][3] = user
                            flow_dict[ULSK1][4] = mac
                            flow_dict[ULSK1][5] = ULSK1
                            flow_dict[ULSK1][6] = bras_ip
                    else:
                        if flow_dict.get(ULSK1) is not None:
                            if state == "Start" or state == "Alive" or state == "Stop":
                                flow_dict[ULSK1][1] = int(time.mktime(time.strptime("20 " + date, "%y %b %d %H:%M:%S")))
                            if state == "Start" and radius != '':
                                flow_dict[ULSK1][7] += 1
                                if incoming is not None:
                                    flow_dict[ULSK1][10] += int(incoming)
                                if outcoming is not None:
                                    flow_dict[ULSK1][11] += int(outcoming)
                            elif state == "Alive" and radius != '':
                                flow_dict[ULSK1][8] += 1
                                if incoming is not None:
                                    flow_dict[ULSK1][10] += int(incoming)
                                if outcoming is not None:
                                    flow_dict[ULSK1][11] += int(outcoming)
                            elif state == "Stop" and radius != '':
                                flow_dict[ULSK1][9] += 1
                                if incoming is not None:
                                    flow_dict[ULSK1][10] += int(incoming)
                                if outcoming is not None:
                                    flow_dict[ULSK1][11] += int(outcoming)

                counter += 1
                if count is not None:
                    if counter == count:
                        break
                if counter % 50000 == 0:
                    show_precent(counter)  # print("----", counter)

            for key, value in flow_dict.items():
                date_start = value[0]
                date_stop = value[1]
                time_interval = date_stop - date_start
                value[2] = int(time_interval)

                res_writer.writerow(value)
    print()


def read_data(filename, searching_data, count=None):
    with open(filename, 'r',  encoding='ISO-8859-1') as ff:
        counter = 0
        for line in ff:
            if searching_data in line:
                print(line)
                counter += 1
                if count is not None:
                    if counter >= count:
                        break


def parse_all():
    print('start')
    filenames_list = [
        "Data/radius.log.1",
        "Data/radius.log.2",
        "Data/radius.log.3",
        "Data/radius.log.4",
        "Data/radius.log.5",
        "Data/radius.log.6",
        "Data/radius.log.7",
        "Data/radius.log.8",
        "Data/radius.log.9"
    ]
    for filename in filenames_list:
        print("start:", filename)
        get_all_flows(filename, "Results/res_" + filename.split(".")[-1] + ".csv")


def  corel(source_filename: str, dest_filename: str):
    data = pd.read_csv(source_filename)
    correl = data.corr(method ='pearson') 
    correl.to_csv(dest_filename, index=True)


@click.command()
@click.option('-l', "--log_file", "log_filename",  default=None, type=click.Path(exists=True, file_okay=True, dir_okay=False), help='path to radius log file')
@click.option('-c', "--clear_log_file", "clear_log_filename", default=None, type=click.Path(exists=True, file_okay=True, dir_okay=False), help='path to preprocessing log file')
def main(log_filename: str, clear_log_filename: str):
    if clear_log_filename is None and log_filename is None:
        return None
    if os.path.isdir("Results") is False:
        os.mkdir("Results")
    
    filename = None
    if clear_log_filename is not None:
        filename = os.path.basename(clear_log_filename)
    elif log_filename is not None:
        filename = os.path.basename(log_filename)
    else:
        return None

    digit_dest_filename = "Results/digit_preproc_{0}.csv".format(filename)
    dict_digit_filename = "Results/digit_preproc_{0}_dict.csv".format(filename)
    dest_filename = "Results/preproc_{0}.csv".format(filename)
    if clear_log_filename is None and log_filename is not None:
        get_all_flows(log_filename, dest_filename)
        print("log was readed successfully!")
        print("Preprocessing log was saved in file: {0}".format(dest_filename))
    elif clear_log_filename is not None:
        dest_filename = clear_log_filename
    print("Converting logins")
    digit.start(dest_filename, digit_dest_filename, dict_digit_filename)
    print("log was converted successfully!")

    while True:
        print("select action:")
        print("--create correlation file: 1")
        print("--calculate kmeans: 2")
        print("--show graph: 3")
        print("--exit: exit")
        command = input(">> ")
        if command == "1":
            print("creating correlation file...")
            corel_filename = "Results/corel_{0}".format(os.path.basename(dest_filename))
            corel(dest_filename, corel_filename)
            print("correlation wa saved in '{0}'".format(corel_filename))
        elif command == "2":
            print("launching kmeans gui...")
            gui_kmeans.start(digit_dest_filename)
            print("kmeans gui was closed!")
        elif command == "3":
            print("launching graph gui...")
            Graph_v0_4.start(dest_filename)
            print("graph gui was closed!")
        elif command == "exit":
            print("good bye")
            break


if __name__ == "__main__":
    # 1011 - p13ay4Zl@pppoe(ULSK-BR09232112900000bbb97e152271)  WgvLLW-W@pppoe(ULSK-BR062311133000003fe793159202)
    # -52 - XsAAXXWsH8@pppoe(ULSK-BR06231111200000c31f7a246101)  W9gg98-g@pppoe(ULSK-BR06231133900000675b34122891)
    # -42 -  0A49F614-0F@dhcp(ULSK-BR15233070400000541f0a047417)
    # '-21' - 9usLtat9-9s@dhcp(ULSK-BR15233040400000389163128271)
    # '-40',- 9usLtat9-9s@dhcp(ULSK-BR15233040400000389163128271)
    # '-44', - 9usLtat9-9s@dhcp(ULSK-BR15233040400000389163128271)
    # '-46', 
    # '-38'- 9usLtat9-9s@dhcp(ULSK-BR15233040400000389163128271)
    main()
    # read_data("Data/radius.log.1","NULN-HGPON-ATS-0-1-9@dhcp")
