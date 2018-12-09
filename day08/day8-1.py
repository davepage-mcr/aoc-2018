#!/usr/bin/python3

import sys
import argparse
import string

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("input", help="Input file")
args = parser.parse_args()

allnodes = set()

class Node:
    # node_ids = list( string.ascii_uppercase + string.ascii_lowercase )

    def __init__(self, data):
        # self.name = Node.node_ids.pop(0)
        self.name = None
        self.children = set()
        self.metadata = []

        num_children = data.pop(0)
        num_meta = data.pop(0)

        for c in range(num_children):
            self.children.add( Node(data) )

        for m in range(num_meta):
            self.metadata.append( data.pop(0) )

        print("New node:", self.name, "with", num_children, "children and", num_meta, "metadata entries")
        print("\tChildren are", [ x.name for x in self.children ])
        print("\tMetadata is", self.metadata)

        allnodes.add(self)

# Read the input from the file name specified on the command line
inputfile = open(args.input)
for line in inputfile:
    data = [ int(x) for x in line.split() ]

root = Node(data)

meta_sum = 0
for n in allnodes:
    for m in n.metadata:
        meta_sum += m

print("We have", len(allnodes), "nodes")
print("Metadata sum:", meta_sum)
