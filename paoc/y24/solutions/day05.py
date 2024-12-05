#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 24 Day 5 - Print Queue """

from paoc.helper import get_input, print_summary
from collections import defaultdict


def parse(lines: list[str]) -> tuple[dict[int, set[int]], map[list[int]]]:
    """ split doc into dict with rules and iterable (map) with updates """
    i = lines.index('')  # empty line splits rules from updates
    rules = defaultdict(set)
    # page "a" keeps memory of what pages "b" should not come before it
    for a, b in map(lambda x: tuple(map(int, x.split('|'))), lines[:i]):
        rules[a].add(b)
    updates = map(lambda x: list(map(int, x.split(','))), lines[i+1:])
    return rules, updates

def fix(update: list[int], rules: dict[int, set[int]]) -> list[int]:
    """ returns (modified) copy of list passed """
    update = update.copy()
    for i, p in enumerate(update):
        violations = list(map(lambda r: p not in r, [rules[u] for u in update[:i]]))
        if any(violations):
            # move page to rightmost index where it does not violate rules
            update.pop(i); update.insert(violations.index(True), p)
    return update


def p1() -> any:
    rules, updates = parse(get_input(5))
    return sum(u[len(u)//2] if u == fix(u, rules) else 0 for u in updates)

def p2() -> any:
    rules, updates = parse(get_input(5))
    return sum(f[len(f)//2] if u != (f:=fix(u, rules)) else 0 for u in updates)


if __name__ == '__main__':
    print_summary(__file__, p1, p2)
