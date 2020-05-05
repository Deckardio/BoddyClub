"""
Получает все ошибки и их время по пользователям.
В процессе написания.
"""

import support_func as sup
import time
import csv


import digit


def get_user_errors(filename: str, dest_filename: str, user_logins, count=None):
    print("start")
    flow_errors = {}
    with open(dest_filename, "w", encoding='ISO-8859-1', newline='') as res_file:
        dest_writer = csv.writer(res_file)
        with open(filename, "r", encoding='ISO-8859-1') as ff:
            counter = 0
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
                if is_error is not None and user is not None:
                    if flow_errors.get(user) is not None:
                        flow_errors[user].append([
                            int(time.mktime(time.strptime("20 " + date, "%y %b %d %H:%M:%S"))),
                            is_error
                        ])
                    else:
                        flow_errors[user] = [[
                            int(time.mktime(time.strptime("20 " + date, "%y %b %d %H:%M:%S"))),
                            is_error
                        ]]
                counter += 1
                if count is not None:
                    if counter == count:
                        break
                if counter % 100000 == 0:
                    print("----", counter)
                        
        print("saving in file:", dest_filename)
        for key, value in flow_errors.items():
            key = user_logins[key]
            for row in value:
                dest_writer.writerow([key] + row)
        print("end")


if __name__ == "__main__":
    raise Exception("doesn't implemented")

    user_logins = digit.load_user_login()
    for i in range(1, 10):
        user_logins = digit.read_file("radius.log." + str(i), user_logins)
    digit.save_user_login(user_logins)

    for i in range(1, 10):
        get_user_errors("radius.log." + str(i), "Results/digit/user_errors/user_errors_(digit)_" + str(i), user_logins)
