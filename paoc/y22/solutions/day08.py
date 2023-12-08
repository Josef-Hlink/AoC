#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 22 Day 8 - Treetop Tree House """

from paoc.helper import get_input, print_summary
import numpy as np

def is_visible(r: int, c: int) -> bool:
    return (
        np.all(grid[r, c+1:] < grid[r, c]) or
        np.all(grid[r, :c] < grid[r, c]) or
        np.all(grid[r+1:, c] < grid[r, c]) or
        np.all(grid[:r, c] < grid[r, c])
    )

def get_score(r: int, c: int) -> int:
    """
    Walk in every direction (up, down, right, left) until you find a tree that's just as high or higher 
    The number of steps + 1 is the viewing distance in that direction
    Total score is all four viewing distances multiplied
    """
    score = 1
    height = grid[r, c]
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        r_, c_ = r, c
        steps = 0
        while True:
            r_ += dr
            c_ += dc
            if r_ < 0 or r_ >= grid.shape[0] or c_ < 0 or c_ >= grid.shape[1]:
                break
            steps += 1
            if grid[r_, c_] >= height:
                break
        score *= steps
    return score

def p1() -> any:
    lines = get_input(8)
    global grid
    grid = np.array([list(line) for line in lines]).astype(int)
    n_trees = (grid.shape[0] + grid.shape[1]) * 2 - 4
    for r in range(1, grid.shape[0]-1):
        for c in range(1, grid.shape[1]-1):
            if is_visible(r, c):
                n_trees += 1
    return n_trees

def p2() -> any:
    lines = get_input(8)
    global grid
    grid = np.array([list(line) for line in lines]).astype(int)
    max_score = 0
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            score = get_score(r, c)
            max_score = max(score, max_score)

    return max_score


if __name__ == '__main__':
    print_summary(__file__, p1, p2, n=10)
