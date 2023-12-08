#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 23 Day 6 - Wait For It """

from paoc.helper import get_input, print_summary
import re
import math


def ways_to_beat(t: int, d: int) -> int:
    """ ax^2 + bx + c = 0 with a=-1, b=t, c=-d [args: `t` time to beat, `d` distance] """
    return math.floor((-t - (sqD := math.sqrt(t**2 - 4*d))) / (-2) - 1e-9) - math.ceil((-t + sqD) / (-2) + 1e-9) + 1

def p1() -> any:
    return math.prod([ways_to_beat(t, d) for t, d in zip(*map(lambda line: [int(x) for x in re.findall(r'\d+', line)], get_input(6)))])

def p2() -> any:
    return ways_to_beat(*map(lambda line: int(re.findall(r'\d+', line.replace(' ', ''))[0]), get_input(6)))


if __name__ == '__main__':
    print_summary(__file__, p1, p2)
