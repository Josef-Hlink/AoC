#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""AoC 25 Day 5 - Cafeteria"""

from paoc.helper import get_input, print_summary
import re


def p1() -> int:
    lines = get_input(5)
    s = lines.index('')
    ranges = [range(int((r := re.findall(r'\d+', line))[0]), int(r[1]) + 1) for line in lines[:s]]
    return sum(any(i in r for r in ranges) for i in map(int, lines[s + 1 :]))


def discard_dupes(r1: range, r2: range) -> range:
    return range(max(r1.start, r2.stop), r1.stop)


def p2() -> int:
    lines = get_input(5)
    s = lines.index('')
    ranges = [range(int((r := re.findall(r'\d+', line))[0]), int(r[1]) + 1) for line in lines[:s]]
    exc_ranges: list[range] = []
    for r1 in sorted(ranges, key=lambda r: r.start):
        for r2 in exc_ranges:
            r1 = discard_dupes(r1, r2)
        if r1.stop > r1.start:
            exc_ranges.append(r1)
    return sum(map(lambda r: r.stop - r.start, exc_ranges))


if __name__ == '__main__':
    print_summary(__file__, p1, p2)
