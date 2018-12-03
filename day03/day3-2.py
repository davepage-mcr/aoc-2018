#!/usr/bin/python3

import sys
import pprint
import re

# Create 1000x1000 array full of 0s

fabricsize = 1000
fabric = []

for x in range(fabricsize+1):
    fabric.append([])
    for y in range(fabricsize+1):
        fabric[x].append(0)

multiclaims = 0
nooverlaps = []

# Read the input from the file name specified on the command line
inputfile = open(sys.argv[1])
for line in inputfile:
    # #1 @ 1,3: 4x4
    parse = re.match(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)', line)
    if not parse:
        print("Line does not match RE:", line.strip())
        next
    else:
        claim_id =  int(parse.group(1))
        starts =    [ int(x) for x in parse.group(2,3) ]
        size =      [ int(x) for x in parse.group(4,5) ]

    overlaps = False
    for x in range(starts[0], starts[0]+size[0]):
        for y in range(starts[1], starts[1]+size[1]):
            if fabric[x][y] == 0:
                print(x,y, "previously unclaimed; covering")
            elif fabric[x][y] == 1:
                print(x,y, "previously claimed once; newly contested")
                multiclaims += 1
                overlaps = True
            else:
                print(x,y, "is already contested")
                overlaps = True
            fabric[x][y] += 1

    if not overlaps:
        nooverlaps.append(claim_id)

print(multiclaims, "square inches contested by multiple claims")
print("No overlaps in claims", nooverlaps)
