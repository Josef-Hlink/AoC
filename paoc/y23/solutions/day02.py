#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 23 Day 2 - Cube Conundrum """

from paoc.helper import get_input, print_summary
import re
import math


C_LIMITS = {'red': 12, 'green': 13, 'blue': 14}
COLORS = tuple(C_LIMITS.keys())

def game_id(game: str) -> int:
    """ Returns the game id as an integer. """
    return int(re.search(r'\d+', game).group())

def all_pulls(game: str, color: str) -> list[int]:
    """ Returns all pulls for a given color in the game as a list of integers. """
    return list(map(lambda x: int(x.removesuffix(f' {color}')), re.findall(fr'\d+ {color}', game)))

def max_cubes(game: str) -> dict[str, int]:
    """ Returns the highest number of times each color was pulled in the given game. """
    return {color: max(all_pulls(game, color)) for color in COLORS}

def is_valid(max_cubes: dict[str, int]) -> bool:
    """ Returns whether the game is valid according to the color limits. """
    return sum([max_cubes[color] > limit for color, limit in C_LIMITS.items()]) == 0

def p1() -> any:
    """ Sum of game IDs that are valid. """
    return sum([game_id(game) if is_valid(max_cubes(game)) else 0 for game in get_input(2)])

def p2() -> any:
    """ Sum of the "power" of each game. """
    return sum([math.prod(max_cubes(game).values()) for game in get_input(2)])


if __name__ == '__main__':
    print_summary(__file__, p1, p2)
