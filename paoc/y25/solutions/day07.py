#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""AoC 25 Day 7 - Laboratories"""

from functools import cache

import numpy as np

from paoc.helper import get_input, print_summary


def p1() -> int:
    lines = get_input(7)
    beams = {lines[0].index('S')}
    n_splits = 0
    for line in lines[1:]:
        splitters = np.where(np.array(list(line)) == '^')[0]
        for beam in filter(lambda beam: beam in splitters, beams.copy()):
            n_splits += 1
            beams.remove(beam)
            beams |= {beam - 1, beam + 1}
    return n_splits


def p2() -> int:
    GRID = np.array([list(l) for l in get_input(7)])

    @cache
    def beam(r: int, c: int, n_splits: int) -> int:
        # base case -> bottom of grid reached
        if r == GRID.shape[0]:
            return 1
        # splitter encountered -> spawn two new beams
        if GRID[r, c] == '^':
            return beam(r + 1, c - 1, n_splits + 1) + beam(r + 1, c + 1, n_splits + 1)
        # normal cell -> continue downwards
        return beam(r + 1, c, n_splits)

    return beam(0, np.where(GRID[0] == 'S')[0][0], 0)


if __name__ == '__main__':
    print_summary(__file__, p1, p2)
