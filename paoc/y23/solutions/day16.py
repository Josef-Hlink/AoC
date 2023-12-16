#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 23 Day 16 - The Floor Will Be Lava """

from paoc.helper import get_input, print_summary


FM = '/'
BM = '\\'
VS = '-'
HS = '|'

N = (-1, 0)
S = (+1, 0)
W = (0, -1)
E = (0, +1)

MIRRORS = {
    FM: {N: E, S: W, W: S, E: N},
    BM: {N: W, S: E, W: N, E: S}
}

SPLITS = {
    VS: {N: (W, E), S: (W, E), W: (W, ), E: (E, )},
    HS: {N: (N, ), S: (S, ), W: (N, S), E: (N, S)}
}

Pos = tuple[int, int]
Dir = tuple[int, int]

class Head:
    def __init__(self, pos: Pos, dir: Dir):
        self.pos = pos
        self.dir = dir

    def step(self) -> None:
        next_pos = (self.pos[0] + self.dir[0], self.pos[1] + self.dir[1])
        self.pos = next_pos
    
    @property
    def in_grid(self) -> bool:
        return -1 < self.r < R and -1 < self.c < C

    @property
    def r(self) -> int: return self.pos[0]

    @property
    def c(self) -> int: return self.pos[1]

def find_energized(grid: list[str]) -> set[Pos]:

    global R, C
    R, C = len(grid), len(grid[0])

    first_head = Head((0, 0), E)
    heads = [first_head]
    head_starts = {(first_head.pos, first_head.dir)}

    budget = 1000
    energized: set[Pos] = set()
    while heads and budget:
        new_heads = []
        for head in heads:
            while head.in_grid:
                energized.add(head.pos)
                tile_type = grid[head.r][head.c]
                if tile_type == '.':
                    pass
                elif tile_type in MIRRORS:
                    head.dir = MIRRORS[tile_type][head.dir]
                elif tile_type in SPLITS:
                    new_dirs = SPLITS[tile_type][head.dir]
                    if len(new_dirs) == 1:
                        head.dir = new_dirs[0]
                    elif len(new_dirs) == 2:
                        for new_head in (Head(head.pos, new_dirs[0]), Head(head.pos, new_dirs[1])):
                            if (new_head.pos, new_head.dir) not in head_starts:
                                new_heads.append(new_head)
                                head_starts.add((new_head.pos, new_head.dir))
                        break
                head.step()
            heads.remove(head)
        heads += new_heads
        budget -= 1

    return energized


def p1() -> int:
    grid = get_input(16)
    return len(find_energized(grid))

def p2() -> int:
    _ = get_input(16)


if __name__ == '__main__':
    print(p1())
    # print_summary(__file__, p1, p2)
