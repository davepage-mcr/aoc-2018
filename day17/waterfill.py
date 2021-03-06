#!/usr/bin/python3

import argparse
import pprint
import re
from colorama import Fore, Style

pp = pprint.PrettyPrinter()

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("filename", help="program input")
args = parser.parse_args()

source = set()
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
    print_some_scan(0, max_y)

def print_some_scan( start_y, end_y ):
    # print("From", min_x - 1, "to", max_x + 2)
    for y in range (start_y, end_y + 1):
        print(y, end="\t")
        for x in range (min_x, max_x + 1):
            coords = (x, y)
            if coords in source:
                print(Fore.GREEN + '+', end='')
            elif coords in water_rest:
                print(Fore.BLUE + '~', end='')
            elif coords in water_fall:
                print(Fore.YELLOW + '|', end="")
            elif coords in clay:
                print(Fore.RED + '#', end="")
            elif coords[0] == 500:
                print(Fore.GREEN + '.', end="")
            elif coords[0] % 50 == 0:
                print(Fore.YELLOW + '.', end="")
            else:
                print(Style.RESET_ALL + '.', end="")
        print(Style.RESET_ALL)

def below(coords):
    return tuple([ coords[0], coords[1]+1])

def left(coords):
    return tuple([ coords[0]-1, coords[1]])

def right(coords):
    return tuple([ coords[0]+1, coords[1]])

def pour(coords, recursion_depth):
    print("New pour from", coords, "at depth", recursion_depth)
    if tuple(coords) in source:
        print("We've already poured from here!")
        return
    source.add(tuple(coords))
    if coords[1] > 1670 and coords[1] < 1750:
        verbose = True
        print_some_scan(coords[1]-20, coords[1]+20)
    else:
        verbose=False

    while coords[1] <= max_y:
        # Have we hit something?
        if below(coords) in clay or below(coords) in water_rest:
            if(verbose):
                print("We've hit water or clay below", coords)
            # Set defaults for clean_left and clean_right here - if a wall is right against the edge, the for loops below might not run once and these will be descoped
            clean_left = True
            clean_right = True

            for l in range(coords[0], min_x, -1 ):
                # Look left until we either hit something or there's nothing below us
                look_coords = [ l, coords[1] ]
                below_us = below( look_coords )
                if not below_us in clay and not below_us in water_rest:
                    if(verbose):
                        print("\tThere is space below us to the left at", look_coords )
                    clean_left = False
                    break

                left_us = left( look_coords )
                if left_us in clay:
                    if(verbose):
                        print("\tThere is clay left of us at", look_coords )
                    break

            for r in range(coords[0], max_x ):
                # Look right until we either hit something or there's nothing below us
                look_coords = [ r, coords[1] ]
                below_us = below( look_coords )
                if not below_us in clay and not below_us in water_rest:
                    if(verbose):
                        print("\tThere is space below us to the right at", look_coords )
                    clean_right = False
                    break

                right_us = right( look_coords )
                if right_us in clay:
                    if(verbose):
                        print("\tThere is clay right of us at", look_coords )
                    break

            if clean_left and clean_right:
                for i in range(l, r+1):
                    fill_coords = tuple([ i, coords[1] ])
                    water_rest.add(fill_coords)
                if(verbose):
                    print("\tClean filled from", [l, coords[1]], "to", [r, coords[1]])
                coords[1] -= 1
                if(verbose):
                    print("\tMoving one up and looking at", coords)
                continue
            else:
                for i in range(l, r+1):
                    fill_coords = tuple([ i, coords[1] ])
                    water_fall.add(fill_coords)
                if(verbose):
                    print("\tFall-filled from", [l, coords[1]], "to", [r, coords[1]])
                if not clean_left:
                    pour([l, coords[1]], recursion_depth+1)
                if not clean_right:
                    pour([r, coords[1]], recursion_depth+1)
            break
        else:
            water_fall.add( tuple(coords) )

        coords[1] += 1

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
pour( [500,1], 0 )

# Sanity check: Make sure no intersection between waters and clay
all_water = water_rest.union(water_fall)

print(len(all_water), "water squares")
