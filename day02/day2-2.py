#!/usr/bin/python3

import sys

def compare( first_id, second_id ):
    print("DEBUG: Comparing", first_id, "with", second_id)
    diffs = 0
    for pos in range(len(first_id)):
        if ( first_id[pos] != second_id[pos] ):
            if ( diffs > 0 ):
                print("\tSecond difference between chars, can't be our one", first_id[pos], second_id[pos])
                return False
            else:
                print("\tFirst difference between", first_id[pos], second_id[pos])
                diffs += 1
    if ( diffs == 1 ):
        print("\tExactly one difference between", first_id, second_id)
        return True
    print("Identical strings, has something gone wrong?", first_id, second_id)
    return False

def commonchars( first_id, second_id ):
    output = ''
    for pos in range(len(first_id)):
      if ( first_id[pos] == second_id[pos] ):
          output += first_id[pos]
    return output

# Read the input from the file name specified on the command line
inputfile = open(sys.argv[1])
boxids = [ line.strip() for line in inputfile ]

for start in range(len(boxids)):
    for compto in range(start + 1, len(boxids)):
        if compare( boxids[start], boxids[compto] ):
            print(commonchars( boxids[start], boxids[compto] ))
            sys.exit()
