#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 23 Day 13 - Point of Incidence """

from paoc.helper import get_input, print_summary
import numpy as np


def parse_input(lines: list[str]) -> list[np.ndarray]:
    """ TODO: add param to `get_input` to get raw contents or make new function for this (to preserve type correctness). """
    return [np.array([list(map('.#'.index, row)) for row in grid.split('\n')], dtype=bool) for grid in '\n'.join(lines).split('\n\n')]

def find_mirror(grid: np.ndarray, smudged: bool = False) -> int:
    orig_split = find_mirror(grid, smudged=False) if smudged else 0
    for split in range(1, grid.shape[0]):
        if split == orig_split:
            continue
        violations = 0
        for back, forward in zip(reversed(grid[:split]), grid[split:]):
            violations += sum(back != forward)
            if violations > smudged:
                break
        else:
            return split
    return 0

def p1() -> int:
    grids = parse_input(get_input(13))
    res = 0
    for grid in grids:
        res += 100 * find_mirror(grid)
        res += find_mirror(grid.T)
    return res

def p2() -> int:
    grids = parse_input(get_input(13))
    res = 0
    for grid in grids:
        res += 100 * find_mirror(grid, smudged=True)
        res += find_mirror(grid.T, smudged=True)
    return res


if __name__ == '__main__':
    print_summary(__file__, p1, p2)
