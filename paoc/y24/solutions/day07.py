#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 24 Day 7 - Bridge Repair """

from paoc.helper import get_input, print_summary
import re
from itertools import product


def total_calibration(lines: list[str], op_chars: str = '+*') -> int:
    total = 0
    for line in lines:
        val, *nums = map(int, re.findall(r'\d+', line))
        for ops in product(op_chars, repeat=len(nums)-1):
            x = nums[0]
            for op, num in zip(ops, nums[1:]):
                if   op == '+': x = x + num
                elif op == '*': x = x * num
                else:           x = int(str(x) + str(num))
            if x == val:
                total += val
                break
    return total

def p1() -> any:
    return total_calibration(get_input(7))

def p2() -> any:
    return total_calibration(get_input(7), op_chars='+*|')


if __name__ == '__main__':
    print_summary(__file__, p1, p2, n=1)
