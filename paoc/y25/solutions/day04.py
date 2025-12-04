#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""AoC 25 Day 4 - Printing Department"""

import numpy as np

from paoc.helper import get_input, print_summary


def build_grid(lines: list[str]) -> np.ndarray:
    grid = np.array([['.@'.index(c) for c in line] for line in lines])
    return np.pad(grid, 1, 'constant', constant_values=0)


def remove_rolls(grid: np.ndarray, use_copy: bool = True) -> None:
    """Without a copy, removing a roll might interfere with another roll's "removability".

    Note that this function directly modifies the grid that is being passed, so we do not
    need to return anything.
    """
    grid_ = np.copy(grid) if use_copy else grid
    for x, y in np.argwhere(grid):
        if grid_[x - 1 : x + 2, y - 1 : y + 2].sum() < 5:
            grid[x, y] = 0


def p1() -> int:
    """See how many rolls are hypothetically removable."""
    grid = build_grid(get_input(4))
    n_rolls_start = grid.sum()
    remove_rolls(grid)
    return n_rolls_start - grid.sum()


def p2() -> int:
    """Actually remove rolls until no more can be removed."""
    grid = build_grid(get_input(4))
    n_rolls_start = grid.sum()
    n_rolls_removed = None
    while n_rolls_removed != 0:
        n_rolls_before = grid.sum()
        # No need for a copy here, that only slows us down bc we would need more iterations
        remove_rolls(grid, use_copy=False)
        n_rolls_removed = n_rolls_before - grid.sum()
    return n_rolls_start - grid.sum()


if __name__ == '__main__':
    print_summary(__file__, p1, p2, n=10)
