#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 24 Day 10 - Hoof It """

from paoc.helper import get_input, print_summary


def hike(i: int, j: int, h: int, D: list[tuple], all_trails: bool = False) -> int | None:
    """ recursive gridwalk from a 0 to a 9 """
    if h == 9:  # target reached
        return D.append((i, j))
    for di, dj in ((-1, 0), (0, -1), (0, 1), (1, 0)):  # rook neighbors
        if not ((i_:=i+di) in I and (j_:=j+dj) in J):  # bound check
            continue
        if grid[i_][j_] == (h_:=h+1):  # valid move
            _ = hike(i_, j_, h_, D, all_trails)  # keep going (recurse) 
    if h == 0:  # only top-level function call should return at end
        return len(D) if all_trails else len(set(D))

def solve(lines: list[str], all_trails: bool = False) -> int:
    global grid; grid = [list(map(int, line)) for line in lines]
    global I, J; I, J = range(len(grid)), range(len(grid[0]))
    trailheads = ((i, j) for i in I for j in J if grid[i][j] == 0)
    return sum(hike(t[0], t[1], 0, [], all_trails) for t in trailheads)

def p1() -> any:
    return solve(get_input(10))

def p2() -> any:
    return solve(get_input(10), all_trails=True)


if __name__ == '__main__':
    print_summary(__file__, p1, p2)
