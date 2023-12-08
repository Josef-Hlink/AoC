#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 22 Day 4 - Camp Cleanup """

from paoc.helper import get_input, print_summary


def p1() -> any:
    
    lines = get_input(4)
    n_overlaps: int = 0

    for line in lines:
        # see what sectors the elves are responsible for
        elf1, elf2 = line.split(',')
        elf1_start, elf1_end = [int(n) for n in elf1.split('-')]
        elf2_start, elf2_end = [int(n) for n in elf2.split('-')]
        elf1_sec = set(range(elf1_start, elf1_end+1))
        elf2_sec = set(range(elf2_start, elf2_end+1))
        # check if either of them is a subset of the other
        if elf1_sec.issubset(elf2_sec) or elf2_sec.issubset(elf1_sec):
            n_overlaps += 1
    
    return n_overlaps


def p2() -> any:

    lines = get_input(4)
    n_overlaps: int = 0

    for line in lines:
        # see what sectors the elves are responsible for
        elf1, elf2 = line.split(',')
        elf1_start, elf1_end = [int(n) for n in elf1.split('-')]
        elf2_start, elf2_end = [int(n) for n in elf2.split('-')]
        elf1_sec = set(range(elf1_start, elf1_end+1))
        elf2_sec = set(range(elf2_start, elf2_end+1))
        # check if there in an intersection between the two
        if elf1_sec.intersection(elf2_sec):
            n_overlaps += 1
    
    return n_overlaps


if __name__ == '__main__':
    print_summary(__file__, p1, p2)
