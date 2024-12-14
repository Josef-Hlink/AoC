#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 24 Day 14 - Restroom Redoubt """

from paoc.helper import get_input, print_summary
import re


def quad_cost(lines: list[str]) -> int:
    wx, wy, s = 101, 103, 100
    g = [[0] * wx for _ in range(wy)]

    for line in lines:
        px, py, vx, vy = map(int, re.findall(r'-?\d+', line))
        px_, py_ = (px+vx*s) % wx, (py+vy*s) % wy
        g[py_][px_] += 1

    q = [0] * 4
    for y in range(wy):
        for x in range(wx):
            if (n:=g[y][x]) == 0:
                continue
            if x < wx // 2:
                if   y < wy // 2: q[0] += n
                elif y > wy // 2: q[2] += n
            elif x > wx // 2:
                if   y < wy // 2: q[1] += n
                elif y > wy // 2: q[3] += n

    return q[0] * q[1] * q[2] * q[3]

def entropy(g: list[list[int]]) -> int:
    """ how "clustered" the robots are """
    e = 0
    for y in range(len(g)):
        for x in range(len(g[0])):
            if g[y][x] == 0:
                continue
            for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                if 0 <= y+dy < len(g) and 0 <= x+dx < len(g[0]):
                    e += g[y+dy][x+dx]
    return e

def seconds_to_christmas_tree(lines: list[str]) -> int:
    wx, wy = 101, 103
    g = [[0] * wx for _ in range(wy)]

    robots = []
    for line in lines:
        px, py, vx, vy = map(int, re.findall(r'-?\d+', line))
        robots.append([px, py, vx, vy])

    me, s_ = 0, 0
    for s in range(wx*wy):
        g = [[0] * wx for _ in range(wy)]
        for robot in robots:
            px, py, vx, vy = robot
            px_, py_ = (px+vx) % wx, (py+vy) % wy
            g[py_][px_] += 1
            robot[0], robot[1] = px_, py_
        if (e:=entropy(g)) > me:
            me, s_ = e, s

    return s_ + 1

def p1() -> any:
    return quad_cost(get_input(14))

def p2() -> any:
    return seconds_to_christmas_tree(get_input(14))


if __name__ == '__main__':
    print_summary(__file__, p1, p2, n=1)
