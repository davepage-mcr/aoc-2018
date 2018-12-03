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
        fabric[x].append([])

multiclaims = 0

# Read the input from the file name specified on the command line
inputfile = open(sys.argv[1])
inputdata = []
for line in inputfile:
    # #1 @ 1,3: 4x4
    parse = re.match(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)', line)
    if not parse:
        print("Line does not match RE:", line.strip())
        next
    else:
        inputdata.append( [ int(parse.group(1)),
                            [ int(x) for x in parse.group(2,3) ],
                            [ int(x) for x in parse.group(4,5) ] ] )

for datum in inputdata:
    claim_id =  datum[0]
    starts =    datum[1]
    size =      datum[2]
    for x in range(starts[0], starts[0]+size[0]):
        for y in range(starts[1], starts[1]+size[1]):
            if len(fabric[x][y]) == 0:
                pass
            elif len(fabric[x][y]) == 1:
                multiclaims += 1
            fabric[x][y].append(claim_id)

print(multiclaims, "square inches contested by multiple claims")

# Now go back over input data and check where there's only one claim_id in all the squares

nooverlaps = []
for datum in inputdata:
    claim_id =  datum[0]
    starts =    datum[1]
    size =      datum[2]
    overlaps = False
    for x in range(starts[0], starts[0]+size[0]):
        for y in range(starts[1], starts[1]+size[1]):
            if len(fabric[x][y]) != 1:
                overlaps = True
                # We should be able to jump out of this double-nested loop
    
    if not overlaps:
        nooverlaps.append(claim_id)

print("No overlaps in claims", nooverlaps)
