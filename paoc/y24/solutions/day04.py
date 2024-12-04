#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 24 Day 4 - Ceres Search """

from paoc.helper import get_input, print_summary
from itertools import product


def p1() -> any:
    """ Find XMAS in any direction, overlaps allowed """
    grid = get_input(4)
    pattern = 'XMAS'
    dirs = list(product((-1, 0, +1), repeat=2))  # all 9 directions
    dirs.remove((0, 0))  # remove "stationary" direction
    count, I, J = 0, range(len(grid)), range(len(grid[0]))

    for i, j in product(I, J):
        if grid[i][j] != 'X':
            continue
        for i_, j_ in dirs:  # check every direction
            for n in range(1, 4):
                ni, nj = i+i_*n, j+j_*n
                if ni not in I or nj not in J or grid[ni][nj] != pattern[n]:
                    break
            else:  # loop not broken out of; full pattern found
                count += 1

    return count

def p2() -> any:
    """ Find two MAS patterns that cross (X) each other at the A """
    grid = get_input(4)
    dirs = list(product((-1, +1), repeat=2))  # diagonal (X) directions
    count, I, J = 0, range(1, len(grid)-1), range(1, len(grid[0])-1)
    
    for i, j in product(I, J):
        if grid[i][j] != 'A':
            continue
        X = [grid[i+i_][j+j_] for i_, j_ in dirs]  # X-neighbors
        if X.count('M') == X.count('S') == 2 and X[1] != X[2]:  # prevent MAMxSAS
            count += 1
    
    return count

if __name__ == '__main__':
    print_summary(__file__, p1, p2)
