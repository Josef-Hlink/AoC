#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 23 Day 14 - Parabolic Reflector Dish """

from paoc.helper import get_input, print_summary
import numpy as np


N = (-1, 0)
S = (+1, 0)
W = (0, -1)
E = (0, +1)

def parse_input(platform: list[str]) -> np.ndarray:
    """ Convert the platform into a np array of integers. """
    return np.array([list(map(lambda x: {'.': 0, 'O': 1, '#': 2}[x], row)) for row in platform])

def tilt(grid: np.ndarray, dir: tuple[int, int]) -> None:
    """ Tilt the grid (inplace!) to make all rounded rocks roll to one side. """
    
    # identify the positions of all rounded rocks
    rrs: list[tuple[int, int]] = list(zip(*np.where(grid == 1)))
    # if direction isn't north, we need to sort the rocks so we process them in the correct order
    if dir == S:
        rrs = sorted(rrs, key=lambda tup: tup[0], reverse=True)
    elif dir == W:
        rrs = sorted(rrs, key=lambda tup: tup[1])
    elif dir == E:
        rrs = sorted(rrs, key=lambda tup: tup[1], reverse=True)
    
    # filter out the rocks that are at the correct border (to avoid index errors)
    if dir[0]:
        rrs = filter(lambda rr: rr[0] != (0 if dir == N else grid.shape[0] - 1), rrs)
    else:
        rrs = filter(lambda rr: rr[1] != (0 if dir == W else grid.shape[1] - 1), rrs)
    
    def shift_dist(y: int, x: int) -> int:
        """ Find the distance a rock has to be shifted for. """
        if dir[0]:  # horizontal shift
            mask: np.ndarray = grid[y+dir[0]::dir[0], x] != 0
            max_shift = y if dir == N else grid.shape[0] - 1 - y
        else:  # vertical shift
            mask: np.ndarray = grid[y, x+dir[1]::dir[1]] != 0
            max_shift = x if dir == W else grid.shape[1] - 1 - x
        return np.where(mask.any(), mask.argmax(), max_shift)
    
    for y, x in rrs:
        dist = shift_dist(y, x)
        # remove rock from old position
        grid[y, x] = 0
        # put rock in new position
        if dir[0]:
            grid[y+(dir[0] * dist), x] = 1
        else:
            grid[y, x+(dir[1] * dist)] = 1
    
    return None

def calc_load(grid: np.ndarray) -> int:
    """ Weird AoC-style calculation to get a final answer. """
    return sum((grid.shape[0]-i) * sum(row == 1) for i, row in enumerate(grid))

def as_tuple(grid: np.ndarray) -> tuple[int]:
    """ We use this as a unique identifier for a grid. """
    return tuple(grid.flatten())

def p1() -> any:
    grid = parse_input(get_input(14))
    tilt(grid, N)
    return calc_load(grid)

def p2() -> any:
    grid = parse_input(get_input(14))

    # loop as long as needed until we find a grid configuration we've already seen before
    memory = []
    while as_tuple(grid) not in memory:
        memory.append(as_tuple(grid))
        # perform one tilting cycle
        for dir in (N, W, S, E):
            tilt(grid, dir)
    
    # now we know the length of the loop
    loop_length = len(memory) - memory.index(as_tuple(grid))
    # so we can forget everything before we entered it
    loop = memory[-loop_length:]
    # see what configuration we'd land on after 10^9 cycles
    i = (int(1e9) - len(memory)) % loop_length
    final_grid = np.array(loop[i]).reshape(grid.shape)
    # and finally calculate the total load on the north support beams again
    return calc_load(final_grid)


if __name__ == '__main__':
    print_summary(__file__, p1, p2, n=10)
