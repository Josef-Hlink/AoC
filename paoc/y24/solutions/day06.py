#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 24 Day 6 - Guard Gallivant """

from paoc.helper import get_input, print_summary
from itertools import product
from copy import deepcopy


C = '^>v<'
D = {'^': (-1,0), '>': (0,1), 'v': (1,0), '<': (0,-1)}
def step(i: int, j: int, d: str) -> tuple[int, int]:
    return i + D[d][0], j + D[d][1]

def find_start(grid: list[list[str]]) -> tuple[int, int]:
    for i, j in product(range(len(grid)), range(len(grid[0]))):
        if grid[i][j] in C:
            break
    return i, j    

def traverse(grid: list[list[str]], check_loop: bool = False) -> tuple[set, bool]:
    """ walk the path of the guard and check if there's loops
    
    returns the set of unique positions the guard has walked,
    and wether or not a loop was found
    """
    I, J = range(len(grid)), range(len(grid[0]))
    i, j = find_start(grid)
    d = grid[i][j]  # current direction
    visA, visB = set(), set()  # B also remembers direction
    
    while True:
        visA.add((i, j)); visB.add((i, j, d))
        i_, j_ = step(i, j, d)
        if i_ not in I or j_ not in J:  # escaped grid, so no loop
            return visA, False
        if grid[i_][j_] == '#':
            d = C[(C.index(d)+1)%4]  # turn logic
        else:
            i, j = i_, j_ 
        if check_loop and (i, j, d) in visB:  # loop detected
            return visA, True

def p1() -> any:
    return len(traverse([list(line) for line in get_input(6)])[0])

def p2() -> any:
    """ bruteforce approach; extremely slow (30s) """
    grid = [list(line) for line in get_input(6)]
    to_check = traverse(grid)[0]
    to_check.remove(find_start(grid))
    
    n_pos = 0
    for i, j in to_check:
        grid_ = deepcopy(grid)
        grid_[i][j] = '#'
        n_pos += traverse(grid_, check_loop=True)[1]
    return n_pos


if __name__ == '__main__':
    print_summary(__file__, p1, p2, n=1)
