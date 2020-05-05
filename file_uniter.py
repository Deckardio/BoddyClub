import csv


DIGIT_TEMPLATE = "res_{0}_digit.csv"
ORIGIN_TEMPLATE = "res_{0}.csv"

DIGIT_COMMON = "res_all_digit.csv"
ORIGIN_COMMON = "res_all.csv"

with open("Results/digit/" + DIGIT_COMMON, 'w', encoding='ISO-8859-1', newline='') as ww:
    writer = csv.writer(ww)
    is_header = True
    for i in range(1,10):
        with open("Results/digit/" + DIGIT_TEMPLATE.format(i), 'r', encoding='ISO-8859-1') as ff:
            reader = csv.reader(ff)
            for index, line in enumerate(reader):
                if (is_header is True or index != 0) and '' not in line:
                    writer.writerow(line)
                    is_header = False
        print(DIGIT_TEMPLATE.format(i) + " was readed")
print("DIGIT_COMMON was created")

with open("Results/origin/" + ORIGIN_COMMON, 'w', encoding='ISO-8859-1', newline='') as ww:
    writer = csv.writer(ww)
    is_header = True
    for i in range(1,10):
        with open("Results/origin/" + ORIGIN_TEMPLATE.format(i), 'r', encoding='ISO-8859-1') as ff:
            reader = csv.reader(ff)
            for index, line in enumerate(reader):
                if (is_header is True or index != 0) and '' not in line:
                    writer.writerow(line)
                    is_header = False
        print(ORIGIN_TEMPLATE.format(i) + " was readed")
print("ORIGIN_COMMON was created")