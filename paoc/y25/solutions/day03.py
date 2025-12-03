#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""AoC 25 Day 3 - Lobby"""

from paoc.helper import get_input, print_summary


def find_max_total_joltage(banks: list[str], n_batteries: int) -> int:
    total_joltage = 0
    for bank in banks:
        digits = []
        # Left part of invalid slice
        l = -1
        # Right part of invalid slice; you need to leave space for at least
        # `n_batteries - iteration` digits.
        for r in range(n_batteries - 1, -1, -1):
            # Find highest digit in valid slice
            digit = max(bank[l + 1 : len(bank) - r])
            digits.append(digit)
            # Find index of earliest occurrence of this highest digit in valid slice,
            # so it (and everything before it) can be excluded in next iteration.
            l = bank.find(digit, l + 1, len(bank) - r)
        total_joltage += int(''.join(map(str, digits)))
    return total_joltage


def p1() -> int:
    return find_max_total_joltage(get_input(3), n_batteries=2)


def p2() -> int:
    return find_max_total_joltage(get_input(3), n_batteries=12)


if __name__ == '__main__':
    print_summary(__file__, p1, p2)
