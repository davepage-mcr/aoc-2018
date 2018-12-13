#!/usr/bin/python3

import argparse
import pprint
from colorama import Fore, Style

class Cart:
    # This is what we assme we're covering at the start
    # "On your initial map, the track under each cart is a straight path matching the direction the cart is facing."
    charmap = { '^':    '|', '>':    '-', 'v':    '|', '<':    '-' }

    # Map direction to ( change in x, change in y )
    dirmap = {
            '^':      ( 0, -1 ),
            '>':      ( 1, 0 ),
            'v':      ( 0, 1 ),
            '<':      ( -1, 0 ),
    }

    # Turns based on current direction and thing we're now covering
    turnmap = {
            # Straight on
            ( '^', '|' ):   '^',
            ( '>', '-' ):   '>',
            ( 'v', '|' ):   'v',
            ( '<', '-' ):   '<',
            # Turn corners
            ( '^', '\\' ):  '<', ( '^', '/' ):   '>',
            ( '>', '\\' ):  'v', ( '>', '/' ):   '^',
            ( 'v', '\\' ):  '>', ( 'v', '/' ):   '<',
            ( '<', '\\' ):  '^', ( '<', '/' ):   'v',
    }

    # Directions at intersection based on direction and turn 0 = left 1 = straight 2 = right
    intersection = {
          ('^', 0):       '<', ('^', 1):       '^', ('^', 2):       '>',
          ('>', 0):       '^', ('>', 1):       '>', ('>', 2):       'v',
          ('v', 0):       '>', ('v', 1):       'v', ('v', 2):       '<',
          ('<', 0):       'v', ('<', 1):       '<', ('<', 2):       '^',
    }

    def __init__(self, char, x, y):
        self.dir    = char
        self.under  = Cart.charmap[char]
        self.x      = x
        self.y      = y
        self.nextturn = 0
        self.crashed = False

    def tick(self):
        print("Cart at", ( self.x, self.y ), "heading", self.dir, "covering", self.under)
        if self.crashed:
            print("\tSome bugger crashed into us!")
            # We've crashed and we know it, so just return
            return True

        # First replace ourselves on the grid with the thing under us
        grid[self.y][self.x] = self.under

        # Change position based on current direction
        self.x += Cart.dirmap[self.dir][0]
        self.y += Cart.dirmap[self.dir][1]
        self.under = grid[self.y][self.x]
        # print("\tChange position: now at", ( self.x, self.y ), "heading", self.dir, "covering", self.under)

        # Change position or crash, based on new position
        if self.under == '+':
            self.dir = Cart.intersection[ (self.dir, self.nextturn ) ]
            self.nextturn = ( self.nextturn + 1 ) % 3

        elif self.under in [ '^', '>', 'v', '<' ]:
            print("\tCrashed into another cart!")
            # We have crashed
            self.crashed = True

            # Find the cart we crashed into, and mark it as crashed too
            # ALSO: Replace the grid at this position with whatever's under the other cart, to signify removal of crashed cards
            victims = list( filter( lambda c: c != self and c.x == self.x and c.y == self.y, carts ) )
            for v in victims:
                print("\tFound the victim cart at", (v.x, v.y))
                v.crashed = True
                v.dir = 'X'
                grid[self.y][self.x] = v.under
            return False

        elif ( self.dir, self.under ) in Cart.turnmap:
            self.dir = Cart.turnmap[(self.dir, self.under)]

        else:
            print("\tWe're going", self.dir, "over a", self.under, "and don't know what to do")

        print("\tCart now at", ( self.x, self.y ), "heading", self.dir, "covering", self.under)
        # Finally, mark our new position and direction on the grid
        grid[self.y][self.x] = self.dir

        return True

def printgrid(grid):
    for line in grid:
        for c in line:
            if c in [ '>', '<', '^', 'v' ]:
                print(Fore.GREEN + c + Style.RESET_ALL, end='')
            else:
                print(c, end='')
        print()

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("input", help="Input file")
parser.add_argument("--verbose", help="Show grids", action="store_true")
args = parser.parse_args()

pp = pprint.PrettyPrinter()

grid=[]
carts=[]

inputfile = open(args.input)
y=0
for line in inputfile:
    line_list = list(line.rstrip())
    for x in range(len(line_list)):
        char = line[x]
        if char in [ '^', 'v', '<', '>' ]:
            carts.append( Cart(char, x, y) )
    grid.append(line_list)
    y += 1

t = 0

while len(carts) > 1:
    print("Time:", t)
    if args.verbose:
        printgrid(grid)

    # Sort list of carts each tick
    # "carts on the top row move first (acting from left to right), then carts on the second row move (again from left to right)"
    # https://stackoverflow.com/questions/4233476/sort-a-list-by-multiple-attributes - sort by tuple
    for c in sorted( carts, key = lambda c: ( c.y, c.x ) ):
        c.tick()

    carts = list( filter( lambda c: c.crashed == False, carts ) )

    t += 1

if args.verbose:
    printgrid(grid)

if len(carts) == 0:
    print("All carts annihilated!")
else:
    survivor = carts[0]
    print("Surviving cart is at", ( survivor.x, survivor.y ))
