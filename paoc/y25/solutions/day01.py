#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""AoC 25 Day 1 - Secret Entrance"""

from paoc.helper import get_input, print_summary


def p1() -> int:
    x, hits = 50, 0
    for dir, n_steps in map(lambda x: (x[0], int(x[1:])), get_input(1)):
        x += n_steps * (1 if dir == 'R' else -1)
        if x % 100 == 0:
            hits += 1
    return hits


def p2() -> int:
    x, hits = 50, 0
    for dir, n_steps in map(lambda x: (x[0], int(x[1:])), get_input(1)):
        for _ in range(n_steps):
            x = x + 1 if dir == 'R' else x - 1
            if x % 100 == 0:
                hits += 1
    return hits


if __name__ == '__main__':
    print_summary(__file__, p1, p2)
