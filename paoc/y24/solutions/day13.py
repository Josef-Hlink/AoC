#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 24 Day 13 - Claw Contraption """

from paoc.helper import get_input, print_summary
import re


def tokens_to_win(lines: list[str], add_10t: bool = False) -> int:
    tokens = 0
    for la, lb, lp, _ in zip(*[iter(lines+[''])] * 4):
        ax, ay = map(int, re.findall(r'\d+', la))
        bx, by = map(int, re.findall(r'\d+', lb))
        px, py = map(int, re.findall(r'\d+', lp))
        if add_10t: px, py = px + int(1e13), py + int(1e13)
        
        d = ax*by - ay*bx
        a = (a_:=(px*by - py*bx)) // d
        b = (b_:=(ax*py - ay*px)) // d
        if a_ % d == 0 and b_ % d == 0:
            tokens += a * 3 + b

    return tokens

def p1() -> any:
    return tokens_to_win(get_input(13))

def p2() -> any:
    return tokens_to_win(get_input(13), add_10t=True)


if __name__ == '__main__':
    print_summary(__file__, p1, p2)
