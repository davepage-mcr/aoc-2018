#!/usr/bin/python3

import sys
import re
import pprint
import string

# Read the input from the file name specified on the command line
inputfile = open(sys.argv[1])

reductions = []
for char in string.ascii_lowercase:
    reductions.append( char + char.upper() ) 
for char in string.ascii_uppercase:
    reductions.append( char + char.lower() ) 

reductions_re = '(' + '|'.join(reductions) + ')'

for line in inputfile:
    polymer = line.strip()
    reduced = ''
    # print("Polymer is\t" + polymer)

    while True:
        # Need a regular expression for a lower character followed by its upper version
        reduced = re.sub(reductions_re, '', polymer)
        if polymer != reduced:
            # print("\tReduce\t" + reduced)
            polymer = reduced
        else:
            break

print("Polymer is", len(polymer), "long")
