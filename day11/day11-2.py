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

        # Now look at all the squares we could now be at the bottom-right of
        biggest_square_size = min(x, y) # This will give 0x0 for the smallest, which works for the slicing below

        for square_size in range(biggest_square_size):
            # We're at the bottom-right of a pre-calculated 3x3 square, can calculate the power for this square at top left
            square = cells[x_sub-square_size:x_sub+1,y_sub-square_size:y_sub+1]
            square_power = square.sum()

            ## TODO: We could probably optimise this by adding the extra row / column / corner on each square_size iteration but numpy runs in <1min

            if max_square_power is None or max_square_power < square_power:
                max_square_power = square_power
                max_square_coords = ( x - square_size, y - square_size, square_size+1 )     # Off-by-one on square_size for presentation

print("Max square power is", max_square_power, "at", ','.join(str(x) for x in max_square_coords))
