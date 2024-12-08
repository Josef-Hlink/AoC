#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 24 Day 8 - Resonant Collinearity """

from paoc.helper import get_input, print_summary
import re
from collections import defaultdict
from itertools import combinations


class Vec:
    def __init__(self, i: int, j: int):
        self.i, self.j, self.tup = i, j, (i, j)
    def __add__(self, other: 'Vec') -> 'Vec':
        return Vec(self.i + other.i, self.j + other.j)
    def __mul__(self, l: int) -> 'Vec':
        return Vec(self.i * l, self.j * l)

def locate_antinodes(lines: list[str], mul: int = 1) -> set[tuple]:
    """ mul sets the direction of vector projection """
    
    assert mul in {1, -1}
    I, J = range(len(lines)), range(len(lines[0]))  # dimensions

    # first group the antennae
    antennae = defaultdict(set)
    for i, line in enumerate(lines):
        for match in re.finditer(f'[^\.]', line):  # match every non-'.' char
            antennae[match.group()].add(Vec(i, match.span()[0]))
    
    # now find all unique antinodes
    antinodes = set()
    for positions in antennae.values():
        for a, b in combinations(positions, 2):
            d  = b + (a * -1)        # difference (a-b)
            a_ = a + (d * -1 * mul)  # mirror b if mul 1, overlap b if mul -1
            b_ = b + (d * mul)       # mirror a if mul 1, overlap a if mul -1
            while a_.i in I and a_.j in J:
                antinodes.add(a_.tup); a_ = a_ + d
                if mul == 1: break
            while b_.i in I and b_.j in J:
                antinodes.add(b_.tup); b_ = b_ + (d * -1)
                if mul == 1: break
    return antinodes

def p1() -> any:
    return len(locate_antinodes(get_input(8)))

def p2() -> any:
    return len(locate_antinodes(get_input(8), mul=-1))


if __name__ == '__main__':
    print_summary(__file__, p1, p2)
