#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 24 Day 4 - Ceres Search """

from paoc.helper import get_input, print_summary


def p1() -> any:
    grid = get_input(4)
    pattern = 'XMAS'
    dirs = [(-1, -1), (-1, +0), (-1, +1),
            (+0, -1),           (+0, +1),
            (+1, -1), (+1, +0), (+1, +1)]
    count = 0
    I, J = range(len(grid)), range(len(grid[0]))

    for i in I:
        for j in J:
            if grid[i][j] != 'X':
                continue
            for i_, j_ in dirs:
                for n in range(1, 4):
                    ni, nj = i+i_*n, j+j_*n
                    if ni not in I or nj not in J or grid[ni][nj] != pattern[n]:
                        break
                else:
                    count += 1

    return count

def p2() -> any:
    grid = get_input(4)
    dirs = [(-1, -1), (-1, +1), (+1, -1), (+1, +1)]
    count = 0
    I, J = range(1, len(grid)-1), range(1, len(grid[0])-1)

    for i in I:
        for j in J:
            if grid[i][j] != 'A':
                continue
            neighbors = [grid[i+i_][j+j_] for i_, j_ in dirs]
            if neighbors.count('M') == 2 and neighbors.count('S') == 2 and ''.join(neighbors) not in ['MSSM', 'SMMS']:
                count += 1
    
    return count

if __name__ == '__main__':
    print_summary(__file__, p1, p2)
