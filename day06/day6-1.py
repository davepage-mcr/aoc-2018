#!/usr/bin/python3

import sys
import re
import pprint
import string

# Read the input from the file name specified on the command line
inputfile = open(sys.argv[1])

def manhattan_distance(coords, target):
    return abs(coords[0] - target[0]) + abs(coords[1] - target[1])

def closest_target(coords):
    # Return the closest target or None if 2+ are equidistant

    closest = []
    closest_distance = None
    for target in all_targets:
        distance = manhattan_distance(coords, target)
        # print("Distance between", coords, target, distance)
        if closest_distance == None or closest_distance > distance:
            closest = [ target ]
            closest_distance = distance
            # print("New closest target for", coords, target, "at distance", closest_distance)
        elif closest_distance == distance:
            closest.append( target )

    # print("Closest target(s) for", coords, "is", closest, len(closest))

    if len(closest) == 1:       # Clearly closest to only one target
        return closest[0]

    return None

def is_finite(target):
    if target[0] == min_x or target[0] == max_x or target[1] == min_y or target[1] == max_y:
        return False
    return True

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

# Now we go over the grid between these maxes and mins, and for each square
# work out the closest coordinate point

areas_by_target = {}
for x in range(min_x - 1, max_x + 1):
    for y in range(min_y - 1, max_y + 1):
        coords = [ x, y ]
        target = closest_target(coords)
        if target != None:
            if target not in areas_by_target:
                areas_by_target[target] = 1
            else:
                areas_by_target[target] += 1

# Now eliminate the infinite targets

for target in all_targets:
    if not is_finite(target):
        del areas_by_target[target]

print(areas_by_target)

# What's the finite target with the biggest area?
targets_by_area = sorted( areas_by_target, key=lambda target: areas_by_target[target] )
biggest_target = targets_by_area[-1]
print("Target with biggest area is", biggest_target, areas_by_target[biggest_target])
