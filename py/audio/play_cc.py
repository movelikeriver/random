import csv
import sys
import time


print(sys.argv)
csv_fn = sys.argv[1]

if len(sys.argv) == 3:
    start_to = float(sys.argv[2])
else:
    start_to = 0

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
        if start >= start_to:
            time.sleep(start - prev)

        print(line[1])
        prev = start
