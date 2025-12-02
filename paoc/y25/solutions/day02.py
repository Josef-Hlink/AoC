#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""AoC 25 Day 2 - Gift Shop"""

import re
from collections.abc import Callable
from itertools import batched

from paoc.helper import get_input, print_summary


def find_invalid_ids_sum(ranges: str, invalidator: Callable[[int], bool]) -> int:
    """Find the sum of all invalid gift IDs in the given ranges."""
    res = 0
    for match in re.finditer(r'(\d+)-(\d+)', ranges):
        n1, n2 = map(int, match.groups())
        for id in range(n1, n2 + 1):  # inclusive
            if invalidator(id):
                res += id
    return res


def is_double_digit(id: int) -> bool:
    """Check if the given ID consists of two identical halves."""
    s = str(id)
    half = len(s) // 2
    return s[:half] == s[half:]


def has_repeating_sequence(id: int) -> bool:
    """Check if the given ID has a repeating sequence of digits."""
    s = str(id)
    half = len(s) // 2
    # Check for all possible chunk sizes
    for n in range(1, half + 1):
        # Check if the string is made up of repeating chunks of size n
        prev = tuple(s[:n])
        for chunk in batched(s[n:], n):
            if prev != chunk:
                break
            prev = chunk
        else:  # not broken out of; all chunks matched
            return True
    return False


def p1() -> int:
    return find_invalid_ids_sum(get_input(2)[0], invalidator=is_double_digit)


def p2() -> int:
    return find_invalid_ids_sum(get_input(2)[0], invalidator=has_repeating_sequence)


if __name__ == '__main__':
    print_summary(__file__, p1, p2, n=10)
