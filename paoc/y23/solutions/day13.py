#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 23 Day 13 - Point of Incidence """

from paoc.helper import get_input, print_summary
import numpy as np


def parse_input(lines: list[str]) -> list[np.ndarray]:
    """ TODO: add param to `get_input` to get raw contents or make new function for this (to preserve type correctness). """
    return [np.array([list(map('.#'.index, row)) for row in grid.split('\n')], dtype=bool) for grid in '\n'.join(lines).split('\n\n')]

def find_mirror(grid: np.ndarray, skip_split: int = 0) -> int:
    for split in range(1, grid.shape[0]):
        if split == skip_split:
            continue
        for back, forward in zip(reversed(grid[:split]), grid[split:]):
            if any(back != forward):
                break
        else:
            return split
    return 0

def p1() -> int:
    grids = parse_input(get_input(13))
    res = 0
    for grid in grids:
        res += 100 * find_mirror(grid)
        res += find_mirror(np.transpose(grid))
    return res

def p2() -> int:
    grids = parse_input(get_input(13))
    res = 0
    for grid in grids:
        orig_hor = find_mirror(grid)
        orig_ver = find_mirror(np.transpose(grid))
        smudge_found = False
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                grid_ = grid.copy()
                grid_[i,j] = not grid_[i,j]
                if (hor := find_mirror(grid_, skip_split=orig_hor)):
                    smudge_found = True; break
                if (ver := find_mirror(np.transpose(grid_), skip_split=orig_ver)):
                    smudge_found = True; break
            if smudge_found:
                res += 100 * hor
                res += ver
                break
        else:
            assert False
    return res


if __name__ == '__main__':
    print_summary(__file__, p1, p2)
