#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""AoC 25 Day 12 - Christmas Tree Farm"""

from paoc.helper import get_input, print_summary

import math


def p1() -> int:
    lines = get_input(12)
    sizes = [sum(c == '#' for c in block) for block in '\n'.join(lines).split('\n\n')[:6]]
    res = 0
    for region in lines[6 * 5 :]:
        area = math.prod(map(int, region.split(':')[0].split('x')))
        qtys = map(int, region.split(': ')[1].split(' '))
        if area >= sum(qty * sizes[i] for i, qty in enumerate(qtys)):
            res += 1
    return res


def p2() -> int:
    lines = get_input(12)
    lines = get_input(12, True)
    _ = lines
    return 0


if __name__ == '__main__':
    print_summary(__file__, p1, p2)
