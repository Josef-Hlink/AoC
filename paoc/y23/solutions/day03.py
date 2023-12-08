#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 23 Day 3 - Gear Ratios """

from paoc.helper import get_input, print_summary
import re
from itertools import product


def neighborhood(i: int, j1: int, j2: int = None) -> set[tuple[int, int]]:
    """ Direct neighborhood of elements at row `i`, columns `j1`-`j2`. If `j2` is unspecified, only `j1` is considered. """
    j2 = j2 or j1 + 1
    return set(product(range(i-1, i+2), range(j1-1, j2+1))) - {(i, j_) for j_ in range(j1, j2)}

class PartNumber:
    """ Part number in the engine schematic. """
    exp = r'\d+'

    def __init__(self, i: int, match: re.Match):
        self.i = i
        self.j1, self.j2 = match.span()
        self.positions = {(self.i, j) for j in range(self.j1, self.j2)}
        self.value = int(match.group())
    
    @property
    def neighbors(self) -> set[tuple[int, int]]:
        return neighborhood(self.i, self.j1, self.j2)

class Symbol:
    """ Any non-".", non-digit character in the engine schematic. """
    exp = r'[^\.|\d]'

    def __init__(self, i: int, match: re.Match):
        self.i = i
        self.j = match.span()[0]
        self.position = (self.i, self.j)
        self.char = match.group()

    @property
    def neighbors(self) -> set[tuple[int, int]]:
        return neighborhood(self.i, self.j)


def p1() -> int:
    """ Sum of all part numbers that have a symbol in their direct neighborhood. """
    engine_schematic = get_input(3)
    part_numbers: set[PartNumber] = set()
    symbols_positions: set[tuple[int, int]] = set()

    for i, row in enumerate(engine_schematic):
        part_numbers.update({PartNumber(i, match) for match in re.finditer(PartNumber.exp, row)})
        symbols_positions.update({Symbol(i, match).position for match in re.finditer(Symbol.exp, row)})
    
    return sum([pn.value if pn.neighbors & symbols_positions else 0 for pn in part_numbers])


def p2() -> int:
    """ Sum of all "gear ratios"; product of two part numbers that are in the direct neighborhood of a `*` symbol. """
    engine_schematic = get_input(3)
    part_numbers: set[PartNumber] = set()
    symbols: set[Symbol] = set()
    for i, row in enumerate(engine_schematic):
        part_numbers.update({PartNumber(i, match) for match in re.finditer(PartNumber.exp, row)})
        symbols.update({Symbol(i, match) for match in re.finditer(Symbol.exp, row)})

    res = 0
    for gear in filter(lambda x: x.char == '*', symbols):
        nbs = gear.neighbors
        values = [pn.value for pn in filter(lambda x: abs(x.i - gear.i) <= 1, part_numbers) if nbs & pn.positions]
        if len(values) == 2: res += values[0] * values[1]
    return res


if __name__ == '__main__':
    print_summary(__file__, p1, p2)
