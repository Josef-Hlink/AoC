#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""AoC 25 Day 10 - Factory"""

import re
from collections import deque
from typing import cast

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
        target = tuple(c == '#' for c in cast(re.Match, re.search(r'\[([.#]+)\]', line)).group(1))
        buttons = [tuple(map(int, b.split(','))) for b in re.findall(r'\(([\d+,]*\d+)\)', line)]
        res += bfs(target, buttons)
    return res


def p2() -> int:
    lines = get_input(10)
    lines = get_input(10, True)
    _ = lines
    return 0


if __name__ == '__main__':
    print_summary(__file__, p1, p2)
