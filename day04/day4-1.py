#!/usr/bin/python3

import sys
import re
import pprint
from datetime import datetime, timedelta

guard_sleep_minutes = {}
guard_asleep_this_minute = {}

pp = pprint.PrettyPrinter()

# Read the input from the file name specified on the command line
inputfile = open(sys.argv[1])

guard_id = None
for line in inputfile:      # We pre-sorted the input because this is boring finite state machine
    # [1518-11-01 00:00] Guard #10 begins shift
    # [1518-11-01 00:05] falls asleep
    # [1518-11-01 00:25] wakes up

    #
    # Grab timestamp
    #

    parse = re.match(r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\]', line)
    if not parse:
        print("Line does not match RE:", line.strip())
        continue
    timestamp = datetime.strptime(parse.group(1), "%Y-%m-%d %H:%M")

    # Deal with early starting guards, suspect Part 2 will break this
    if timestamp.hour > 12:
        timestamp += timedelta(days=1)
        timestamp = timestamp.replace( hour=0, minute=0)

    #
    # Check for change of guard ID
    #

    parse = re.search(r'Guard #(\d+) begins shift', line)
    if parse:
        guard_id = int(parse.group(1))
        fellasleep_at = None

        # Is this a new guard we need to start tracking?
        if not guard_id in guard_sleep_minutes:
            guard_sleep_minutes[guard_id] = 0
        continue

    if guard_id == None:
        print("We should have a guard_id by now but we don't!")
        sys.exit(1)

    #
    # Check for falling asleep / waking up
    #

    parse = re.search(r'falls asleep', line)
    if parse:
        fellasleep_at = timestamp
        if not guard_id in guard_asleep_this_minute:
            guard_asleep_this_minute[guard_id] = {}
        continue
    
    parse = re.search(r'wakes up', line)
    if not parse:
        print("I have no idea what this is:", line.strip())
        sys.exit(1)

    if fellasleep_at == None:
        print("Guard", guard_id, "has woken up without falling asleep")
        sys.exit(1)

    # This gets us the first part - which guard is sleepiest

    time_asleep = timestamp - fellasleep_at
    minutes_asleep = int ( time_asleep.seconds / 60 )
    # print("Guard", guard_id, "was asleep for ", minutes_asleep, "minutes from", fellasleep_at, "to", timestamp)
    guard_sleep_minutes[guard_id] += minutes_asleep

    # This gets us the second part - which minute was the sleepiest guard most often asleep at?
    # Don't assume this is all within the midnight hour
    fellasleep_at_minute = fellasleep_at.hour * 60 + fellasleep_at.minute
    for minute in range( fellasleep_at_minute, fellasleep_at_minute + minutes_asleep ):
        if not minute in guard_asleep_this_minute[guard_id]:
            guard_asleep_this_minute[guard_id][minute] = 0
        guard_asleep_this_minute[guard_id][minute] += 1 

# Create a hypothetical high-id ultra-sleepy guard for testing purposes
guards_by_sleepiness = sorted(guard_sleep_minutes, key=lambda guard_id: guard_sleep_minutes[guard_id])
sleepiest_guard = guards_by_sleepiness[-1]

minutes_by_sleeping = sorted(guard_asleep_this_minute[sleepiest_guard], key=lambda minute: guard_asleep_this_minute[sleepiest_guard][minute])
sleepiest_minute = minutes_by_sleeping[-1]

print("Sleepiest minute for guard", sleepiest_guard, sleepiest_minute)

print("Answer:", sleepiest_guard * sleepiest_minute)
