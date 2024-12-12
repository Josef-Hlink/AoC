#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 24 Day 12 - Garden Groups """

from paoc.helper import get_input, print_summary
from collections import deque, defaultdict
from itertools import product


DIRS = ((-1, 0), (1, 0), (0, -1), (0, 1))

def map_region(s: tuple[int, int]) -> set[int, int]:
    c = GRID[s[0]][s[1]]
    Q, R = deque([s]), set()
    while Q:
        i, j = Q.popleft()
        if (i, j) in R: continue
        R.add((i, j))
        for di, dj in DIRS:
            if (i_:=i+di) in I and (j_:=j+dj) in J and GRID[i_][j_] == c:
                Q.append((i_, j_))
    return R

def calc_perimeter_1(region: set[tuple]) -> int:
    s = region.pop(); region.add(s)
    c = GRID[s[0]][s[1]]
    p = 0
    for i, j in region:
        for di, dj in DIRS:
            if (i_:=i+di) in I and (j_:=j+dj) in J:
                if GRID[i_][j_] != c:
                    p += 1
            else:
                p += 1
    return p

def grow(i: int, j: int, face: set[tuple], visited: set[tuple]) -> None:
    """ ! modifies visited ! """
    Q = deque([(i, j)])
    while Q:
        i, j = Q.popleft()
        for di, dj in DIRS:
            i_, j_ = i+di, j+dj
            if (i_, j_) not in face or (i_, j_) in visited:
                continue
            Q.append((i_, j_))
            visited.add((i_, j_))

def calc_perimeter_2(region: set[tuple]) -> int:
    if len(region) == 1: return 4
    faces = defaultdict(set)
    for i, j in region:
        if (i-1, j) not in region:
            faces[i, 0].add((i, j))
        if (i+1, j) not in region:
            faces[i, 1].add((i, j))
        if (i, j-1) not in region:
            faces[j, 2].add((i, j))
        if (i, j+1) not in region:
            faces[j, 3].add((i, j))
    p = 0
    for face in faces.values():
        visited = set()
        for i, j in face:
            if (i, j) not in visited:
                grow(i, j, face, visited)
                p += 1
    return p

def solve(lines: list[str], cost_func: callable) -> int:
    global GRID; GRID = lines
    global I, J; I, J = range(len(GRID)), range(len(GRID[0]))
    unmapped = set(product(I, J))
    cost = 0
    while unmapped:
        region = map_region(unmapped.pop())
        unmapped -= region
        cost += len(region) * cost_func(region)
    return cost

def p1() -> any:
    return solve(get_input(12), cost_func=calc_perimeter_1)

def p2() -> any:
    return solve(get_input(12), cost_func=calc_perimeter_2)


if __name__ == '__main__':
    print_summary(__file__, p1, p2)
