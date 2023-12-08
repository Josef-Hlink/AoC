#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 23 Day 8 - Haunted Wasteland """

from paoc.helper import get_input, print_summary
import re
import math


def parse_doc(doc: list[str]) -> tuple[list[bool], dict[str, tuple[str, str]]]:
    """ `D` is the directions as list of bools (left is 0, right is 1).
        `G` is the graph as dict; `{from: (to1, to2), ...}`. """
    D = [d=='R' for d in (doc)[0]]
    G = {(N:=re.findall(r'\w{3}', line))[0]: (N[1], N[2]) for line in doc[2:]}
    return D, G

def p1() -> int:
    """ 'AAA' node walks through graph until we find 'ZZZ'.
        We return no. steps it took this node. """
    D, G = parse_doc(get_input(8))
    n = 'AAA'
    ld, s = len(D), 0
    while n != 'ZZZ':
        n, s = G[n][D[s%ld]], s + 1
    return s

def p2() -> int:
    """ Each '__A' node walks through graph until we find '__Z'.
        We return LCM of no. steps it took each node. """
    D, G = parse_doc(get_input(8))
    N = tuple(n for n in G.keys() if n.endswith('A'))
    ld, S = len(D), [0 for _ in range(len(N))]
    for i, n in enumerate(N):
        while not n.endswith('Z'):
            n, S[i] = G[n][D[S[i]%ld]], S[i] + 1
    return math.lcm(*S)


if __name__ == '__main__':
    print_summary(__file__, p1, p2)
