#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 23 Day 9 - Mirage Maintenance """

from paoc.helper import get_input, print_summary
import re
from itertools import pairwise


def get_extrapolated_values(histories: list[list[int]]) -> list[int]:
    extrapolated_values = []
    for history in histories:
        diffs = get_diffs(seq=history)
        extrapolated_value = extrapolate_from_diffs(diffs)
        extrapolated_values.append(extrapolated_value)
    return extrapolated_values

def get_diffs(seq: list[int]) -> list[list[int]]:
    diffs = [seq]
    while any(seq):
        seq = [n2-n1 for n1, n2 in pairwise(seq)]
        diffs.append(seq)
    return diffs

def extrapolate_from_diffs(diffs: list[list[int]]) -> int:
    inv = diffs[::-1]
    for i, row in enumerate(inv):
        extrapolated_value = 0 if i == 0 else row[-1] + inv[i-1][-1]
        row.append(extrapolated_value)
    return inv[-1][-1]

def p1() -> int:
    oasis_report = get_input(9)
    histories = [[int(n) for n in re.findall(r'-?\d+', line)] for line in oasis_report]
    return sum(get_extrapolated_values(histories))

def p2() -> int:
    oasis_report = get_input(9)
    histories = [[int(n) for n in re.findall(r'-?\d+', line)][::-1] for line in oasis_report]
    return sum(get_extrapolated_values(histories))


if __name__ == '__main__':
    print_summary(__file__, p1, p2)
