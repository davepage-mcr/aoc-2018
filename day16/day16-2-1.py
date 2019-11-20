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


operations = ( 'addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori',
        'setr', 'seti', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr' )

opspercode = []
for opcodes in range(16):
    opspercode.append(set(operations))

def compute ( bef, inst, operation ):
    aft = bef.copy()

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

    # Now remove any operation which *doesn't* match from the list of possible
    # operations for this opcode

    opcode = instruction[0]

    for operation in operations:
        aft = compute( before, instruction, operation )
        if aft != after:
            opspercode[opcode].discard(operation)

# Now we have a dict of opcodes to sets of operations. Some of these set are
# length 1, meaning that it's a fixed match and we can remove that operation
# from the possibilities of other opcodes (which may reduce them to length 1
# etc.)

finishedcodes = set()

changed = True
while changed == True:
    changed = False

    for opcode in range(16):
        if len(opspercode[opcode]) == 1 and opcode not in finishedcodes:

            operators = tuple( opspercode[opcode] )
            operator = operators[0]

            print("Opcode", opcode, "is", operator)
            finishedcodes.add(opcode)

            for sopcode in range(16):
                if opcode == sopcode: # Skip ourselves!
                    continue
                if operator in opspercode[sopcode]:
                    opspercode[sopcode].remove(operator)
                    changed = True
