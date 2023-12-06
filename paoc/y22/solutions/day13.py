#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 22 Day 13 - Distress Signal """

from paoc.helper import get_input, print_summary
import json
from itertools import zip_longest


def compare_elements(left: list, right: list):
    """
    Recursively compares elements of two lists.
    The inputs are always lists, so if a recursive call with an int would be made, it is put in a list of length 1.
    """

    if isinstance(left, int) and isinstance(right, int):
        if left < right: return ORD
        elif left > right: return NORD
        else: return EQ
    if not isinstance(left, list):
        return compare_elements([left], right)
    if not isinstance(right, list):
        return compare_elements(left, [right])
    
    for l, r in zip_longest(left, right, fillvalue=None):
        if l is None: return ORD
        if r is None: return NORD
        is_ordered = compare_elements(l, r)
        if is_ordered != EQ: return is_ordered
    return EQ

def p1() -> any:

    packets = '\n'.join(get_input(13)).split('\n\n')
    packet_pairs = [[json.loads(item) for item in packet] for packet in [packet.split('\n') for packet in packets]]
    ordered_pairs_idx = []

    global ORD, EQ, NORD, STAT
    ORD, EQ, NORD = 1, 0, -1
    STAT = {ORD: 'ordered', EQ: 'equal', NORD: 'not ordered'}

    for idx, (left, right) in enumerate(packet_pairs, start=1):
        if compare_elements(left, right) == ORD:
            ordered_pairs_idx.append(idx)
    return sum(ordered_pairs_idx)

def p2() -> any:
    
    lines = get_input(13)
    packets = [json.loads(line) for line in lines if line != ''] + [[[2]], [[6]]]

    global ORD, EQ, NORD, STAT
    ORD, EQ, NORD = 1, 0, -1
    STAT = {ORD: 'ordered', EQ: 'equal', NORD: 'not ordered'}

    # bubble sort
    for _ in range(len(packets)):
        for j in range(len(packets) - 1):
            if compare_elements(packets[j], packets[j+1]) == NORD:
                packets[j], packets[j+1] = packets[j+1], packets[j]

    # find indices of our divider packets
    for i, packet in enumerate(packets, start=1):
        if packet == [[2]]: i1 = i
        if packet == [[6]]: i2 = i
    
    return i1 * i2


if __name__ == '__main__':
    print_summary(__file__, p1, p2, n=10)
