#!/usr/bin/python3

import sys

# Read the input from the file name specified on the command line

inputfile = open(sys.argv[1])
inputs = [ int(x) for x in inputfile ]

freq = 0
seenfreqs = [ freq ]

while True:
    for freqdiff in inputs:
        freq += freqdiff
        print("Interim frequency ", freq)
        if freq in seenfreqs:
            print("We've seen", freq, "before")
            sys.exit()
        seenfreqs.append(freq)
    print("Looping over input")

print(freq)
