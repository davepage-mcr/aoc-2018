#!/usr/bin/python3

import sys

# Frequency counting function

def getfreqs ( boxid ):
    print("DEBUG: Looking at", boxid)
    lfreqs = {}
    for char in boxid:
        if char in lfreqs:
            lfreqs[char] += 1
        else:
            lfreqs[char] = 1
    print("DEBUG: Frequency analysis", lfreqs)
    return ( 2 in lfreqs.values(), 3 in lfreqs.values())

# Read the input from the file name specified on the command line

inputfile = open(sys.argv[1])

num_ids_with_pairs = 0
num_ids_with_triplets = 0

for line in inputfile:
    ( contains_a_pair, contains_a_triplet ) = getfreqs (line.strip())
    if contains_a_pair:
        num_ids_with_pairs += 1
    if contains_a_triplet:
        num_ids_with_triplets += 1

print(num_ids_with_pairs, "box IDs contain at least one pair of letters")
print(num_ids_with_triplets, "box IDs contain at least one triplet of letters")
print("Checksum is", num_ids_with_pairs * num_ids_with_triplets)
