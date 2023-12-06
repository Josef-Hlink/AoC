#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 22 Day 3 - Rucksack Reorganization """

from paoc.helper import get_input, print_summary


def group(lines, n):
    for i in range(0, len(lines), n):
        yield lines[i:i+n]

def p1() -> any:
    lines: list = get_input(3)
    priority_sum: int = 0
    for line in lines:
        inventory: str = line.strip()
        # find compartments
        sep: int = len(inventory) // 2
        comp1, comp2 = set(inventory[:sep]), set(inventory[sep:])
        # there is only one duplicate, so we can just pop it
        duplicate: str = comp1.intersection(comp2).pop()
        # map duplicate item to priority
        priority: int = ord(duplicate) - 96 if duplicate.islower() else ord(duplicate) - 38
        priority_sum += priority
    
    return priority_sum

def p2() -> any:
    lines: list = get_input(3)
    priority_sum: int = 0
    for ln1, ln2, ln3 in group(lines, 3):
        elf1, elf2, elf3 = ln1.strip(), ln2.strip(), ln3.strip()
        inv1, inv2, inv3 = set(elf1), set(elf2), set(elf3)
        # there should be only one common item, so we can just pop it
        badge: str = inv1.intersection(inv2).intersection(inv3).pop()
        # map badge to priority
        priority: int = ord(badge) - 96 if badge.islower() else ord(badge) - 38
        priority_sum += priority
    return priority_sum


if __name__ == '__main__':
    print_summary(__file__, p1, p2)
