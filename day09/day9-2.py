#!/usr/bin/python3

import sys
import argparse
import string
import pprint
import re
from array import array

pp = pprint.PrettyPrinter()

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("input", help="Input file")
args = parser.parse_args()

def pretty_marbles():
    output = []
    for i in range(len(marbles)):
        if i == current_marble_index:
            output.append( '({0:2d})'.format(marbles[i]) )
        else:
            output.append( ' {0:2d} '.format(marbles[i]) )
    return ''.join(output)

inputfile = open(args.input)
for line in inputfile:
    # 10 players; last marble is worth 1618 points
    parse = re.match(r'(\d+) players; last marble is worth (\d+) points', line)
    if not parse:
        print("Line does not match RE:", line.strip())
        continue

    num_players = int(parse.group(1))
    num_marbles = int(parse.group(2))

    # UnsignedLong should be OK for up to 4294967295 marbles
    marbles = array('L')
    marbles.append(0)

    next_marble_id = 1
    current_marble_index = 0

    scores = {}
    for player in range(1, num_players + 1):
        scores[player] = 0

    player = 0
    for next_marble_id in range(1, num_marbles + 1):
        if next_marble_id % 10000 == 0:
            print("Playing marble", next_marble_id, "of", num_marbles)

        player = player % num_players + 1

        if next_marble_id % 23 == 0:
            # the current player keeps the marble they would have placed, adding it to their score
            scores[player] += next_marble_id

            # the marble 7 marbles counter-clockwise from the current marble is
            # removed from the circle and also added to the current player's score.
            remove_marble_index = ( current_marble_index - 7 ) % len(marbles)
            remove_marble_value = marbles[remove_marble_index]
            scores[player] += remove_marble_value
            marbles.pop( remove_marble_index )

            # The marble located immediately clockwise of the marble that was
            # removed becomes the new current marble
            current_marble_index = remove_marble_index

            # print("Elf {0} takes marble {1:2d} fm index {2}".format( player, remove_marble_value, current_marble_index))
        else:
            # place the lowest-numbered remaining marble into the circle between
            # the marbles that are 1 and 2 marbles clockwise of the current marble.
            next_marble_index = ( current_marble_index + 1 ) % len(marbles) + 1
            marbles.insert( next_marble_index, next_marble_id )

            # print("Elf {0} added marble {1:2d} at index {2}".format( player, next_marble_id, current_marble_index))

            # The marble that was just placed then becomes the current marble.
            current_marble_index = next_marble_index

    top_players = sorted( scores, key=lambda player: scores[player] )
    top_score = scores[top_players[-1]]

    print(num_players, top_score)
