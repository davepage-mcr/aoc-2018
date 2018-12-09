#!/usr/bin/python3

import sys
import re
import pprint
import string

# Read the input from the file name specified on the command line
inputfile = open(sys.argv[1])

def manhattan_distance(coords, target):
    return abs(coords[0] - target[0]) + abs(coords[1] - target[1])

def distance_to_all_targets(coords):
    distance = 0
    for target in all_targets:
        distance += manhattan_distance(coords, target)
    return distance

# Infinite areas come from co-ordinates which are (joint) top, bottom, left or
# right-most so spot these

max_x = None
max_y = None
min_x = None
min_y = None

# all_targets is a set (unsorted, no duplicates) of tuples (fixed length) of integers

all_targets = set()
for line in inputfile:
    coords = tuple( [ int(x) for x in line.split(', ') ] ) 

    if max_x == None or max_x < coords[0]:
        max_x = coords[0]
    if max_y == None or max_y < coords[1]:
        max_y = coords[1]

    if min_x == None or min_x > coords[0]:
        min_x = coords[0]
    if min_y == None or min_y > coords[1]:
        min_y = coords[1]

    all_targets.add( tuple( [ int(x) for x in line.split(', ') ] ) )

# Find all squares in the region less than the threshold

region_size = 0
for x in range(min_x - 1, max_x + 1):
    for y in range(min_y - 1, max_y + 1):
        coords = [ x, y ]
        total_distance = distance_to_all_targets(coords)

        if total_distance < 10000:
            region_size += 1

print(region_size)
