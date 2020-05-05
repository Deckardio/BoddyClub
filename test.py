import csv
from collections import Counter

D_SOURCE = "Data/res_all_digit.csv"
D_DEST = "Results/res_all_digit.csv"
SOURCE = "Data/res_all.csv"
DEST = "Results/res_all.csv"

def find_max():
    res = Counter()
    count = 0
    with open(SOURCE, 'r', encoding='ISO-8859-1') as rr:
        reader = csv.reader(rr)
        for line in reader:
            res[line[3]] += 1
            count += 1
            if count % 100000 == 0:
                print(count)

    count = 0
    with open("test.tmp", 'w', encoding='ISO-8859-1', newline='') as ww:
        writer = csv.writer(ww)
        for key, line in res.items():
            writer.writerow([key, line])
            count += 1
            if count % 100000 == 0:
                print(count)

    return sorted(res, key=lambda x: res[x])[-10:]


def get_max_users(users: list):
    count = 0
    res = dict()
    print('reading...')
    is_headers = True
    headers = []
    with open(SOURCE, 'r', encoding='ISO-8859-1') as rr:
        reader = csv.reader(rr)
        for line in reader:
            if is_headers is True:
                headers = line
                is_headers = False
            else:
                user_name = line[3]
                if user_name in users:
                    if res.get(user_name) is  None:
                        res[user_name] = [line]
                    else:
                        res[user_name].append(line)
            count += 1
            if count % 100000 == 0:
                print(count)
    print("saving...")
    count = 0
    print(res.keys())
    for user, data in res.items():
        with open("Results/max_users/" + user, 'w', encoding='ISO-8859-1', newline='') as ww:
            writer = csv.writer(ww)
            writer.writerow(headers)
            for line in data:
                writer.writerow(line)
        count += 1
        if count % 100000 == 0:
            print(count)

# max_users = find_max()
# print(max_users)
# get_max_users(max_users)
'''

count = 0

with open(DEST, 'w', encoding='ISO-8859-1', newline='') as ww:
    writer = csv.writer(ww)
    with open(SOURCE, 'r', encoding='ISO-8859-1') as rr:
        reader = csv.reader(rr)
        for line in reader:
            if '' not in line:
                writer.writerow(line)
            count += 1
            if count % 100000 == 0:
                print(count)

'''
'''
count = 0
for i in range(1,10):
    with open("Data/radius.log.{0}".format(i), 'r', encoding='ISO-8859-1') as rr:
        for line in rr:
            print(line)
            break
'''