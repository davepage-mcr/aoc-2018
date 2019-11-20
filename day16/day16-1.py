#!/usr/bin/python3

import argparse
import pprint
import re

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("input", help="Input file")
parser.add_argument("--verbose", help="Show grids", action="store_true")
args = parser.parse_args()

# Each opcode becomes a function with two inputs - the initial register state
# and the rest of the instruction, and returns an "after" tuple which can be
# compared

def compute ( bef, inst, operation ):
    aft = bef.copy()

    opcode = inst[0]
    inpa = inst[1]
    inpb = inst[2]
    output = inst[3]

    if operation == 'addr':
        aft[output] = bef[inpa] + bef[inpb]
    elif operation == 'addi':
        aft[output] = bef[inpa] + inpb
    elif operation == 'mulr':
        aft[output] = bef[inpa] * bef[inpb]
    elif operation == 'muli':
        aft[output] = bef[inpa] * inpb
    elif operation == 'banr':
        aft[output] = bef[inpa] & bef[inpb]
    elif operation == 'bani':
        aft[output] = bef[inpa] & inpb
    elif operation == 'borr':
        aft[output] = bef[inpa] | bef[inpb]
    elif operation == 'bori':
        aft[output] = bef[inpa] | inpb
    elif operation == 'setr':
        aft[output] = bef[inpa]
    elif operation == 'seti':
        aft[output] = inpa
    elif operation == 'gtir' or operation == 'gtri' or operation == 'gtrr':
        if ( operation == 'gtir' and inpa > bef[inpb] ) or \
                ( operation == 'gtri' and bef[inpa] > inpb ) or \
                ( operation == 'gtrr' and bef[inpa] > bef[inpb] ):
            aft[output] = 1
        else:
            aft[output] = 0
    elif operation == 'eqir' or operation == 'eqri' or operation == 'eqrr':
        if ( operation == 'eqir' and inpa == bef[inpb] ) or \
                ( operation == 'eqri' and bef[inpa] == inpb ) or \
                ( operation == 'eqrr' and bef[inpa] == bef[inpb] ):
            aft[output] = 1
        else:
            aft[output] = 0
    else:
        print("Undefined operation", operation)

    return aft

operations = ( 'addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori',
        'setr', 'seti', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr' )

answer = 0

inputfile = open(args.input)
for line in inputfile:
    line = line.strip()

    parse = re.match(r'^\s*$', line)
    if parse:
        continue

    parse = re.match(r'^Before:\s+\[(\d+), (\d+), (\d+), (\d+)\]', line)
    if parse:
        before = ( [ int(x) for x in parse.group(1,2,3,4) ] )
        continue

    parse = re.match(r'^(\d+) (\d+) (\d+) (\d+)', line)
    if parse:
        instruction = ( [ int(x) for x in parse.group(1,2,3,4) ] )
        continue

    parse = re.match(r'^After:\s+\[(\d+), (\d+), (\d+), (\d+)\]', line)
    if not parse:
        print("Couldn't parse", line)
        continue
    after = ( [ int(x) for x in parse.group(1,2,3,4) ] )

    # Now count the opcodes which could be applied to before to get after
    opcode = instruction[0]
    nummatches = 0

    for operation in operations:
        aft = compute( before, instruction, operation )
        if aft == after:
            nummatches += 1

    if nummatches >= 3:
        answer += 1

print(answer)
