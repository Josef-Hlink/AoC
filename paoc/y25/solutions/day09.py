#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""AoC 25 Day 9 - Movie Theater"""

import re
from itertools import combinations

from paoc.helper import get_input, print_summary

import numpy as np


def p1() -> int:
    lines = get_input(9)
    reds = [tuple(map(int, re.findall(r'\d+', l))) for l in lines]
    max_area = 0
    for t1, t2 in combinations(reds, 2):
        max_area = max(max_area, (abs(t1[0] - t2[0]) + 1) * (abs(t1[1] - t2[1]) + 1))
    return max_area


def p2() -> int:
    r"""Horribly inefficient implementation, but I can't think of something better myself.

    Apparently the red tiles are laid out in a gigantic sort of jagged circle formation,
    with two extreme outliers that form a gap that cuts through the middle of this circle.

    ```text
        /----\
       /      \
       |      |
       -----1 |
       -----2 |
       |      |
       \      /
        \----/
    ```

    First we construct a grid, in which we track the positions of all green tiles that are laid
    to connect the red tiles.
    Then we add a check to our naive p1 algorithm where we assert that no green tiles are allowed
    in the area that would be encapsulated between two red edge tiles.

    Because of this very specific input layout, we also do not have to check every single
    combination of two red tiles, but we can just evaluate areas between gap tile 1 and all red
    tiles north of it, as well as the areas between gap tile 2 and other reds below it.

    This solution still takes a little over a minute on my M4 air.
    """

    lines = get_input(9)
    reds = [tuple(map(int, re.findall(r'\d+', l))) for l in lines]

    # Build grid so we can keep track of lines between reds
    grid = np.zeros((max([x[0] for x in reds]) + 1, max([x[1] for x in reds]) + 1), dtype=np.int8)
    gap_tiles: list[tuple[int, int]] = []
    y_, x_ = reds[0]
    for y, x in reds[1:] + [(y_, x_)]:
        grid[y_, x_] = 1
        if y == y_:
            grid[y, min(x, x_) : max(x, x_)] = 1
        else:  # x == x_
            grid[min(y, y_) : max(y, y_), x] = 1
        if abs(y - y_) > 10_000:  # hardcoded outlier detection, yuck
            gap_tiles.append(max((y, x), (y_, x_), key=lambda tile: tile[0]))
        y_, x_ = y, x

    # sort on x, so we can divide the other red tiles in two halves
    gap_tiles.sort(key=lambda tile: tile[1])

    to_check = [(gap_tiles[0], tile) for tile in reds if tile[1] < gap_tiles[0][1]] + [
        (gap_tiles[1], tile) for tile in reds if tile[1] > gap_tiles[1][1]
    ]

    max_area = 0
    for (y, x), (y_, x_) in to_check:
        if np.any(grid[min(y, y_) + 1 : max(y, y_), min(x, x_) + 1 : max(x, x_)] == 1):
            continue
        max_area = max(max_area, (abs(y - y_) + 1) * (abs(x - x_) + 1))
    return max_area


if __name__ == '__main__':
    print_summary(__file__, p1, p2, n=1)
