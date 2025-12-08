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
    boxes = [tuple(map(int, re.findall(r'\d+', l))) for l in lines]
    dists = [(b1, b2, dist(b1, b2)) for i, b1 in enumerate(boxes) for b2 in boxes[i + 1 :]]
    dists.sort(key=lambda t: t[2])
    circuits: list[set[tuple[int, ...]]] = []
    for _ in range(1000):
        b1, b2, _ = dists.pop(0)
        connections = []
        for i, circuit in enumerate(circuits):
            if b1 in circuit or b2 in circuit:
                connections.append(i)
        if len(connections) == 1:
            circuits[connections[0]] |= {b1, b2}
        elif len(connections) > 1:
            new_circuit = set()
            for i in sorted(connections, reverse=True):
                new_circuit |= circuits.pop(i)
            new_circuit |= {b1, b2}
            circuits.append(new_circuit)
        else:
            circuits.append({b1, b2})
    return math.prod(list(sorted(map(len, circuits), reverse=True))[:3])


def p2() -> int:
    lines = get_input(8)
    boxes = [tuple(map(int, re.findall(r'\d+', l))) for l in lines]
    lb = len(boxes)
    dists = [(b1, b2, dist(b1, b2)) for i, b1 in enumerate(boxes) for b2 in boxes[i + 1 :]]
    dists.sort(key=lambda t: t[2])
    circuits: list[set[tuple[int, ...]]] = []
    b1x, b2x = 0, 0
    for b1, b2, _ in dists:
        connections = []
        for i, circuit in enumerate(circuits):
            if b1 in circuit or b2 in circuit:
                connections.append(i)
        if len(connections) == 1:
            circuits[connections[0]] |= {b1, b2}
        elif len(connections) > 1:
            new_circuit = set()
            for i in sorted(connections, reverse=True):
                new_circuit |= circuits.pop(i)
            new_circuit |= {b1, b2}
            circuits.append(new_circuit)
        else:
            circuits.append({b1, b2})
        if len(circuits) == 1 and len(circuits[0]) == lb:
            b1x, b2x = b1[0], b2[0]
            break
    return b1x * b2x


if __name__ == '__main__':
    print_summary(__file__, p1, p2, n=10)
