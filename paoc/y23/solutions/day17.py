# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

""" AoC 23 Day 17 - Clumsy Crucible """

from paoc.helper import get_input, print_summary, parse_multiline_string as pms
import numpy as np
from queue import PriorityQueue


class State:
    __slots__ = ['r', 'c', 'a', 'h']
    def __init__(self, r: int, c: int, a: int, h: int):
        """ row, col, axis traveled to get to this point, heat accumulated """
        self.r, self.c, self.a, self.h = r, c, a, h

    def __lt__(self, other: "State") -> bool:
        """ so we can use these objects in a priority queue """
        return self.h < other.h

def min_heat_loss(grid: np.ndarray, min_steps: int = 1, max_steps: int = 3) -> int:
    q = PriorityQueue()
    R, C = grid.shape - np.array([1, 1])
    q.put(State(0, 0, 0, 0))
    q.put(State(0, 0, 1, 0))

    visited = set()
    while q:
        s = q.get()
        if (s.r, s.c) == (R, C):
            break  # goal position reached
        if (s.r, s.c, s.a) in visited:
            continue  # already seen
        visited.add((s.r, s.c, s.a))
        h = s.h
        for sign in (-1, +1):  # try both ways (up & down / left & right)
            h_ = h
            r_, c_ = s.r, s.c
            for steps in range(1, max_steps + 1):
                if s.a == 0:  # we're taking steps along the 0th axis; rows
                    r_ = s.r + steps * sign
                else:  # we're taking steps along the 1st axis; columns
                    c_ = s.c + steps * sign
                if r_ < 0 or c_ < 0 or r_ > R or c_ > C:
                    break  # out of bounds
                h_ += grid[c_, r_]
                if (r_, c_, 1 - s.a) in visited:
                    continue  # already seen
                if steps >= min_steps:
                    q.put(State(r_, c_, 1 - s.a, h_))

    return s.h


def p1() -> int:
    grid = np.array([list(row) for row in get_input(17)], dtype=int)
    return min_heat_loss(grid)

def p2() -> int:
    grid = np.array([list(row) for row in get_input(17)], dtype=int)
    return min_heat_loss(grid, min_steps=4, max_steps=10)


if __name__ == '__main__':
    print_summary(__file__, p1, p2, n=10)
