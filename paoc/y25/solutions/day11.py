#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""AoC 25 Day 11 - Reactor"""

from functools import cache

from paoc.helper import get_input, print_summary


def p1() -> int:
    graph = {line.split(':')[0]: line.split(': ')[1].split(' ') for line in get_input(11)}

    @cache
    def n(node: str) -> int:
        if node == 'out':
            return 1
        return sum(n(node_) for node_ in graph[node])

    return n('you')


def p2() -> int:
    graph = {line.split(':')[0]: line.split(': ')[1].split(' ') for line in get_input(11)}

    @cache
    def n(node: str, dac: bool, fft: bool) -> int:
        if node == 'out':
            if dac and fft:
                return 1
            return 0
        if node == 'dac':
            dac = True
        if node == 'fft':
            fft = True
        return sum(n(node_, dac, fft) for node_ in graph[node])

    return n('svr', False, False)


if __name__ == '__main__':
    print_summary(__file__, p1, p2)
