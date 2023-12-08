#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 22 Day 1 - Calorie Counting """

from paoc.helper import get_input, print_summary


def p1() -> any:
    lines = get_input(1)
    inventory_sum = 0
    largest_inventory = 0
    for i, line in enumerate(lines):
        if (line == '') or (i == len(lines)-1):
            largest_inventory = max(largest_inventory, inventory_sum)
            inventory_sum = 0
        else:
            inventory_sum += int(line.strip())

    return largest_inventory

def p2() -> any:

    # we'll store all inventory sums here
    inventory_sums = []

    # read the input file
    lines = get_input(1)
    
    inventory_sum = 0
    for i, line in enumerate(lines):
        if (line == '') or (i == len(lines)-1):
            inventory_sums.append(inventory_sum)
            inventory_sum = 0
        else:
            inventory_sum += int(line.strip())

    # sort descending
    inventory_sums_sorted = sorted(inventory_sums, reverse=True)

    # return sum of the three highest sums
    return sum(inventory_sums_sorted[:3])


if __name__ == '__main__':
    print_summary(__file__, p1, p2)
