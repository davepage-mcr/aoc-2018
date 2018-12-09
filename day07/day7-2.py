#!/usr/bin/python3

import sys
import argparse
import string

class Step:
    def __init__(self, name):
        self.name = name
        self.parents = set()
        self.children = set()
        self.duration = Step.basetime + string.ascii_uppercase.find(name) + 1

class Worker:
    def __init__(self, num):
        self.num = num
        self.working_on = None
        self.finished_at = None

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("input", help="Input file")
parser.add_argument("--real", help="Use real input and parameters", action="store_true")
args = parser.parse_args()

num_workers = 2
Step.basetime = 0
if args.real:
    num_workers = 5
    Step.basetime = 60

workers = []
for w in range(num_workers):
    workers.append(Worker(w))

steps = {}

# Read the input from the file name specified on the command line
inputfile = open(args.input)

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
done_steps = set()
undone_steps = set()
for s in steps:
    undone_steps.add( s )
    if len( steps[s].parents ) == 0:
        available_steps.add( s )

steps_order = []

clock = 0
# At each step, pick the alphabetical first available step
while len( undone_steps ) > 0:
    sorted_steps = sorted(available_steps)

    for w in workers:
        # print("\tWorker", w.num, "working on", w.working_on, "until", w.finished_at)
        if w.finished_at and w.finished_at <= clock:
            print("\tWorker", w.num, "has finished", w.working_on)

            done_steps.add(w.working_on)
            undone_steps.remove(w.working_on)
            steps_order.append(w.working_on)

            # Consider what steps we've opened up
            for child in steps[w.working_on].children:
                satisfied = True
                for requirement in steps[child].parents:
                    if requirement not in done_steps:
                        satisfied = False
                        continue

                if satisfied:
                    print("\t\tAll parents of", child, "have been satisfied")
                    available_steps.add(child)

                sorted_steps = sorted(available_steps)

            w.working_on = None
            w.finished_at = None

        if w.working_on == None:
            if ( len(sorted_steps) > 0 ):
                next_step = sorted_steps.pop(0)
                w.working_on = next_step
                w.finished_at = clock + steps[next_step].duration
                print("\tWorker", w.num, "assigned", next_step, "until", w.finished_at)

                available_steps.remove(next_step)

                sorted_steps = sorted(available_steps)

    print(clock, end="\t")
    for w in workers:
        if w.working_on:
            print(w.working_on, end="\t")
        else:
            print('.', end="\t")
    print('Available:', sorted_steps, 'Finished:', ''.join(steps_order))

    clock += 1

print(''.join(steps_order))
