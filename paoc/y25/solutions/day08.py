#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""AoC 25 Day 8 - Playground"""

import math
import re

from paoc.helper import get_input, print_summary


def dist(b1: tuple[int, ...], b2: tuple[int, ...]) -> float:
    return math.sqrt((b1[0] - b2[0]) ** 2 + (b1[1] - b2[1]) ** 2 + (b1[2] - b2[2]) ** 2)


def update_circuits(
    circuits: list[set[tuple[int, ...]]],
    b1: tuple[int, ...],
    b2: tuple[int, ...],
) -> None:
    """Update circuits with new box connection. Modifies circuits list in place!"""

    # Find indices of circuits that connect to b1 or b2
    connections: list[int] = []
    for i, circuit in enumerate(circuits):
        if b1 in circuit or b2 in circuit:
            connections.append(i)

    # Update circuits based on connections found
    if len(connections) == 1:
        circuits[connections[0]] |= {b1, b2}
    elif len(connections) == 2:
        new_circuit = set()
        for i in sorted(connections, reverse=True):  # reverse to avoid index shift
            new_circuit |= circuits.pop(i)
        new_circuit |= {b1, b2}
        circuits.append(new_circuit)
    else:
        circuits.append({b1, b2})


def p1() -> int:
    boxes = [tuple(map(int, re.findall(r'\d+', l))) for l in get_input(8)]
    dists = [(b1, b2, dist(b1, b2)) for i, b1 in enumerate(boxes) for b2 in boxes[i + 1 :]]
    circuits: list[set[tuple[int, ...]]] = []

    # Make 1000 closest connections and return product of sizes of 3 largest circuits
    for b1, b2, _ in sorted(dists, key=lambda tup: tup[2])[:1000]:
        update_circuits(circuits, b1, b2)
    return math.prod(list(sorted(map(len, circuits), reverse=True))[:3])


def p2() -> int:
    boxes = [tuple(map(int, re.findall(r'\d+', l))) for l in get_input(8)]
    dists = [(b1, b2, dist(b1, b2)) for i, b1 in enumerate(boxes) for b2 in boxes[i + 1 :]]
    circuits: list[set[tuple[int, ...]]] = []

    # Connect boxes until all are in one circuit and return
    # product of the x coordinates of the last connected boxes
    b1x, b2x = 0, 0
    for b1, b2, _ in sorted(dists, key=lambda tup: tup[2]):
        update_circuits(circuits, b1, b2)
        if len(circuits) == 1 and len(circuits[0]) == len(boxes):
            b1x, b2x = b1[0], b2[0]
            break
    return b1x * b2x


if __name__ == '__main__':
    print_summary(__file__, p1, p2, n=10)
