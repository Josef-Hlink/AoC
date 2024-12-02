#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 24 Day 2 - Red-Nosed Reports """

from paoc.helper import get_input, print_summary
from itertools import pairwise


def check_safety(report: list[int]) -> bool:
    sign = 1 if report[0] < report[1] else -1
    for a, b in pairwise(report):
        if not (1 <= (b - a) * sign <= 3):
            return False
    return True

def p1() -> any:
    reports = [list(map(int, line.split())) for line in get_input(2)]
    return sum(check_safety(report) for report in reports)

def p2() -> any:
    reports = [list(map(int, line.split())) for line in get_input(2)]  # N x m
    mods_per_report = [[r[:i]+r[i+1:] for i in range(len(r))] for r in reports]  # N x m x (m-1)
    return sum(any(check_safety(mod) for mod in mods) for mods in mods_per_report)

if __name__ == '__main__':
    print_summary(__file__, p1, p2)
