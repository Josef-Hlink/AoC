#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 23 Day 11 - Cosmic Expansion """

from paoc.helper import get_input, print_summary
import numpy as np
from itertools import combinations


def calc_distances(image: list[str], n_exp: int = 1) -> list[int]:
    """ Find out which rows and columns are empty, then calculate adjusted Manhattan distance. """
    universe = np.array([['.#'.index(c) for c in row] for row in image], dtype=bool)
    empty = tuple(set(np.where(universe.sum(axis=i)==0)[0]) for i in (1, 0))
    return [distance(a, b, empty, n_exp) for a, b in combinations(zip(*np.where(universe==1)), 2)]

def distance(a: tuple[int, int], b: tuple[int, int], empty: tuple[set[int]], n_exp: int) -> int:
    """ Manhattan distance adjusted by number of expansions. """
    dist = 0
    # for both row and col, we do essentially the same thing
    for i in (1, 0):
        a, b = sorted((a, b), key=lambda x: x[i])
        #  add:   manhattan +  (no. times we cross an empty row/col) * multiplier
        dist += b[i] - a[i] + len(set(range(a[i], b[i])) & empty[i]) * n_exp
    return dist

def distance_1l(a: tuple[int, int], b: tuple[int, int], empty: tuple[set[int]], n_exp: int) -> int:
    """ Oneliner version of above; it's slightly slower as we have to call `abs()` and do extra sorting. """
    return sum(abs((ai:=a[i])-(bi:=b[i])) + len(set(range(min(ai, bi), max(ai, bi))) & empty[i]) * n_exp for i in (1, 0))

def p1() -> int:
    return sum(calc_distances(get_input(11)))

def p2() -> int:
    return sum(calc_distances(get_input(11), n_exp=int(1e6-1)))


if __name__ == '__main__':
    print_summary(__file__, p1, p2, n=10)
