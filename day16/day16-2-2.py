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

def compute ( bef, inst ):
    aft = bef.copy()

    opcode = inst[0]
    inpa = inst[1]
    inpb = inst[2]
    output = inst[3]

    operation = operations[opcode]

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
        print("Undefined opcode", opcode )

    return aft

# In order from day16-2-1.py
operations = ( 'eqri', 'bani', 'seti', 'bori', 'eqir', 'banr', 'borr', 'muli',
        'setr', 'addr', 'eqrr', 'addi', 'gtir', 'gtrr', 'gtri', 'mulr' )

registers = [0,0,0,0]

inputfile = open(args.input)
for line in inputfile:
    line = line.strip()

    parse = re.match(r'^(\d+) (\d+) (\d+) (\d+)', line)
    if not parse:
        print("Couldn't parse", line)
        continue

    instruction = ( [ int(x) for x in parse.group(1,2,3,4) ] )
    registers = compute( registers, instruction )

print(registers)
