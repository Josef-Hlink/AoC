#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""AoC 25 Day 8 - Playground"""

import re
import math

from paoc.helper import get_input, print_summary


def dist(b1: tuple[int, ...], b2: tuple[int, ...]) -> float:
    return math.sqrt((b1[0] - b2[0]) ** 2 + (b1[1] - b2[1]) ** 2 + (b1[2] - b2[2]) ** 2)


def p1() -> int:
    lines = get_input(8)
    # lines = get_input(8, True)
    boxes = [tuple(map(int, re.findall(r'\d+', l))) for l in lines]
    print(len(boxes))
    dists = [(b1, b2, dist(b1, b2)) for i, b1 in enumerate(boxes) for b2 in boxes[i + 1 :]]
    dists.sort(key=lambda t: t[2])
    circuits: list[set[tuple[int, ...]]] = []
    for _ in range(1000):
        b1, b2, _ = dists.pop(0)
        for i, circuit in enumerate(circuits):
            if b1 in circuit or b2 in circuit:
                circuits[i] = circuit | {b1, b2}
                break
        else:
            circuits.append({b1, b2})
        # check if we can do any merges
        final_circuits = []
        for i, circuit in enumerate(circuits):
            coll = circuit
            for j, oth in enumerate(circuits[i + 1 :]):
                if circuit.intersection(oth):
                    coll |= oth
                    circuits[j] = set()
            final_circuits.append(coll)
        circuits = final_circuits

    for fc in sorted(map(len, circuits), reverse=True):
        if fc < 3:
            break
        print(fc)

    return math.prod(list(sorted(map(len, circuits), reverse=True))[:3])


def p2() -> int:
    lines = get_input(8)
    lines = get_input(8, True)
    _ = lines
    return 0


if __name__ == '__main__':
    print(p1())
    print(p2())
    exit()
    print_summary(__file__, p1, p2)
