#!/usr/bin/python3

import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("attempts", help="Number of Recipes to Try", type=int)
args = parser.parse_args()

scores = [3, 7]
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

while len(scores) <= args.attempts + 10:
    # printscores()
    totalscore = scores[elfindices[0]] + scores[elfindices[1]]
    firstdigit = totalscore // 10
    seconddigit = totalscore % 10
    if ( firstdigit > 0 ):
        scores.append( firstdigit )
    scores.append( seconddigit ) 
    elfindices[0] += 1 + scores[elfindices[0]]
    elfindices[1] += 1 + scores[elfindices[1]]
    elfindices[0] %= len(scores)
    elfindices[1] %= len(scores)

# printscores()

# Now take the scores of the last 10 recipes and munge them
nextten = ''.join( str(x) for x in scores[-11:-1] )
print( nextten )
