#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 24 Day 1 - Historian Hysteria """

from paoc.helper import get_input, print_summary


def p1() -> any:
    l, r = zip(*map(lambda x: x.split('   '), get_input(1)))
    return sum(abs(int(a) - int(b)) for a, b in zip(sorted(l), sorted(r)))

def p2() -> any:
    l, r = zip(*map(lambda x: x.split('   '), get_input(1)))
    return sum(int(a) * r.count(a) for a in l)


if __name__ == '__main__':
    print_summary(__file__, p1, p2)
