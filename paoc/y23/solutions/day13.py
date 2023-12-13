#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 23 Day 13 - Point of Incidence """

from paoc.helper import get_input, print_summary
import numpy as np


def parse_input(lines: list[str]) -> list[np.ndarray]:
    """ Each pattern in the input file (separated by an empty line) becomes a np array. """
    return [np.array([list(r) for r in p.split('\n')]) for p in '\n'.join(lines).split('\n\n')]

def find_split(grid: np.ndarray, smudged: bool = False) -> int:
    """ Finds the row index after which the grid is mirrored. If no such index exists, returns 0. """
    
    # if the grid is smudged, we want to know its original split so we can ignore that one
    orig_split = find_split(grid, smudged=False) if smudged else 0
    
    # evaluate all possible splits
    for split in range(1, grid.shape[0]):
        
        if split == orig_split:
            continue
        
        # iteratively check if the backward and corresponding forward row are the same
        violations = 0
        for backward, forward in zip(reversed(grid[:split]), grid[split:]):
            # if the grid is smudged, we tolerate 1 (truthy) violation
            # otherwise we tolerate 0 (falsy) violations
            violations += sum(backward != forward)
            if violations > smudged:
                break
        
        # loop wasn't broken out of, so no(t enough) violations were found for this split
        else:
            return split

    # no split was found
    return 0


def p1() -> int:
    res = 0
    for grid in parse_input(get_input(13)):
        # there's only ever one horizontal or vertical split,
        # so if a horizontal one was found we don't have to evaluate the vertical too
        res += 100 * find_split(grid) or find_split(grid.T)
    return res

def p2() -> int:
    res = 0
    for grid in parse_input(get_input(13)):
        res += 100 * find_split(grid, smudged=True) or find_split(grid.T, smudged=True)
    return res


if __name__ == '__main__':
    print_summary(__file__, p1, p2)
