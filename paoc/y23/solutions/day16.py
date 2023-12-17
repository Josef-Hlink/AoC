#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 23 Day 16 - The Floor Will Be Lava """

from paoc.helper import get_input, print_summary
from collections import deque
import os
import sys
import time


N = (-1, 0)
S = (+1, 0)
W = (0, -1)
E = (0, +1)

class Photon:
    def __init__(self, pos: tuple[int, int], dir: tuple[int, int]):
        self.pos = pos
        self.dir = dir

    def move(self) -> None:
        next_pos = (self.pos[0] + self.dir[0], self.pos[1] + self.dir[1])
        self.pos = next_pos

class Contraption:
    def __init__(self, lines: list[str], visual: bool = False):
        self.raw = lines
        self.nr = len(lines)
        self.nc = len(lines[0])
        self.energized: set[tuple[int, int]] = set()
        self.visual = visual
        if visual:
            self.processed = [['#'] * (self.nc + 2)] + [list(f'#{line}#') for line in self.raw] + [['#'] * (self.nc + 2)]
    
    def __getitem__(self, key: int) -> str:
        return self.raw[key]
    
    def energize(self, pos: tuple[int, int]) -> None:
        self.energized.add(pos)
        if self.visual:
            r, c = pos
            self.processed[r+1][c+1] = f"\033[30;43m{self.raw[r][c]}\033[0m"
    
    def copy(self) -> "Contraption":
        return Contraption(self.raw.copy())
    
    def render(self) -> None:
        os.system('clear')
        print('\n'.join(''.join(line) for line in self.processed))
        time.sleep(1)

def energize(contraption: Contraption, origin: Photon) -> Contraption:

    mirrors = {
        '/':  {N: E,  S: W,  W: S,  E: N},
        '\\': {N: W,  S: E,  W: N,  E: S}
    }
    splits = {
        '-': {N: (W, E),  S: (W, E)},
        '|': {W: (N, S),  E: (N, S)}
    }

    photons = deque()
    photons.append(origin)
    sources = {(origin.pos, origin.dir)}

    while photons:
        p = photons.popleft()
        while -1 < p.pos[0] < contraption.nr and -1 < p.pos[1] < contraption.nc:
            contraption.energize(p.pos)
            tile_type = contraption[p.pos[0]][p.pos[1]]
            if tile_type == '.':
                # this happens often, so we save time by skipping slightly more expensive checks
                pass
            elif tile_type in mirrors:
                # direction just gets changed, but we'll keep using the same photon object
                p.dir = mirrors[tile_type][p.dir]
            elif tile_type in splits and p.dir in splits[tile_type]:
                # two new photon objects are created (if we haven't seen them before)
                new_dirs = splits[tile_type][p.dir]
                for p_ in (Photon(p.pos, new_dirs[0]), Photon(p.pos, new_dirs[1])):
                    if (p_.pos, p_.dir) not in sources:
                        photons.append(p_)
                        sources.add((p_.pos, p_.dir))
                # the old photon dies
                break
            p.move()
        if contraption.visual:
            contraption.render()
    return contraption


def p1() -> int:
    return len(energize(Contraption(get_input(16)), Photon((0, 0), E)).energized)

def p2() -> int:
    contraption = Contraption(get_input(16))
    max_energized = 0
    for r in range(contraption.nr):
        max_energized = max(max_energized, len(energize(contraption.copy(), Photon((r, 0), E)).energized))
        max_energized = max(max_energized, len(energize(contraption.copy(), Photon((r, contraption.nc-1), W)).energized))
    for c in range(contraption.nr):
        max_energized = max(max_energized, len(energize(contraption.copy(), Photon((0, c), S)).energized))
        max_energized = max(max_energized, len(energize(contraption.copy(), Photon((contraption.nr-1, c), N)).energized))
    return max_energized


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'visualize':
        _ = energize(Contraption(get_input(16), visual=True), Photon((0, 0), E))
    else:
        print_summary(__file__, p1, p2, n=10)
