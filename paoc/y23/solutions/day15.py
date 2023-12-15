#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 23 Day 15 - Lens Library """

from paoc.helper import get_input, print_summary
import re


def HASH(string: str) -> int:
    hash = 0
    for char in string:
        hash += ord(char)
        hash *= 17
        hash %= 256
    return hash

# having lens objects allows for nicer syntax than using tuples
class Lens:
    __slots__ = ['label', 'focal_length']
    
    def __init__(self, label: str):
        self.label = label
    
    def __eq__(self, other: "Lens") -> None:
        """ Allows us to index lenses in a box by their label. """
        return self.label == other.label

def HASHMAP(sequence: str) -> list[list[Lens]]:
    hashmap = [[] for _ in range(256)]
    for instruction in sequence.split(','):
        op_i = re.match(r'\w+', instruction).end()
        label, operation = instruction[:op_i], instruction[op_i]
        hash = HASH(label)
        box = hashmap[hash]
        lens = Lens(label)
        if operation == '=':
            focal_length = int(instruction[op_i+1:])
            if lens in box:
                hashmap[hash][box.index(lens)].focal_length = focal_length
            else:
                lens.focal_length = focal_length
                hashmap[hash].append(lens)
        elif operation == '-':
            if lens in box:
                hashmap[hash].pop(box.index(lens))
        else:
            assert False, "Unreachable"
    return hashmap

def calc_focusing_power(boxes: list[list[Lens]]) -> int:
    focusing_power = 0
    for b, box in enumerate(boxes, start=1):
        for l, lens in enumerate(box, start=1):
            focusing_power += b * l * lens.focal_length
    return focusing_power


def p1() -> int:
    return sum(HASH(instruction) for instruction in get_input(15)[0].split(','))

def p2() -> int:
    return calc_focusing_power(HASHMAP(get_input(15)[0]))


if __name__ == '__main__':
    print_summary(__file__, p1, p2)
