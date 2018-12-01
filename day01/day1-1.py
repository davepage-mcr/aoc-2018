#!/usr/bin/python3

import sys

# Read the input from the file name specified on the command line

inputfile = open(sys.argv[1])

freq = 0
for line in inputfile:
    freqdiff = int(line)
    freq += freqdiff

print(freq)
