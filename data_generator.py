import sys
import time

orig = 'radius.log.1'
test = 'testdata_sh'
onesession = 'onesess'

sys.stdout.reconfigure(encoding='ISO-8859-1')
with open("Data/" + orig, 'r', encoding='ISO-8859-1') as rr:
    for line in rr:
        line = line + '\n'
        sys.stdout.write(line)
        # print(line)
        time.sleep(0.01)
