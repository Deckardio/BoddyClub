"""
Создание числового идентификатора для логина пользователя.
"""
import csv


USER_LOGIN_FILENAME = "Results/digit/digit_login"


def load_user_login():
    with open(USER_LOGIN_FILENAME, 'r', encoding='ISO-8859-1') as ff:
        file_reader = csv.reader(ff)
        res = {}
        for line in file_reader:
            tmp = line
            res[tmp[0]] = tmp[1]
    return res


def save_user_login(data: {}, dest_filename: str):
    with open(dest_filename, 'w', encoding='ISO-8859-1', newline='') as ff:
        file_writer = csv.writer(ff)
        for name, digit in data.items():
            file_writer.writerow([name, digit])
        # print("data was saved!")


def read_file(source_filename: str, digit_login: dict):
    with open(source_filename, 'r', encoding='ISO-8859-1') as ff:
        file_reader = csv.reader(ff)
        is_header = True
        for line in file_reader:
            if is_header is False:
                user_login = line[3]
                if digit_login.get(user_login) is None:
                    digit_login[user_login] = len(digit_login)
            is_header = False
            
    return digit_login


def convert(source_filename: str, dest_filename: str, digit_login: dict):
    with open(dest_filename, 'w', encoding='ISO-8859-1', newline='') as dest_file:
        writer = csv.writer(dest_file)
        with open(source_filename, 'r', encoding='ISO-8859-1') as ff:
            file_reader = csv.reader(ff)
            is_header = True
            for line in file_reader:
                if is_header is False:
                    line[3] = digit_login[line[3]]
                is_header = False
                writer.writerow(line)
        return digit_login


def get_digit():
    # 
    digit_login = {}
    for i in range(1, 10):
        digit_login = read_file("Results/origin/res_" + str(i) + ".csv", digit_login)
    save_user_login(digit_login, USER_LOGIN_FILENAME)


def set_digit():
    digit_login = load_user_login()
    for i in range(1, 10):
        digit_login = convert("Results/origin/res_" + str(i) + ".csv", "Results/digit/res_" + str(i) + "_digit.csv", digit_login)


def start(filename: str, dest_filename: str, dict_filename: str):
    digit_login = {}
    digit_login = read_file(filename, digit_login)
    save_user_login(digit_login, dict_filename)
    digit_login = convert(filename, dest_filename, digit_login)


if __name__ == "__main__":
    get_digit()
    set_digit()
