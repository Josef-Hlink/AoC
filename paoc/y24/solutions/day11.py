#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 24 Day 11 - Plutonian Pebbles """

from paoc.helper import get_input, print_summary
from collections import defaultdict
from functools import cache
import re


@cache  # ~2x speedup: 6ms->3ms for p1 and 90ms->40ms for p2
def evolve(s: str) -> str | tuple[str]:
    if s == '0': return '1'
    elif (l:=len(s)) % 2 == 0: return s[:l//2], str(int(s[l//2:]))
    else: return str(2024*int(s))

def n_stones_after_m_blinks(stones: str, m: int) -> int:
    S = defaultdict(int)
    for s in re.findall(r'\d+', stones): S[s] += 1
    for _ in range(m):
        for s, c in S.copy().items():
            S[s] -= c
            if isinstance(s_:=evolve(s), str): S[s_] += c
            else: S[s_[0]] += c; S[s_[1]] += c
    return sum(S.values())

def p1() -> any:
    return n_stones_after_m_blinks(get_input(11)[0], 25)

def p2() -> any:
    return n_stones_after_m_blinks(get_input(11)[0], 75)


if __name__ == '__main__':
    print_summary(__file__, p1, p2)
