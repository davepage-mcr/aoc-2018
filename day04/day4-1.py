#!/usr/bin/python3

import sys
import re
from datetime import datetime

# Read the input from the file name specified on the command line
inputfile = open(sys.argv[1])

for line in inputfile:
    # [1518-11-01 00:00] Guard #10 begins shift
    # [1518-11-01 00:05] falls asleep
    # [1518-11-01 00:25] wakes up

    parse = re.match(r'^\[(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2})\]', line)
    if not parse:
        print("Line does not match RE:", line.strip())
        next
    data = [ int(x) for x in parse.group(1,2,3,4,5) ]
    print(data)
    timestamp = datetime(data) # TypeError: an integer is required (got type list)
