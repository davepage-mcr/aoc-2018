#!/usr/bin/python3

import argparse
from blist import blist
import sys

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("target", help="Target Scores to Find", type=str)       # Need a str as may have a prefixed 0
args = parser.parse_args()
targetlength = len(args.target)

scores = blist([3, 7])

elfindices = [0, 1]
elfmarkers = [ '()', '[]' ]

def printscores():
    for s in range( len(scores) ):
        startmark   = ' '
        endmark     = ' '
        for e in range(len(elfindices)):
            if s == elfindices[e]:
                startmark   = elfmarkers[e][0]
                endmark     = elfmarkers[e][1]
        print(startmark + str(scores[s]) + endmark, end='')
    print()

for i in range(25000000):
    totalscore = scores[elfindices[0]] + scores[elfindices[1]]
    firstdigit = totalscore // 10
    seconddigit = totalscore % 10
    if ( firstdigit > 0 ):
        # Look for our scores to find at the end of this array
        scores.append( firstdigit )
        lastfew = ''.join( str(s) for s in scores[-(targetlength):] )
        if lastfew == args.target:
            break

    # Look for our scores to find at the end of this array
    scores.append( seconddigit )
    lastfew = ''.join( str(s) for s in scores[-(targetlength):] )
    if lastfew == args.target:
        break

    elfindices[0] += 1 + scores[elfindices[0]]
    elfindices[0] %= len(scores)
    elfindices[1] += 1 + scores[elfindices[1]]
    elfindices[1] %= len(scores)

else:
    print("Ran out of tries")
    sys.exit(1)

print("Found", args.target, "after", len(scores) - targetlength, "recipes")
