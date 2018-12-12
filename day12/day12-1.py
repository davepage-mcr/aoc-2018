#!/usr/bin/python3

import argparse
import re
import pprint

generations = 20

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("input", help="Input file")
args = parser.parse_args()

pp = pprint.PrettyPrinter()

plants = {}     # Use a dict so we can have -ve numbers as keys
rules  = {}     # Dict of matches (tuples) to True (new flower) or False (no flower)

def nextgen(position):
    # take the position key from the plants dict
    # Return true or false depending on whether there should be a plant in the pot next time

    # Build up a tuple of positions by prepending / appending False where needed
    positions = []
    for i in range(position - 2, position + 3):
        if i in plants and plants[i]:
            positions.append(True)
        else:
            positions.append(False)
    match = tuple(positions)

    if match in rules:
        return rules[match]
    return False

def printplants(plants, min_x=0, max_x=len(plants)):
    string = ''
    for i in range(min_x, max_x):
        if i in plants and plants[i]:
            string += '#'
        else:
            string += '.'
    return string

inputfile = open(args.input)
for line in inputfile:
    regex = re.match(r'initial state: ([\.#]+)', line)
    if regex:
        # Build a list
        statestring = regex.group(1)
        for i in range(len(statestring)):
            if statestring[i] == '#':
                plants[i] = True
            else:
                plants[i] = False
        continue

    regex = re.match(r'([\.#]+) => ([\.#])', line)
    if regex:
        # Append this rule to the list of rules
        match = []
        for c in regex.group(1):
            if c == '#':
                match.append(True)
            else:
                match.append(False)
        if regex.group(2) == '#':
            rules[ tuple(match) ] = True
        else:
            rules[ tuple(match) ] = False

for g in range(generations):
    print(g, "\t", printplants(plants, -3, len(plants)))
    nextgeneration = {}
    positions = sorted(plants.keys())
    # Got to allow this to grow down and up
    for p in range( positions[0] - 2, positions[-1]+3):
        nextgeneration[p] = nextgen(p)

    plants = nextgeneration

print(g, "\t", printplants(plants, -3, len(plants)))

total_plants=0
for p in sorted(plants.keys()):
    if plants[p] == True:
        print("Pot", p, "contains a plant")
        total_plants += p
print(total_plants)

