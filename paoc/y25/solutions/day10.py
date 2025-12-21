#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""AoC 25 Day 10 - Factory"""

import re
from collections import deque
from functools import cache
from itertools import combinations, product

from paoc.helper import get_input, print_summary


def update_state(state: tuple[bool, ...], button: tuple[int, ...]) -> tuple[bool, ...]:
    return tuple(not state[i] if i in button else state[i] for i in range(len(state)))


def bfs(target: tuple[bool, ...], buttons: list[tuple[int, ...]]) -> int:
    initial_state = tuple(False for _ in target)
    queue = deque([(initial_state, 0)])
    visited = {initial_state}
    while queue:
        state, steps = queue.popleft()
        if state == target:
            return steps
        for button in buttons:
            new_state = update_state(state, button)
            if new_state not in visited:
                visited.add(new_state)
                queue.append((new_state, steps + 1))
    raise ValueError('No solution found')


def p1() -> int:
    lines = get_input(10)
    res = 0
    for line in lines:
        target = tuple(c == '#' for c in line[1:].split(']')[0])
        buttons = [tuple(map(int, b.split(','))) for b in re.findall(r'\(([\d+,]*\d+)\)', line)]
        res += bfs(target, buttons)
    return res


def patterns(coeffs: list[tuple[int, ...]]) -> dict[tuple[int, ...], dict[tuple[int, ...], int]]:
    n_buttons = len(coeffs)
    n_vars = len(coeffs[0])
    # Generate all possible patterns and their costs
    out = {parity_pattern: {} for parity_pattern in product([0, 1], repeat=n_vars)}
    for n_buttons_pressed in range(n_buttons + 1):
        # Try all combinations of n_buttons_pressed buttons
        for buttons in combinations(range(n_buttons), n_buttons_pressed):
            # Calculate the resulting pattern by summing the coefficients
            pattern = tuple(map(sum, zip((0,) * n_vars, *(coeffs[i] for i in buttons))))
            parity_pattern = tuple(i % 2 for i in pattern)
            # Store the pattern and its cost if not already present
            if pattern not in out[parity_pattern]:
                out[parity_pattern][pattern] = n_buttons_pressed
    return out


def solve_single(buttons: list[tuple[int, ...]], target: tuple[int, ...]) -> int:
    coeffs = [tuple(int(i in button) for i in range(len(target))) for button in buttons]
    pattern_costs = patterns(coeffs)

    @cache
    def solve_single_aux(target: tuple[int, ...]) -> int:
        if all(i == 0 for i in target):
            return 0
        answer = 1000000
        for pattern, pattern_cost in pattern_costs[tuple(i % 2 for i in target)].items():
            if all(i <= j for i, j in zip(pattern, target)):
                new_goal = tuple((j - i) // 2 for i, j in zip(pattern, target))
                answer = min(answer, pattern_cost + 2 * solve_single_aux(new_goal))
        return answer

    return solve_single_aux(target)


def p2() -> int:
    lines = get_input(10)
    res = 0
    for line in lines:
        target = tuple(map(int, line[:-1].split('{')[1].split(',')))
        buttons = [tuple(map(int, b.split(','))) for b in re.findall(r'\(([\d+,]*\d+)\)', line)]
        res += solve_single(buttons, target)
    return res


if __name__ == '__main__':
    print_summary(__file__, p1, p2)
