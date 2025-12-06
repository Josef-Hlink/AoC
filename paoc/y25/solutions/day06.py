#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""AoC 25 Day 6 - Trash Compactor"""

from paoc.helper import get_input, print_summary
import re


def p1() -> int:
    lines = get_input(6)
    nums = [re.findall(r'\d+', l) for l in lines[:-1]]
    ops = re.findall(r'[\+\*]', lines[-1])
    return sum(eval(ops[i].join([r[i] for r in nums])) for i in range(len(nums[0])))


def p2() -> int:
    lines = get_input(6)
    lines = [' ' + l for l in lines]  # prepend space for last formula
    res = 0
    buffer = []
    # Walk RtL col-wise, adding joined digits to a buffer until a formula ends
    for i in range(len(lines[0]) - 1, -1, -1):
        col = ''.join([l[i] for l in lines[:-1]])
        # Non-empty column; add number
        if col.strip():
            buffer.append(col)
        # Evaluate numbers in buffer and reset it
        else:
            res += eval(lines[-1][i + 1].join(buffer))
            buffer = []
    return res


if __name__ == '__main__':
    print_summary(__file__, p1, p2)
