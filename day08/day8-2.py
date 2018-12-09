#!/usr/bin/python3

import sys
import argparse
import string

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("input", help="Input file")
args = parser.parse_args()

class Node:
    node_number = 0

    def __init__(self, data):
        self.number = Node.node_number
        Node.node_number += 1

        self.children = []
        self.metadata = []
        self.cached_value = None

        num_children = data.pop(0)
        num_meta = data.pop(0)

        for c in range(num_children):
            self.children.append( Node(data) )

        for m in range(num_meta):
            self.metadata.append( data.pop(0) )

    def value(self):
        print("\nCalculating value for node", self.number)

        if self.cached_value:
            print("\tReturning cached value", self.cached_value)
            return self.cached_value

        value = 0
        if len(self.children) == 0:
            for m in self.metadata:
                value += m
            print("\tNode has no children; return sum of metadata", self.metadata, value)
            self.cached_value = value
            return value

        # We have children, treat metadata as indices
        print("\tNode", self.number, "has", len(self.children), "children, ids", [ x.number for x in self.children ], "look at indices", self.metadata)
        for m in self.metadata:
            if m == 0:
                print("Index 0 means skip")
                continue

            i = m - 1
            if i >= len( self.children ):
                print("We don't have a", m, "node; skip")
                continue

            print("Adding the value of the ", m, "th child, Node", self.children[i].number)
            value += self.children[i].value()

        self.cached_value = value
        return value

# Read the input from the file name specified on the command line
inputfile = open(args.input)
for line in inputfile:
    data = [ int(x) for x in line.split() ]

root = Node(data)

print(root.value())
