#!/usr/bin/python3

import argparse
import pprint
import re

pp = pprint.PrettyPrinter()

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("filename", help="program input")
args = parser.parse_args()

source = { (500,0) }
clay = set()
water_rest = set()
water_fall = set()

inputfile = open(args.filename)

min_x = None
max_x = None
max_y = None
min_y = None

def check_max( current, new ):
    if current is None:
        return new
    return max(current,new)

def check_min( current, new ):
    if current is None:
        return new
    return min(current,new)

def print_scan():
    print(min_x, max_x)
    for y in range (0, max_y + 2 ):
        print(y, end="\t")
        for x in range (min_x - 1, max_x + 2 ):
            coords = (x, y)
            if coords in source:
                print('+', end="")
            elif coords in clay:
                print('#', end="")
            elif coords in water_rest:
                print('~', end="")
            elif coords in water_fall:
                print('|', end="")
            else:
                print('.', end="")
        print()

def below(coords):
    return tuple([ coords[0], coords[1]+1])

def left(coords):
    return tuple([ coords[0]-1, coords[1]])

def right(coords):
    return tuple([ coords[0]+1, coords[1]])

for line in inputfile:
    # Populate the "clay" set with tuples from the coordinate sets in this line
    regex = re.match(r'^([xy])=(\d+), ([xy])=(\d+)\.\.(\d+)$', line)
    if not regex:
        print("Failed to match regex:", line)
        exit(1)

    fixedcoord = regex.group(1)
    fixedcoordval = int(regex.group(2))
    variablecoord = regex.group(3)
    variablestart = int(regex.group(4))
    variableend = int(regex.group(5))

    for i in range(variablestart, variableend+1):
        if fixedcoord == 'x':
            min_x = check_min( min_x, fixedcoordval )
            max_x = check_max( max_x, fixedcoordval )
            min_y = check_min( min_y, i )
            max_y = check_max( max_y, i )
            coords = ( fixedcoordval, i )
        else:
            min_x = check_min( min_x, i )
            max_x = check_max( max_x, i )
            min_y = check_min( min_y, fixedcoordval )
            max_y = check_max( max_y, fixedcoordval )
            coords = ( i, fixedcoordval )

        clay.add(coords)

# Now we have populated the clay set, we start pouring water from (500,1) downwards

coords = [500,1]
while coords[1] <= max_y:
    # Have we hit something?
    if below(coords) in clay:
        print("We've hit clay at", coords)
        break

    water_fall.add( tuple(coords) )
    coords[1] += 1

print_scan()
