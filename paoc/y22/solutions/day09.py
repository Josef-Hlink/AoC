#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 22 Day 9 - Rope Bridge """

from paoc.helper import get_input, print_summary


def update_tail1(xh: int, yh: int, xt: int, yt: int) -> tuple[int, int]:
    dx, dy = xh-xt, yh-yt
    if abs(dx) > 1:  # tail needs to catch up
        xt += dx/abs(dx)
        if abs(dy):  # we also need to do a diagonal step
            yt = yh
    if abs(dy) > 1:  # tail needs to catch up
        yt += dy/abs(dy)
        if abs(dx):  # we also need to do a diagonal step
            xt = xh
    return xt, yt

def update_tail2(xh: int, yh: int, xt: int, yt: int) -> tuple[int, int]:
    dx, dy = xh-xt, yh-yt
    # use variables to avoid divby0error when either dx or dy is 0 (0/1 is still zero)
    ax = abs(dx) if dx != 0 else 1
    ay = abs(dy) if dy != 0 else 1
    if not 2 in {ax, ay}:  # no diff of 2 -> no movement
        return xt, yt
    return xt + dx/ax, yt + dy/ay

def print_visited(visited: set):
    X, Y = [i[0] for i in visited], [i[1] for i in visited]
    x_min, x_max = int(min(X)), int(max(X))
    y_min, y_max = int(min(Y)), int(max(Y))
    for y in range(y_min, y_max+1):
        for x in range(x_min, x_max):
            c = '#' if (x, y) in visited else '.'
            print(c, end='')
        print()

def p1() -> any:

    lines = get_input(9)
    d = dict(U=(0, 1), D=(0, -1), R=(1, 0), L=(-1, 0))
    visited = set()

    xh, yh = 0, 0
    xt, yt = 0, 0
    for line in lines:
        direction, steps = line.strip().split(' ')
        for _ in range(int(steps)):
            xh += d[direction][0]
            yh += d[direction][1]
            xt, yt = update_tail1(xh, yh, xt, yt)
            visited.add((xt, yt))

    return len(visited)

def p2() -> any:

    lines = get_input(9)
    d = dict(U=(0, 1), D=(0, -1), R=(1, 0), L=(-1, 0))
    visited = set()

    rope: list[tuple[int, int]] = [(0, 0) for _ in range(10)]
    for line in lines:
        direction, steps = line.strip().split(' ')
        for _ in range(int(steps)):
            xH, yH = rope[0]
            xH, yH = xH + d[direction][0], yH + d[direction][1]
            rope[0] = (xH, yH)
            for knot in range(1, 10):
                # each previous knot will be considered the head now
                xh, yh = rope[knot-1][0], rope[knot-1][1]
                xt, yt = rope[knot][0], rope[knot][1]
                rope[knot] = update_tail2(xh, yh, xt, yt)
            visited.add((rope[9][0], rope[9][1]))
    # print_visited(visited)
    return len(visited)


if __name__ == '__main__':
    print_summary(__file__, p1, p2)
