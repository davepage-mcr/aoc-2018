#!/usr/bin/python3

import sys

def compare( first_id, second_id ):
    print("DEBUG: Comparing", first_id, "with", second_id)
    pos = 0
    diffs = 0
    while pos < len(first_id):
        if ( first_id[pos] != second_id[pos] ):
            if ( diffs > 0 ):
                print("\tSecond difference between chars, can't be our one", first_id[pos], second_id[pos])
                return False
            else:
                print("\tFirst difference between", first_id[pos], second_id[pos])
                diffs += 1
        pos += 1
    if ( diffs == 1 ):
        print("\tExactly one difference between", first_id, second_id)
        return True
    print("Identical strings, has something gone wrong?", first_id, second_id)
    return False

def commonchars( first_id, second_id ):
    pos = 0
    output = ''
    while pos < len(first_id):
      if ( first_id[pos] == second_id[pos] ):
          output += first_id[pos]
      pos += 1
    return output

# Read the input from the file name specified on the command line
inputfile = open(sys.argv[1])
boxids = [ line.strip() for line in inputfile ]

start = 0
while start < len(boxids):
    compto = start + 1
    while compto < len(boxids):
        if compare( boxids[start], boxids[compto] ):
            print(commonchars( boxids[start], boxids[compto] ))
            sys.exit()
        compto += 1
    start += 1
