#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 22 Day 6 - Tuning Trouble """

from paoc.helper import get_input, print_summary


def p1() -> any:
    data_stream = get_input(6)[0]

    for i in range(4, len(data_stream)):
        buffer = data_stream[i-4:i]
        if len(set(buffer)) == 4:
            break

    return i

def p2() -> any:
    data_stream = get_input(6)[0]

    for i in range(14, len(data_stream)):
        buffer = data_stream[i-14:i]
        if len(set(buffer)) == 14:
            break

    return i


if __name__ == '__main__':
    print_summary(__file__, p1, p2)
