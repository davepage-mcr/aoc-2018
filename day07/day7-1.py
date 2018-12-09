#!/usr/bin/python3

import sys
import re
import pprint
import string

class Step:
    def __init__(self, name):
        self.name = name
        self.parents = set()
        self.children = set()

# Read the input from the file name specified on the command line
inputfile = open(sys.argv[1])

steps = {}

for line in inputfile:
    # Step C must be finished before step A can begin
    parent = line[5]
    child  = line[36]

    if not parent in steps:
        steps[parent] = Step(parent)

    if not child in steps:
        steps[child] = Step(child)

    steps[parent].children.add(child)
    steps[child].parents.add(parent)

# Now look for the nodes with no parents (there may be more than one!)
available_steps = set()
for s in steps:
    if len( steps[s].parents ) == 0:
        available_steps.add( s )

steps_order = []

done_steps = set()
# At each step, pick the alphabetical first available step
while len( available_steps ) > 0:
    sorted_steps = sorted(available_steps )
    print("Possible steps:", sorted_steps)
    next_step = sorted_steps[0]
    print("\tDo step", next_step, "which may unlock", steps[next_step].children)

    done_steps.add(next_step)
    steps_order.append( next_step )
    available_steps.remove(next_step)
    for child in steps[next_step].children:
        print("\t\tConsidering child", child, "with parents", steps[child].parents)
        satisfied = True
        for requirement in steps[child].parents:
            if requirement not in done_steps:
                print("\t\tParent", requirement, "has not been satisfied; cannot add")
                satisfied = False
                continue

        if satisfied:
                print("\t\tAll parents of", child, "have been satisfied")
                available_steps.add(child)

print(''.join(steps_order))
