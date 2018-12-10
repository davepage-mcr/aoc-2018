#!/usr/bin/python3

import sys
import re
import pprint
import argparse

guard_asleep_this_minute = {}

pp = pprint.PrettyPrinter()

class Point:
    def __init__( self, position, velocity ):
        self.position = position
        self.velocity = velocity

    def tick(self, backwards=False):
        if backwards:
            self.position[0] -= self.velocity[0]
            self.position[1] -= self.velocity[1]
        else:
            self.position[0] += self.velocity[0]
            self.position[1] += self.velocity[1]

class PointField:
    def _blanklimits(self):
        self.min_x  = None
        self.min_y  = None
        self.max_x  = None
        self.max_y  = None
    
    def __init__(self):
        self.points = set()
        self._blanklimits()

    def _checklimits(self, point):
        if self.min_x == None or self.min_x > point.position[0]:
            self.min_x = point.position[0]
        if self.min_y == None or self.min_y > point.position[1]:
            self.min_y = point.position[1]
        if self.max_x == None or self.max_x < point.position[0]:
            self.max_x = point.position[0]
        if self.max_y == None or self.max_y < point.position[1]:
            self.max_y = point.position[1]

    def add(self, point):
        self.points.add(point)
        self._checklimits(point)

    def _ispoint(self, coords):
        for point in self.points:
            if point.position[0] == coords[0] and point.position[1] == coords[1]:
                return True
        return False

    def print(self):
        for y in range(self.min_y, self.max_y+1):
            print(y, "\t", end='')
            for x in range(self.min_x, self.max_x+1):
                # Is this a point?
                if self._ispoint( (x,y) ):
                    print('#', end='')
                else:
                    print('.', end='')
            print()
        print("\t", end='')
        for x in range(self.min_x, self.max_x+1):
            if x == 0:
                print(x, end='')
            else:
                print(' ', end='')
        print()

    def tick(self, backwards=False):
        area = ( self.max_x - self.min_x ) * ( self.max_y - self.min_y )
        self._blanklimits()
        for point in self.points:
            point.tick(backwards)
            self._checklimits(point)
        newarea = ( self.max_x - self.min_x ) * ( self.max_y - self.min_y )
        return newarea > area

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("input", help="Input file")
args = parser.parse_args()

inputfile = open(args.input)

field = PointField()

for line in inputfile:
    parse = re.match(r'position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>', line)
    if not parse:
        print("Line does not match RE:", line.strip())
        continue

    field.add( Point( [ int(parse.group(1)), int(parse.group(2)) ], [ int(parse.group(3)), int(parse.group(4)) ] ) )

expanding = False
clock = 0
while not expanding:
    expanding = field.tick()
    clock += 1
    if expanding:
        print("After", clock, "second(s), grid expanding - narrowest formation at", clock - 1)
        field.tick(True)
        field.print()
