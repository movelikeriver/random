import csv
import sys
import time


print(sys.argv)
csv_fn = sys.argv[1]

with open(csv_fn) as fn:
    c = csv.reader(fn, delimiter=",")

    prev = -1

    for line in c:
        if prev == -1:
            # head
            print(line)
            prev = 0
            continue

        start = float(line[0])
        time.sleep(start - prev)
        print(line[1])
        prev = start
