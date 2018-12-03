#!/usr/bin/python3

import sys
import pprint
import re

# Create 1000x1000 array full of empty sets
# The sets will contain the claim IDs which cover this square

fabricsize = 1000
fabric = []

for x in range(fabricsize+1):
    fabric.append([])
    for y in range(fabricsize+1):
        fabric[x].append( set() )

multiclaims = 0
nooverlaps = set()

# Read the input from the file name specified on the command line
inputfile = open(sys.argv[1])

for line in inputfile:
    # #1 @ 1,3: 4x4
    parse = re.match(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)', line)
    if not parse:
        print("Line does not match RE:", line.strip())
        next

    claim_id    = int(parse.group(1))
    starts      = [ int(x) for x in parse.group(2,3) ]
    size        = [ int(x) for x in parse.group(4,5) ]

    nooverlap   = True
    for x in range(starts[0], starts[0]+size[0]):
        for y in range(starts[1], starts[1]+size[1]):
            if len(fabric[x][y]) == 0:
                # print("\t", x,y, "not already covered")
                pass
            elif len(fabric[x][y]) == 1:
                # print("\t", x,y, "covering for first time")
                nooverlap = False
                multiclaims += 1
            else:
                # print("\t", x,y, "already covered")
                nooverlap = False

            if len(fabric[x][y]) > 0:
                # This has been claimed already, so remove the claim IDs
                # from the set of non-overlapping IDs
                for existing_id in fabric[x][y]:
                    nooverlaps.discard(existing_id)

            fabric[x][y].add(claim_id)

    if nooverlap:
        nooverlaps.add( claim_id )

print(multiclaims, "square inches contested by multiple claims")
print("No overlaps in claims", nooverlaps)
