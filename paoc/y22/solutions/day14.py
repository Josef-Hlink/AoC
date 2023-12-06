#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 22 Day 14 - Regolith Reservoir """

from paoc.helper import get_input, print_summary
import re
import numpy as np


def create_cave(lines: list[str], full: bool = False) -> np.ndarray:
    """
    Create a numpy array from the input lines representing the cave.
    The cave is filled with 1 for rocks and 0 for air, sand will be represented by 2.
    If full is True, we make the array way wider to allow for the overflowing sand.
    We also have to put an empty and a rock row at the bottom of the cave if full is True.
    """
    # find all coordinates with regex (xxx,yyy? -> xxx,yyy -> ...)
    # y can have 3 digits, x always has 3, a line has an unknown number of coordinates
    x_coords = [int(point[0]) for line in lines for point in re.findall(r'(\d+),(\d+)', line)]
    y_coords = [int(point[1]) for line in lines for point in re.findall(r'(\d+),(\d+)', line)]

    # create a numpy array for the cave
    x_max, y_max = max(x_coords), max(y_coords)
    # set cave width to 1000, because source is at 500
    x_max = 1000 if full else x_max
    cave = np.zeros((y_max + 1, x_max + 1), dtype=int)

    # fill the cave with the coordinates (1 for rock, 2 for sand later on)
    for line in lines:
        points = re.findall(r'(\d+),(\d+)', line)
        current = (int(points[0][0]), int(points[0][1]))
        cave[current[1], current[0]] = 1
        for point in points[1:]:
            next_point = (int(point[0]), int(point[1]))
            ly, hy = min(current[1], next_point[1]), max(current[1], next_point[1])
            lx, hx = min(current[0], next_point[0]), max(current[0], next_point[0])
            cave[ly:hy+1, lx:hx+1] = 1
            current = next_point
    
    if full: cave = np.vstack((cave, np.zeros((2, cave.shape[1]), dtype=int))); cave[-1, :] = 1
    
    return cave

def get_sand_pos(cave: np.ndarray) -> tuple[int, int]:
    """
    Simulate the sand falling down one coordinate at a time, until it reaches a rock or another sand particle.
    Avoid accessing indices outside the cave.
    """
    x, y = 500, 0
    x_max = cave.shape[1] - 1
    while y < cave.shape[0] - 1:
        if cave[y + 1, x] == 0:
            y += 1
        else:
            if cave[y+1, x - 1] == 0:
                x -= 1
            elif x+1 <= x_max and cave[y+1, x + 1] == 0:
                x += 1
            else:
                break
    return x, y

def render(cave: np.ndarray) -> None:
    repr = {0: '.', 1: '#', 2: 'o'}
    x_min, x_max = 498, 502
    try:
        while cave[:-1, x_min].any(): x_min -= 1
    except IndexError: pass
    try:
        while cave[:-1, x_max].any(): x_max += 1
    except IndexError: pass
    first_row = '  0 ' + '.' * (500-x_min) + '+' + '.' * (x_max-500)
    print(''.join(first_row))
    lowest_sand = np.where(cave == 2)[0].max()
    start_from = max(1, lowest_sand - 20)
    if start_from > 1: print('    ' + '-' * (len(first_row)-4))
    for i, row in enumerate(cave[start_from:start_from+20]):
        print(f'{start_from+i+1:>3}', ''.join([repr[col] for col in row[x_min:x_max+1]]))
    print(f'sand particles: {np.count_nonzero(cave == 2)}')
    input()

def p1() -> any:
    lines = get_input(14)
    cave = create_cave(lines)
    particles = 0
    while True:
        x, y = get_sand_pos(cave)
        if y == cave.shape[0] - 1:
            break
        cave[y, x] = 2
        particles += 1
        # render(cave)
    
    return particles

def p2() -> any:
    lines = get_input(14)
    cave = create_cave(lines, full=True)
    particles = 0
    while True:
        x, y = get_sand_pos(cave)
        particles += 1
        cave[y, x] = 2
        # render(cave)
        if y == 0:
            break
    
    return particles


if __name__ == '__main__':
    print_summary(__file__, p1, p2, n=10)
