#!/usr/bin/python3

import argparse
import numpy as np

gridsize=300

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("serial", help="Grid Serial Number", type=int)
args = parser.parse_args()

serial = args.serial

cells = np.zeros( (gridsize,gridsize), dtype=int )

max_square_power = None
max_square_coords = ( None, None )

for x_sub in range(gridsize):
    for y_sub in range(gridsize):
        # Convert from array subscripts to coordinates, avoid off-by-one errors
        x = x_sub + 1
        y = y_sub + 1

        rack_id = x + 10
        power = ( ( rack_id * y ) + serial ) * rack_id

        # Extract hundreds digit
        power %= 1000               # Strip off anything bigger
        power //= 100               # Lose the smaller stuff

        power -= 5

        cells[x_sub][y_sub] = power

        if x_sub > 1 and y_sub > 1:
            # We're at the bottom-right of a pre-calculated 3x3 square, can calculate the power for this square at top left
            square_power = 0
            for square_x in range(x_sub-2, x_sub+1):
                for square_y in range(y_sub-2, y_sub+1):
                    square_power += cells[square_x][square_y]
            # print("Total power for square with top-left subscript", [ x_sub-2, y_sub-2 ], square_power)
            if max_square_power is None or max_square_power < square_power:
                max_square_power = square_power
                max_square_coords = ( x_sub - 1, y_sub - 1 )

print("Max square power is", max_square_power, max_square_coords)
